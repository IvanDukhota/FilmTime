package com.filmtime.model;

import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.filmtime.api.UserProfile.UserProfileEditContract;
import com.filmtime.api.UserProfile.UserProfileFetchContract;
import com.filmtime.api.ApiService;
import com.filmtime.api.ApiStatus;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.RetrofitClient;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class UserProfileModel {
    private UserProfileResponse userProfileData;
    public UserProfileResponse getUserProfileData() {
        return userProfileData;
    }

    public UserProfileModel()
    { }

    public UserProfileModel(UserProfileResponse userProfileResponse) {
        userProfileData = userProfileResponse;
    }

    public void setUserProfileData(UserProfileResponse userProfileData) {
        this.userProfileData = userProfileData;
    }

    public static UserProfileModel fromIntentExtra(Intent intent) {
        UserProfileResponse userProfileData = (UserProfileResponse) intent.getSerializableExtra(UserProfileResponse.EXTRA_KEY);
        return new UserProfileModel(userProfileData);
    }

    public boolean isDataNull() {
        return userProfileData == null;
    }

    public void fetchUserProfileData(Context context, UserProfileFetchContract consumer) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.getUserProfile().enqueue(new Callback<UserProfileResponse>() {
            @Override
            public void onResponse(Call<UserProfileResponse> call, Response<UserProfileResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    userProfileData = (UserProfileResponse) response.body();
                    consumer.onUserProfileFetchResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onUserProfileFetchResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<UserProfileResponse> call, Throwable t) {
                Log.e("API_FAILURE", "Error: " + t.getMessage());
                consumer.onUserProfileFetchResponse(ApiStatus.FAILURE);
            }
        });
    }

    public void editUserProfileData(Context context, UserProfileEditContract consumer,
                                    UserProfileEditRequest userProfileEditRequest) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.editUserProfile(userProfileEditRequest).enqueue(new Callback<UserProfileEditResponse>() {
            @Override
            public void onResponse(Call<UserProfileEditResponse> call, Response<UserProfileEditResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.body().getMessage());
                    consumer.onUserProfileEditResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onUserProfileEditResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<UserProfileEditResponse> call, Throwable t) {
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                consumer.onUserProfileEditResponse(ApiStatus.FAILURE);
            }
        });
    }
}