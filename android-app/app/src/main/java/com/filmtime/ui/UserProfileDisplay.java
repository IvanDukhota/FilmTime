package com.filmtime.ui;

import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import com.filmtime.model.UserProfileResponse;

public class UserProfileDisplay {
    private ImageView pfpImageView;
    private TextView usernameTextView;
    private TextView emailTextView;
    private TextView bioTextView;
    private TextView countryTextView;

    public UserProfileDisplay(TextView usernameTextView, TextView emailTextView,
                              TextView bioTextView, TextView countryTextView, ImageView pfpImageView) {
        this.usernameTextView = usernameTextView;
        this.emailTextView = emailTextView;
        this.bioTextView = bioTextView;
        this.countryTextView = countryTextView;
        this.pfpImageView = pfpImageView;
    }

    public void displayUserProfileData(UserProfileResponse userProfileData) {
        try {
            usernameTextView.setText(userProfileData.getUsername());
            emailTextView.setText(userProfileData.getEmail());
            bioTextView.setText(userProfileData.getBio());
            countryTextView.setText(userProfileData.getCountry());

            //TODO: reimplement image fetching
        }
        catch (NullPointerException ex) {
            Log.e("PROFILE_EX", ex.getMessage());
        }
    }

    public UserProfileResponse readUserProfileData() {
        UserProfileResponse data = new UserProfileResponse();
        try {
            data.setEmail(emailTextView.getText().toString());
            data.setBio(bioTextView.getText().toString());
            data.setUsername(usernameTextView.getText().toString());
            data.setCountry(countryTextView.getText().toString());
        }
        catch (NullPointerException ex) {
            Log.e("PROFILE_EX", ex.getMessage());
            return null;
        }
        return data;
    }
}
