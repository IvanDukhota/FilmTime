package com.filmtime.model;

import android.content.Context;
import android.util.Log;

import com.filmtime.api.ApiService;
import com.filmtime.api.ApiStatus;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.Content.ContentByIdContract;
import com.filmtime.api.Content.ContentByTitleContract;
import com.filmtime.api.RetrofitClient;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ContentModel {
    ContentResponse[] contentResponse;

    public ContentModel()
    { }
    public ContentModel(ContentResponse[] contentResponse) {
        this.contentResponse = contentResponse;
    }

    public void fetchContentById(ContentByIdContract consumer, int id) {
        ApiService apiService = RetrofitClient.getInstance().create(ApiService.class);
        apiService.getContentDetails(id).enqueue(new Callback<ContentResponse>() {
            @Override
            public void onResponse(Call<ContentResponse> call, Response<ContentResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.message());
                    contentResponse = new ContentResponse[] { response.body() };
                    consumer.onFetchContentByIdResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onFetchContentByIdResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<ContentResponse> call, Throwable t) {
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                consumer.onFetchContentByIdResponse(ApiStatus.FAILURE);
            }
        });
    }

    public void fetchContentByTitle(ContentByTitleContract consumer, String title) {
        ApiService apiService = RetrofitClient.getInstance().create(ApiService.class);
        apiService.getContent(title).enqueue(new Callback<ContentResponse[]>() {
            @Override
            public void onResponse(Call<ContentResponse[]> call, Response<ContentResponse[]> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("API_LOG", response.message());
                    contentResponse = response.body();
                    consumer.onFetchContentByTitleResponse(ApiStatus.RESPONSE_OK);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    consumer.onFetchContentByTitleResponse(ApiStatus.RESPONSE_ERR);
                }
            }
            @Override
            public void onFailure(Call<ContentResponse[]> call, Throwable t) {
                Log.e("API_ERROR", "Error: " + t.getMessage());
                t.printStackTrace();
                consumer.onFetchContentByTitleResponse(ApiStatus.FAILURE);
            }
        });
    }

    public ContentResponse getContentResponse() {
        if (contentResponse == null || contentResponse.length == 0) {
            return null;
        }
        return contentResponse[0];
    }

    public ContentResponse[] getAllContent() {
        return contentResponse;
    }

    public void setContentResponse(ContentResponse[] contentResponse) {
        this.contentResponse = contentResponse;
    }
}
