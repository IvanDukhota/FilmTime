package com.filmtime.model;

import java.io.Serializable;

public class UserProfileResponse implements Serializable {
    public final static String EXTRA_KEY = "user_profile_data";
    private String email;
    private String username;
    private String country;
    private String bio;
    private String profile_picture;
    private Genre[] genres;
    private String role;
    private String status;
    public UserProfileResponse()
    { }
    public UserProfileResponse(String email, String username, String country, String bio,
                               String profilePicture, Genre[] genres, String role, String status) {
        this.email = email;
        this.username = username;
        this.country = country;
        this.bio = bio;
        this.profile_picture = profilePicture;
        this.genres = genres;
        this.role = role;
        this.status = status;
    }


    public void setEmail(String email) {
        this.email = email;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public void setBio(String bio) {
        this.bio = bio;
    }

    public void setProfilePicture(String profilePicture) {
        this.profile_picture = profilePicture;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getEmail() {
        return email;
    }

    public String getUsername() {
        return username;
    }

    public String getCountry() {
        return country;
    }

    public String getBio() {
        return bio;
    }

    public String getProfilePicture() {
        return profile_picture;
    }

    public String getRole() {
        return role;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public void setGenres(Genre[] genres) {
        this.genres = genres;
    }

    public Genre[] getGenres() {
        return genres;
    }

    public void setProfile_picture(String profile_picture) {
        this.profile_picture = profile_picture;
    }

}