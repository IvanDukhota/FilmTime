package com.filmtime;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.ContextThemeWrapper;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.activity.EdgeToEdge;
import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.helper.widget.Flow;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.Content.GenresFetchContract;
import com.filmtime.api.UserProfile.PreferencesSaveContract;
import com.filmtime.api.UserProfile.UserProfileEditContract;
import com.filmtime.api.UserProfile.UserProfileFetchContract;
import com.filmtime.model.Genre;
import com.filmtime.model.GenresModel;
import com.filmtime.model.PreferencesModel;
import com.filmtime.model.UserProfileEditRequest;
import com.filmtime.ui.UserProfileDisplay;
import com.filmtime.api.ApiStatus;
import com.filmtime.model.UserProfileModel;
import com.filmtime.util.Util;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class ProfileEditActivity extends AppCompatActivity implements View.OnClickListener,
        UserProfileFetchContract, UserProfileEditContract, GenresFetchContract, PreferencesSaveContract {
    // necessary to determine when to apply user's preferences on collection of buttons
    private boolean needToFetchUserProfile = false;
    private UserProfileModel userProfileModel;
    private GenresModel genresModel;
    private UserProfileDisplay userProfileDisplay;
    private EditText passwordEditText;
    private TextView emailTextView;
    private EditText passwordRepeatEditText;
    private EditText usernameEditText;
    private EditText countryEditText;
    private EditText bioEditText;
    private ImageView pfpImageView;
    private HashMap<Integer, ToggleButton> genreButtons;
    private byte[] pfpImageData;
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
        Button pickImage = (Button) findViewById(R.id.ButtonPfpEdit);
        pickImage.setOnClickListener(this);

        emailTextView = (TextView) findViewById(R.id.emailTextView);
        passwordEditText = (EditText) findViewById(R.id.editTextPassword);
        passwordRepeatEditText = (EditText) findViewById(R.id.editTextRepeatPassword);
        usernameEditText = (EditText) findViewById(R.id.editTextUsername);
        countryEditText = (EditText) findViewById(R.id.editTextCountry);
        bioEditText = (EditText) findViewById(R.id.editTextBio);
        pfpImageView = (ImageView) findViewById(R.id.pfpImageEdit);

        userProfileDisplay = new UserProfileDisplay(usernameEditText, emailTextView,
                bioEditText, countryEditText, pfpImageView);
        userProfileModel = UserProfileModel.fromIntentExtra(getIntent());

        genresModel = new GenresModel();
        genresModel.getGenres(this, this);

        if (userProfileModel.isDataNull()) {
            needToFetchUserProfile = true;
            userProfileModel.fetchUserProfileData(this, this);
        }
        else {
            userProfileDisplay.displayUserProfileData(userProfileModel.getUserProfileData());
        }
    }

    private void createGenreButtons() {
        genreButtons = new HashMap<>();

        ConstraintLayout layout = findViewById(R.id.preferences_wrapper);
        Flow flow = findViewById(R.id.preferences_container);

        for (Genre genre : genresModel.getGenres()) {
            ToggleButton button = new ToggleButton(new ContextThemeWrapper(this, R.style.GenreButtonStyle));
            button.setId(View.generateViewId());

            button.setTextOn(genre.getName());
            button.setTextOff(genre.getName());
            button.setOnCheckedChangeListener(new ToggleButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton button, boolean isChecked) {
                    if (button.isChecked()) {
                        button.setBackgroundResource(R.drawable.toggle_button_on_background);
                        button.setTextColor(getResources().getColor(R.color.black, getTheme()));
                    }
                    else {
                        button.setBackgroundResource(R.drawable.toggle_button_off_background);
                        button.setTextColor(getResources().getColor(R.color.white, getTheme()));
                    }
                }
            });
            button.setChecked(true); // workaround to trigger onCheckedChanged
            button.setChecked(false); //default state
            genreButtons.put(genre.getId(), button);

            layout.addView(button);

            int[] existingIds = flow.getReferencedIds();
            int[] newIds = Arrays.copyOf(existingIds, existingIds.length + 1);
            newIds[newIds.length - 1] = button.getId();
            flow.setReferencedIds(newIds);
        }
    }

    private void setGenreButtons() {
        for(Genre userGenre : userProfileModel.getUserProfileData().getGenres()) {
            ToggleButton btn = genreButtons.get(userGenre.getId());
            btn.setChecked(true);
        }
    }

    @Override
    public void onGenresFetchResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                createGenreButtons();
                if (!needToFetchUserProfile) {
                    setGenreButtons();
                }
                break;
            }
            case FAILURE: {
                Toast.makeText(this, "Failed to retrieve genres.", Toast.LENGTH_SHORT).show();
                break;
            }
            case RESPONSE_ERR: {
                Toast.makeText(this, "API error.", Toast.LENGTH_SHORT).show();
                break;
            }
        }
    }

    @Override
    public void onPreferencesSaveResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                Toast.makeText(this, "Preferences updated", Toast.LENGTH_SHORT).show();
                break;
            }
            case FAILURE: {
                Toast.makeText(this, "Failed to retrieve genres.", Toast.LENGTH_SHORT).show();
                break;
            }
            case RESPONSE_ERR: {
                Toast.makeText(this, "API error.", Toast.LENGTH_SHORT).show();
                break;
            }
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

                PreferencesModel preferencesModel = new PreferencesModel();
                preferencesModel.putUserPreferences(this, this, getSelectedGenreIds());

                if (pfpImageData == null) {
                    pfpImageData = serializeBitmapToBytes(((BitmapDrawable)pfpImageView.getDrawable()).getBitmap());
                }

                UserProfileEditRequest request = new UserProfileEditRequest(usernameEditText.getText().toString(),
                        countryEditText.getText().toString(),
                        bioEditText.getText().toString(),
                        pfpImageData, null);
                if (changePassword)
                    request.setPassword(passwordEditText.getText().toString());

                userProfileModel.editUserProfileData(this, this, request);
                break;
            }
            case R.id.ButtonPfpEdit: {
                Intent intent = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                startActivityForResult(intent, 1);
                break;
            }
        }
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1 && resultCode == RESULT_OK && data != null) {
            Uri imageUri = data.getData();
            try {
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), imageUri);
                pfpImageView.setImageBitmap(bitmap);

                pfpImageData = serializeBitmapToBytes(bitmap);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private byte[] serializeBitmapToBytes(Bitmap bitmap) {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);
        return byteArrayOutputStream.toByteArray();
    }

    private int[] getSelectedGenreIds() {
        ArrayList<Integer> genreIds = new ArrayList<>();
        for (Map.Entry<Integer, ToggleButton> entry : genreButtons.entrySet()) {
            if (entry.getValue().isChecked()) {
                genreIds.add(entry.getKey());
            }
        }

        return genreIds.stream().mapToInt(i -> i).toArray();
    }
    @Override
    public void onUserProfileEditResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                Toast.makeText(this, "Data modified successfully!", Toast.LENGTH_SHORT).show();
                Util.redirectToActivity(this, UserProfileActivity.class);
                finishAndRemoveTask();
                break;
            }
            case FAILURE: {
                Toast.makeText(this, "Data modification error.", Toast.LENGTH_SHORT).show();
                break;
            }
            case RESPONSE_ERR: {
                Toast.makeText(this, "API error.", Toast.LENGTH_SHORT).show();
                break;
            }
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
                    finishAndRemoveTask();
                }
                userProfileDisplay.displayUserProfileData(userProfileModel.getUserProfileData());
                setGenreButtons();
                break;
            }
            case RESPONSE_ERR:
            case FAILURE: {
                finishAndRemoveTask();
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