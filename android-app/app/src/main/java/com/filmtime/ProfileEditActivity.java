package com.filmtime;

import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.ApiService;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.RetrofitClient;
import com.filmtime.model.UserProfileEditRequest;
import com.filmtime.model.UserProfileResponse;
import com.filmtime.util.UserProfileManager;
import com.filmtime.util.Util;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ProfileEditActivity extends AppCompatActivity implements View.OnClickListener {
    private UserProfileManager userProfileManager;
    private EditText passwordEditText;
    private EditText emailEditText;
    private EditText passwordRepeatEditText;
    private EditText usernameEditText;
    private EditText countryEditText;
    private EditText bioEditText;
    private boolean changePassword;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_profile_edit);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        Button cancelButton = (Button) findViewById(R.id.buttonCancelEdit);
        cancelButton.setOnClickListener(this);
        Button saveButton = (Button) findViewById(R.id.buttonSaveEdited);
        saveButton.setOnClickListener(this);

        passwordEditText = (EditText) findViewById(R.id.editTextPassword);
        passwordRepeatEditText = (EditText) findViewById(R.id.editTextRepeatPassword);
        usernameEditText = (EditText) findViewById(R.id.editTextUsername);
        countryEditText = (EditText) findViewById(R.id.editTextCountry);
        bioEditText = (EditText) findViewById(R.id.editTextBio);

        userProfileManager = UserProfileManager.fromIntentExtra(getIntent());
        if (userProfileManager.isDataNull()) {
            userProfileManager.fetchUserProfileData(this,
                    () -> {
                        if (userProfileManager.isDataNull()) {
                            Log.e("API_ERROR", "User profile fetch returned null.");
                            Toast.makeText(ProfileEditActivity.this,
                                    "Error: failed to fetch user profile.", Toast.LENGTH_SHORT).show();
                            finish();
                        }
                        userProfileManager.displayUserProfileData(usernameEditText, emailEditText,
                                bioEditText, countryEditText);
                    },
                    this::finish,
                    this::finish
            );
        }
        else {
            userProfileManager.displayUserProfileData(usernameEditText, emailEditText,
                    bioEditText, countryEditText);
        }
    }

    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.buttonCancelEdit: {
                Util.redirectToActivity(this, UserProfileActivity.class);
                break;
            }
            case R.id.buttonSaveEdited: {
                if (!isInputDataValid()) {
                    break;
                }

                UserProfileEditRequest request = new UserProfileEditRequest(usernameEditText.getText().toString(),
                        countryEditText.getText().toString(),
                        bioEditText.getText().toString(),
                        null, null);
                if (changePassword)
                    request.setPassword(passwordEditText.getText().toString());

                userProfileManager.editUserProfileData(this,
                        request,
                        () -> {
                            Toast.makeText(this, "Data modified successfully!", Toast.LENGTH_SHORT).show();
                            Util.redirectToActivity(this, UserProfileActivity.class);
                        },
                        () -> {
                            Toast.makeText(this, "Data modification error.", Toast.LENGTH_SHORT).show();
                        },
                        () -> {
                            Toast.makeText(this, "API error.", Toast.LENGTH_SHORT).show();
                        });
                break;
            }
        }
    }
    private boolean isInputDataValid() {
        changePassword = true;
        if (passwordEditText.getText().toString().isEmpty()) {
            changePassword = false;
        }
        else if (!Util.validatePasswordInputs(this, passwordEditText, passwordRepeatEditText)) {
            return false;
        }

        if (!Util.isValidUsername(usernameEditText.getText().toString())) {
            Toast.makeText(this, "Username must be between 4 and 32 characters.", Toast.LENGTH_SHORT).show();
            return false;
        }

        if (countryEditText.getText().length() < 4 || countryEditText.getText().length() > 32) {
            Toast.makeText(this, "Country must be between 4 and 32 characters.", Toast.LENGTH_SHORT).show();
            return false;
        }

        if (bioEditText.getText().length() > 255) {
            Toast.makeText(this, "Description must be less than 256 characters.", Toast.LENGTH_SHORT).show();
            return false;
        }

        return true;
    }
}