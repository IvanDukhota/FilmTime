package com.filmtime;

import android.content.Intent;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.ApiStatus;
import com.filmtime.api.UserProfile.UserProfileFetchContract;
import com.filmtime.model.UserProfileResponse;
import com.filmtime.ui.MenuAdapter;
import com.filmtime.util.JwtManager;
import com.filmtime.model.UserProfileModel;
import com.filmtime.util.Util;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity implements UserProfileFetchContract {
    private UserProfileModel userProfileModel;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        loginWithStoredToken();

        BottomNavigationView menu = findViewById(R.id.bottomNavigationView);
        menu.setSelectedItemId(R.id.movie);
        MenuAdapter.initMenu(this, menu);
    }
    private void loginWithStoredToken() {
        JwtManager jwtManager = new JwtManager(this);
        if (!jwtManager.hasAccessToken() && !jwtManager.hasRefreshToken()) {
            Util.redirectToActivity(this, LoginActivity.class);
            return;
        }
        userProfileModel = new UserProfileModel();
        userProfileModel.fetchUserProfileData(this, this);
    }

    @Override
    public void onUserProfileFetchResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                Intent intent = new Intent(MainActivity.this, UserProfileActivity.class);
                intent.putExtra(UserProfileResponse.EXTRA_KEY, userProfileModel.getUserProfileData());
                MainActivity.this.startActivity(intent);
                break;
            }
            case RESPONSE_ERR:
            case FAILURE: {
                Util.redirectToActivity(this, LoginActivity.class);
                break;
            }
        }
    }
}