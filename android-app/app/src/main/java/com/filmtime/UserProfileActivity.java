package com.filmtime;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ExpandableListView;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.UserProfile.UserProfileFetchContract;
import com.filmtime.model.Genre;
import com.filmtime.model.UserProfileResponse;
import com.filmtime.ui.UserProfileDisplay;
import com.filmtime.api.ApiStatus;
import com.filmtime.ui.UserProfileListAdapter;
import com.filmtime.util.JwtManager;
import com.filmtime.model.UserProfileModel;
import com.filmtime.util.Util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class UserProfileActivity extends AppCompatActivity implements View.OnClickListener, UserProfileFetchContract {
    private ExpandableListView expandableListView;
    private List<String> expandableListTitle;
    private HashMap<String, List<String>> expandableListDetail;
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

        expandableListView = (ExpandableListView) findViewById(R.id.user_profile_expandable_list);
        expandableListDetail = new HashMap<>();
        expandableListTitle = new ArrayList<>();
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
            fillUserPreferencesList(userProfileModel.getUserProfileData());
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

                fillUserPreferencesList(userProfileModel.getUserProfileData());
                break;
            }
            case FAILURE:
            case RESPONSE_ERR: {
                Util.redirectToActivity(this, LoginActivity.class);
                break;
            }
        }
    }

    private void fillUserPreferencesList(UserProfileResponse userdata) {
        List<String> genrePreferences = Arrays.stream(userdata.getGenres())
                .map(Genre::getName)
                .collect(Collectors.toList());
        expandableListDetail.put("Preferences", genrePreferences);
        expandableListTitle = new ArrayList<String>(expandableListDetail.keySet());
        expandableListView.setAdapter(new UserProfileListAdapter(
                this, expandableListTitle, expandableListDetail)
        );
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