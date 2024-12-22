package com.filmtime.model;

import android.content.Context;
import android.util.Log;

import com.filmtime.api.ApiService;
import com.filmtime.api.ApiStatus;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.UserProfile.HistoryFetchContract;
import com.filmtime.api.RetrofitClient;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class UserHistoryModel {
    private UserContentInteraction[] userInteractions;

    public UserHistoryModel()
    { }

    public void fetchHistory(Context context, HistoryFetchContract consumer) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.getUserHistory().enqueue(new Callback<UserContentInteraction[]>() {
            @Override
            public void onResponse(Call<UserContentInteraction[]> call, Response<UserContentInteraction[]> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.message());
                    userInteractions = response.body();
                    consumer.onHistoryFetchResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onHistoryFetchResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<UserContentInteraction[]> call, Throwable t) {
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                consumer.onHistoryFetchResponse(ApiStatus.FAILURE);
            }
        });
    }

    public UserContentInteraction[] getUserInteractions() {
        return userInteractions;
    }

    public void setUserInteractions(UserContentInteraction[] userInteractions) {
        this.userInteractions = userInteractions;
    }
}
