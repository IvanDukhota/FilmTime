package com.filmtime.util;

import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import com.filmtime.api.ApiService;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.RetrofitClient;
import com.filmtime.model.UserProfileEditRequest;
import com.filmtime.model.UserProfileEditResponse;
import com.filmtime.model.UserProfileResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class UserProfileManager {
    private UserProfileResponse userProfileData;
    public UserProfileResponse getUserProfileData() {
        return userProfileData;
    }
    public void setUserProfileData(UserProfileResponse userProfileData) {
        this.userProfileData = userProfileData;
    }

    public UserProfileManager(UserProfileResponse userProfileResponse) {
        userProfileData = userProfileResponse;
    }

    public static UserProfileManager fromIntentExtra(Intent intent) {
        UserProfileResponse userProfileData = (UserProfileResponse) intent.getSerializableExtra(UserProfileResponse.EXTRA_KEY);
        UserProfileManager instance = new UserProfileManager(userProfileData);
        return instance;
    }

    public boolean isDataNull() {
        return userProfileData == null;
    }

    public void fetchUserProfileData(Context context, Runnable onResponseSuccess, Runnable onResponseError, Runnable onFailure) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.getUserProfile().enqueue(new Callback<UserProfileResponse>() {
            @Override
            public void onResponse(Call<UserProfileResponse> call, Response<UserProfileResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    userProfileData = (UserProfileResponse) response.body();
                    onResponseSuccess.run();
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    onResponseError.run();
                }
            }
            @Override
            public void onFailure(Call<UserProfileResponse> call, Throwable t) {
                Toast.makeText(context, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                onFailure.run();
            }
        });
    }

    public void editUserProfileData(Context context, UserProfileEditRequest userProfileEditRequest, Runnable onResponseSuccess, Runnable onResponseError, Runnable onFailure) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.editUserProfile(userProfileEditRequest).enqueue(new Callback<UserProfileEditResponse>() {
            @Override
            public void onResponse(Call<UserProfileEditResponse> call, Response<UserProfileEditResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.body().getMessage());
                    Log.i("API_LOG", response.body().getData());
                    onResponseSuccess.run();
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    onResponseError.run();
                }
            }
            @Override
            public void onFailure(Call<UserProfileEditResponse> call, Throwable t) {
                Toast.makeText(context, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                onFailure.run();
            }
        });
    }
    public void displayUserProfileData(TextView usernameTextView, TextView emailTextView,
                                       TextView bioTextView, TextView countryTextView) {
        try {
            usernameTextView.setText(userProfileData.getUsername());
            emailTextView.setText(userProfileData.getEmail());
            bioTextView.setText(userProfileData.getBio());
            countryTextView.setText(userProfileData.getCountry());
        }
        catch (NullPointerException ex) {
            Log.e("PROFILE_EX", ex.getMessage());
        }
    }
}