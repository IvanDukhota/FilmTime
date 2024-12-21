package com.filmtime.model;

import java.io.Serializable;

public class UserProfileResponse implements Serializable {
    public final static String EXTRA_KEY = "user_profile_data";
    private String email;
    private String username;
    private String country;
    private String bio;
    private byte[] profile_picture;
    private String role;

    private String status;
    public UserProfileResponse()
    { }
    public UserProfileResponse(String email, String username, String country, String bio,
                               byte[] profilePicture, String role, String status) {
        this.email = email;
        this.username = username;
        this.country = country;
        this.bio = bio;
        this.profile_picture = profilePicture;
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

    public void setProfilePicture(byte[] profilePicture) {
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

    public byte[] getProfilePicture() {
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
}