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
import com.filmtime.model.LoginRequest;
import com.filmtime.model.LoginResponse;
import com.filmtime.util.JwtManager;
import com.filmtime.util.Util;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity implements View.OnClickListener {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_login);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        Button loginButton = (Button) findViewById(R.id.buttonLogin);
        loginButton.setOnClickListener(this);

        Button loginFacebookButton = (Button) findViewById(R.id.buttonLoginFacebook);
        loginFacebookButton.setOnClickListener(this);

        Button loginGoogleButton = (Button) findViewById(R.id.buttonLoginGoogle);
        loginGoogleButton.setOnClickListener(this);
    }

    public void onClick(View v) {
        switch (v.getId()) {
            case  R.id.buttonLogin: {
                EditText emailEditText = (EditText) findViewById(R.id.editTextTextEmailAddress);
                EditText passwordEditText = (EditText) findViewById(R.id.editTextTextPassword);
                login(emailEditText.getText().toString(), passwordEditText.getText().toString());
                break;
            }

            case R.id.buttonLoginFacebook: {
                //todo: do something
                break;
            }

            case R.id.buttonLoginGoogle: {
                //todo: do something
                break;
            }
        }
    }
    private void login(String email, String password) {
        JwtManager jwtManager = new JwtManager(this);
        ApiService apiService = RetrofitClient.getInstance().create(ApiService.class);

        LoginRequest request = new LoginRequest(email, password);
        apiService.login(request).enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    jwtManager.saveAccessToken(response.body().getAccess());
                    jwtManager.saveRefreshToken(response.body().getRefresh());
                    Toast.makeText(LoginActivity.this, "Login successful", Toast.LENGTH_SHORT).show();
                    Util.redirectToActivity(LoginActivity.this, UserProfileActivity.class);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    Toast.makeText(LoginActivity.this, "Login failed", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                Toast.makeText(LoginActivity.this, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}