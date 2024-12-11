package com.filmtime.api;

import com.filmtime.model.LoginRequest;
import com.filmtime.model.LoginResponse;
import com.filmtime.model.UserProfileResponse;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

public interface ApiService {
    @POST("/api/v1/login/")
    Call<LoginResponse> login(@Body LoginRequest loginRequest);

    @GET("/api/v1/user/profile/")
    Call<UserProfileResponse> getUserProfile();

    @POST("/api/v1/token/refresh/")
    Call<LoginResponse> refreshToken(@Body String refresh);
}