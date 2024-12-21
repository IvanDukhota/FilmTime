package com.filmtime;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.UserProfile.UserProfileFetchContract;
import com.filmtime.model.UserProfileResponse;
import com.filmtime.ui.UserProfileDisplay;
import com.filmtime.api.ApiStatus;
import com.filmtime.util.JwtManager;
import com.filmtime.model.UserProfileModel;
import com.filmtime.util.Util;

public class UserProfileActivity extends AppCompatActivity implements View.OnClickListener, UserProfileFetchContract {
    private UserProfileModel userProfileModel;
    private UserProfileDisplay userProfileDisplay;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_profile);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        Button logOutButton = (Button) findViewById(R.id.buttonLogOut);
        logOutButton.setOnClickListener(this);
        Button editButton = (Button) findViewById(R.id.buttonEditProfile);
        editButton.setOnClickListener(this);

        TextView usernameTextView = (TextView) findViewById(R.id.usernameTextView);
        TextView emailTextView = (TextView) findViewById(R.id.emailTextView);
        TextView countryTextView = (TextView) findViewById(R.id.countryTextView);
        TextView bioTextView = (TextView) findViewById(R.id.bioTextView);
        ImageView pfpImageView = (ImageView) findViewById(R.id.pfpImageView);

        userProfileDisplay = new UserProfileDisplay(usernameTextView, emailTextView, bioTextView,
                countryTextView, pfpImageView);
    }

    @Override
    protected void onStart() {
        super.onStart();
        getUserProfileData();
    }

    private void getUserProfileData() {
        userProfileModel = UserProfileModel.fromIntentExtra(getIntent());

        if (userProfileModel.isDataNull()) {
            userProfileModel.fetchUserProfileData(this, this);
        }
        else {
            userProfileDisplay.displayUserProfileData(userProfileModel.getUserProfileData());
        }
    }

    @Override
    public void onUserProfileFetchResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                if (userProfileModel.isDataNull()) {
                    Log.e("API_ERROR", "User profile fetch returned null.");
                    Toast.makeText(this,
                            "Error: failed to fetch user profile.", Toast.LENGTH_SHORT).show();
                    Util.redirectToActivity(this, LoginActivity.class);
                }
                userProfileDisplay.displayUserProfileData(userProfileModel.getUserProfileData());
                break;
            }
            case FAILURE:
            case RESPONSE_ERR: {
                Util.redirectToActivity(this, LoginActivity.class);
                break;
            }
        }
    }

    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.buttonEditProfile: {
                Intent intent = new Intent(this, ProfileEditActivity.class);
                intent.putExtra(UserProfileResponse.EXTRA_KEY, userProfileModel.getUserProfileData());
                startActivity(intent);
                break;
            }
            case R.id.buttonLogOut: {
                JwtManager jwtManager = new JwtManager(this);
                jwtManager.deleteAccessToken();
                jwtManager.deleteRefreshToken();
                Util.redirectToActivity(this, LoginActivity.class);
                finishAndRemoveTask();
                break;
            }
        }
    }
}