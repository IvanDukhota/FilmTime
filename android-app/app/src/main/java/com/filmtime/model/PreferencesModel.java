package com.filmtime.model;

import android.content.Context;
import android.util.Log;

import com.filmtime.api.ApiService;
import com.filmtime.api.ApiStatus;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.UserProfile.PreferencesSaveContract;
import com.filmtime.api.RetrofitClient;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class PreferencesModel {
    public void putUserPreferences(Context context, PreferencesSaveContract consumer, int[] genreIds) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.putGenres(new PreferencesSaveRequest(genreIds)).enqueue(new Callback<MessageResponse>() {
            @Override
            public void onResponse(Call<MessageResponse> call, Response<MessageResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.message());
                    consumer.onPreferencesSaveResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onPreferencesSaveResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<MessageResponse> call, Throwable t) {
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                consumer.onPreferencesSaveResponse(ApiStatus.FAILURE);
            }
        });
    }
}
