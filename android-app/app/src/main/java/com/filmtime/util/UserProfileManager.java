package com.filmtime.util;

import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;

import com.filmtime.api.ApiConsumer;
import com.filmtime.api.ApiService;
import com.filmtime.api.ApiStatus;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.RetrofitClient;
import com.filmtime.model.UserProfileEditRequest;
import com.filmtime.model.UserProfileEditResponse;
import com.filmtime.model.UserProfileResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class UserProfileManager {
    private ApiConsumer consumer;
    private UserProfileResponse userProfileData;
    public UserProfileResponse getUserProfileData() {
        return userProfileData;
    }

    public UserProfileManager(UserProfileResponse userProfileResponse, ApiConsumer consumer) {
        userProfileData = userProfileResponse;
        this.consumer = consumer;
    }

    public void setConsumer(ApiConsumer consumer) {
        this.consumer = consumer;
    }
    public void setUserProfileData(UserProfileResponse userProfileData) {
        this.userProfileData = userProfileData;
    }

    public static UserProfileManager fromIntentExtra(Intent intent, ApiConsumer consumer) {
        UserProfileResponse userProfileData = (UserProfileResponse) intent.getSerializableExtra(UserProfileResponse.EXTRA_KEY);
        return new UserProfileManager(userProfileData, consumer);
    }

    public boolean isDataNull() {
        return userProfileData == null;
    }

    public void fetchUserProfileData(Context context) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.getUserProfile().enqueue(new Callback<UserProfileResponse>() {
            @Override
            public void onResponse(Call<UserProfileResponse> call, Response<UserProfileResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    userProfileData = (UserProfileResponse) response.body();
                    consumer.onResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<UserProfileResponse> call, Throwable t) {
                Log.e("API_FAILURE", "Error: " + t.getMessage());
                consumer.onResponse(ApiStatus.FAILURE);
            }
        });
    }

    public void editUserProfileData(Context context, UserProfileEditRequest userProfileEditRequest) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.editUserProfile(userProfileEditRequest).enqueue(new Callback<UserProfileEditResponse>() {
            @Override
            public void onResponse(Call<UserProfileEditResponse> call, Response<UserProfileEditResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.body().getMessage());
                    consumer.onResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<UserProfileEditResponse> call, Throwable t) {
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                consumer.onResponse(ApiStatus.FAILURE);
            }
        });
    }
}