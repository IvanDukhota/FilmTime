package com.filmtime.api;

import com.filmtime.model.ContentResponse;
import com.filmtime.model.Genre;
import com.filmtime.model.LoginRequest;
import com.filmtime.model.LoginResponse;
import com.filmtime.model.MessageResponse;
import com.filmtime.model.PreferencesSaveRequest;
import com.filmtime.model.RefreshTokenRequest;
import com.filmtime.model.RegisterRequest;
import com.filmtime.model.UserContentInteraction;
import com.filmtime.model.UserProfileEditResponse;
import com.filmtime.model.UserProfileResponse;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.PATCH;
import retrofit2.http.PUT;
import retrofit2.http.Part;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface ApiService {
    @POST("/api/v1/registration/login/")
    Call<LoginResponse> login(@Body LoginRequest loginRequest);

    @POST("/api/v1/registration/register/")
    Call<LoginResponse> signUp(@Body RegisterRequest registerRequest);

    @GET("/api/v1/registration/user/profile/")
    Call<UserProfileResponse> getUserProfile();

    @Multipart
    @PATCH("/api/v1/registration/user/profile/edit/")
    Call<UserProfileEditResponse> editUserProfile(
            @Part("password") RequestBody password,
            @Part("username") RequestBody username,
            @Part("country") RequestBody country,
            @Part("bio") RequestBody bio,
            @Part MultipartBody.Part profile_picture
    );

    @Multipart
    @PATCH("/api/v1/registration/user/profile/edit/")
    Call<UserProfileEditResponse> editUserProfile(
            @Part("username") RequestBody username,
            @Part("country") RequestBody country,
            @Part("bio") RequestBody bio,
            @Part MultipartBody.Part profile_picture
    );

    @POST("/api/v1/registration/token/refresh/")
    Call<LoginResponse> refreshToken(@Body RefreshTokenRequest refresh);

    @GET("/api/v1/content/genres/")
    Call<Genre[]> getGenres();

    @PUT("/api/v1/registration/update-user-genres/")
    Call<MessageResponse> putGenres(@Body PreferencesSaveRequest request);

    @GET("/api/v1/user/history/")
    Call<UserContentInteraction[]> getUserHistory();

    @GET("/api/v1/content/movie/{movie_id}")
    Call<ContentResponse> getContentDetails(@Path("movie_id") int movieId);

    @GET("/api/v1/content/movies/filter/")
    Call<ContentResponse[]> getContent(@Query("title") String params);
}