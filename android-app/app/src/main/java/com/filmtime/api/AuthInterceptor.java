package com.filmtime.api;

import android.content.Context;

import com.filmtime.model.LoginResponse;
import com.filmtime.util.JwtManager;
import com.filmtime.util.Constants;

import java.io.IOException;

import okhttp3.Interceptor;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class AuthInterceptor implements Interceptor {
    private JwtManager jwtManager;
    private ApiService apiService;

    public AuthInterceptor(Context context) {
        jwtManager = new JwtManager(context);
        apiService = new Retrofit.Builder()
                .baseUrl(Constants.SERVER_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .client(new OkHttpClient.Builder().build())
                .build()
                .create(ApiService.class);
    }

    @Override
    public Response intercept(Chain chain) throws IOException {
        Request originalRequest = chain.request();
        String token = jwtManager.getAccessToken();

        if (token != null) {
            Request modifiedRequest = originalRequest.newBuilder()
                    .addHeader("Authorization", "Bearer " + token)
                    .build();

            Response response = chain.proceed(modifiedRequest);
            if (response.code() == 401) {
                response.close();
                String newAccessToken = refreshAccessToken();
                if (newAccessToken != null) {
                    jwtManager.saveAccessToken(newAccessToken);

                    // Retry the original request with the new access token
                    Request retryRequest = originalRequest.newBuilder()
                            .addHeader("Authorization", "Bearer " + newAccessToken)
                            .build();
                    return chain.proceed(retryRequest);
                }
            }
            return response;
        }

        return chain.proceed(originalRequest);
    }
    private String refreshAccessToken() {
        String refreshToken = jwtManager.getRefreshToken();
        if (refreshToken == null) {
            return null;
        }
        try {
            retrofit2.Response<LoginResponse> response = apiService.refreshToken(refreshToken).execute();
            if (response.isSuccessful() && response.body() != null) {
                return response.body().getAccess();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }
}