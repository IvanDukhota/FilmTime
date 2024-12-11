package com.filmtime.api;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import com.filmtime.util.Constants;

public class RetrofitClient {
    public static Retrofit getInstance(AuthInterceptor authInterceptor) {
            OkHttpClient.Builder clientBuilder = new OkHttpClient.Builder();

            // Add the interceptor if provided
            if (authInterceptor != null) {
                clientBuilder.addInterceptor(authInterceptor);
            }

            OkHttpClient client = clientBuilder.build();

            return new Retrofit.Builder()
                    .baseUrl(Constants.SERVER_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .client(client)
                    .build();
    }
    public static Retrofit getInstance() {
        return new Retrofit.Builder()
                .baseUrl(Constants.SERVER_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .client(new OkHttpClient.Builder().build())
                .build();
    }
}