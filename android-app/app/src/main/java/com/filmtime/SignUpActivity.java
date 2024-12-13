package com.filmtime;

import android.os.Bundle;
import android.util.Log;
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
import com.filmtime.api.RetrofitClient;
import com.filmtime.model.LoginResponse;
import com.filmtime.model.RegisterRequest;
import com.filmtime.util.JwtManager;
import com.filmtime.util.Util;
import com.google.gson.Gson;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SignUpActivity extends AppCompatActivity implements View.OnClickListener {
    private EditText emailEditText;
    private EditText passwordEditText;
    private EditText usernameEditText;
    private EditText passwordRepeatEditText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_sign_up);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        Button loginRedirectBtn = (Button) findViewById(R.id.loginRedirectButton);
        loginRedirectBtn.setOnClickListener(this);
        Button signUpBtn = (Button) findViewById(R.id.signUpButton);
        signUpBtn.setOnClickListener(this);

        usernameEditText = (EditText) findViewById(R.id.usernameSignUpEditText);
        emailEditText = (EditText) findViewById(R.id.emailSignUpEditText);
        passwordEditText = (EditText) findViewById(R.id.passwordSignUpEditText);
        passwordRepeatEditText = (EditText) findViewById(R.id.repeatPasswordSignUpEditText);
    }

    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.loginRedirectButton: {
                Util.redirectToActivity(this, LoginActivity.class);
            }
            case R.id.signUpButton: {
                if (validateSignUpInputs(usernameEditText, emailEditText, passwordEditText, passwordRepeatEditText)) {
                    String email = emailEditText.getText().toString();
                    String password = passwordEditText.getText().toString();
                    String username = usernameEditText.getText().toString();

                    signUp(username, email, password);
                }
                break;
            }
        }
    }

    private boolean validateSignUpInputs(EditText usernameEditText, EditText emailEditText,
                                         EditText passwordEditText, EditText passwordRepeatEditText) {
        if (!Util.isValidEmail(emailEditText.getText())) {
            Toast.makeText(this, "Invalid email.", Toast.LENGTH_SHORT).show();
            return false;
        }
        if (!Util.isValidUsername(usernameEditText.getText().toString())) {
            Toast.makeText(this, "Username must be between 4 and 32 characters.", Toast.LENGTH_SHORT).show();
            return false;
        }
        return Util.validatePasswordInputs(this, passwordEditText, passwordRepeatEditText);
    }

    private void signUp(String username, String email, String password) {
        JwtManager jwtManager = new JwtManager(this);
        ApiService apiService = RetrofitClient.getInstance().create(ApiService.class);

        RegisterRequest request = new RegisterRequest(username, email, password);
        apiService.signUp(request).enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    jwtManager.saveAccessToken(response.body().getAccess());
                    jwtManager.saveRefreshToken(response.body().getRefresh());
                    Toast.makeText(SignUpActivity.this, "Sign up successful", Toast.LENGTH_SHORT).show();
                    Util.redirectToActivity(SignUpActivity.this, UserProfileActivity.class);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                        Log.e("SIGN_UP_ERROR", "Response: " + new Gson().toJson(response.errorBody()));
                    }
                    if (response.code() == 409) {
                        Toast.makeText(SignUpActivity.this, "Username or email already taken", Toast.LENGTH_SHORT).show();
                        passwordEditText.setText("");
                        passwordRepeatEditText.setText("");
                    }
                }
            }

            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                Log.e("API_FAILURE", "Error: " + t.getMessage());
                t.printStackTrace();
                Toast.makeText(SignUpActivity.this, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}