package com.filmtime.model;

import android.content.Context;
import android.util.Log;

import com.filmtime.api.ApiService;
import com.filmtime.api.ApiStatus;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.Content.GenresFetchContract;
import com.filmtime.api.RetrofitClient;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class GenresModel {
    private Genre[] genresResponse;
    public GenresModel()
    { }

    public Genre[] getGenres() {
        return genresResponse;
    }

    public void getGenres(Context context, GenresFetchContract consumer) {
        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(context)).create(ApiService.class);
        apiService.getGenres().enqueue(new Callback<Genre[]>() {
            @Override
            public void onResponse(Call<Genre[]> call, Response<Genre[]> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.message());
                    genresResponse = response.body();
                    consumer.onGenresFetchResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onGenresFetchResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<Genre[]> call, Throwable t) {
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                consumer.onGenresFetchResponse(ApiStatus.FAILURE);
            }
        });
    }
}
