package com.filmtime;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.ApiService;
import com.filmtime.api.AuthInterceptor;
import com.filmtime.api.RetrofitClient;
import com.filmtime.model.UserProfileResponse;
import com.filmtime.util.JwtManager;
import com.filmtime.util.Util;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
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
    }
    private void loginWithStoredToken() {
        JwtManager jwtManager = new JwtManager(this);
        if (!jwtManager.hasAccessToken() && !jwtManager.hasRefreshToken()) {
            Util.redirectToActivity(this, LoginActivity.class);
            return;
        }

        ApiService apiService = RetrofitClient.getInstance(new AuthInterceptor(this)).create(ApiService.class);
        apiService.getUserProfile().enqueue(new Callback<UserProfileResponse>() {
            @Override
            public void onResponse(Call<UserProfileResponse> call, Response<UserProfileResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    Log.i("AUTH_RESPONSE", "Login with token successful.");
                    Intent intent = new Intent(MainActivity.this, UserProfileActivity.class);
                    intent.putExtra(UserProfileResponse.EXTRA_KEY, response.body());
                    MainActivity.this.startActivity(intent);
                } else {
                    Log.e("API_ERROR", "Error code: " + response.code());
                    if (response.errorBody() != null) {
                        Log.e("API_ERROR", "Error: " + response.errorBody());
                    }
                    Log.i("AUTH_RESPONSE", "Login with token failed.");
                    Util.redirectToActivity(MainActivity.this, LoginActivity.class);
                }
            }

            @Override
            public void onFailure(Call<UserProfileResponse> call, Throwable t) {
                Log.e("API_FAILURE", "Error: " + t.getMessage());
                Util.redirectToActivity(MainActivity.this, LoginActivity.class);
            }
        });
    }
}