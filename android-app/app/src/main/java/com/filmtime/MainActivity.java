package com.filmtime;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.ApiStatus;
import com.filmtime.api.Content.ContentByTitleContract;
import com.filmtime.api.UserProfile.UserProfileFetchContract;
import com.filmtime.model.ContentModel;
import com.filmtime.model.ContentResponse;
import com.filmtime.ui.MenuAdapter;
import com.filmtime.util.JwtManager;
import com.filmtime.model.UserProfileModel;
import com.filmtime.util.Util;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity implements Button.OnClickListener, UserProfileFetchContract,
        ContentByTitleContract {
    private UserProfileModel userProfileModel;
    private EditText searchField;
    private ContentModel contentModel;

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

        Button searchButton = findViewById(R.id.search_button);
        searchButton.setOnClickListener(this);

        searchField = findViewById(R.id.search_field);

        contentModel = new ContentModel();

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
                break;
            }
            case RESPONSE_ERR:
            case FAILURE: {
                Util.redirectToActivity(this, LoginActivity.class);
                break;
            }
        }
    }

    @Override
    public void onFetchContentByTitleResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                if (contentModel.getContentResponse() == null) {
                    Toast.makeText(this, "No content with this title found!", Toast.LENGTH_SHORT).show();
                    return;
                }

                Intent intent = new Intent(MainActivity.this, ContentPageActivity.class);
                intent.putExtra(ContentResponse.EXTRA_KEY_ID, contentModel.getContentResponse().getId());
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

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.search_button) {
            contentModel.fetchContentByTitle(this, searchField.getText().toString());
        }
    }
}