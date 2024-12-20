package com.filmtime.api;

import com.filmtime.model.LoginRequest;
import com.filmtime.model.LoginResponse;
import com.filmtime.model.RegisterRequest;
import com.filmtime.model.UserProfileEditRequest;
import com.filmtime.model.UserProfileEditResponse;
import com.filmtime.model.UserProfileResponse;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PATCH;

public interface ApiService {
    @POST("/api/v1/registration/login/")
    Call<LoginResponse> login(@Body LoginRequest loginRequest);

    @POST("/api/v1/registration/register/")
    Call<LoginResponse> signUp(@Body RegisterRequest registerRequest);

    @GET("/api/v1/registration/user/profile/")
    Call<UserProfileResponse> getUserProfile();

    @PATCH("/api/v1/registration/user/profile/edit/")
    Call<UserProfileEditResponse> editUserProfile(@Body UserProfileEditRequest userProfileEditRequest);

    @POST("/api/v1/registration/token/refresh/")
    Call<LoginResponse> refreshToken(@Body String refresh);
}