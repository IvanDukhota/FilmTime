package com.filmtime.util;

import android.content.Context;
import android.content.SharedPreferences;

public class JwtManager {
    private static final String PREF_NAME = "jwt_prefs";
    private static final String KEY_ACCESS_TOKEN = "jwt_access_token";
    private static final String KEY_REFRESH_TOKEN = "jwt_refresh_token";

    private SharedPreferences sharedPreferences;

    public JwtManager(Context context) {
        sharedPreferences = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    public void deleteAccessToken() {
        saveAccessToken(null);
    }
    public void saveAccessToken(String token) {
        saveToken(token, KEY_ACCESS_TOKEN);
    }
    public void deleteRefreshToken() {
        saveRefreshToken(null);
    }
    public void saveRefreshToken(String token) {
        saveToken(token, KEY_REFRESH_TOKEN);
    }
    private void saveToken(String token, String key) {
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(key, token);
        editor.apply();
    }
    public boolean hasAccessToken() {
        String token = getAccessToken();
        return token != null && !token.trim().isEmpty();
    }
    public boolean hasRefreshToken() {
        String token = getRefreshToken();
        return token != null && !token.trim().isEmpty();
    }
    public String getAccessToken() {
        return getToken(KEY_ACCESS_TOKEN);
    }
    public String getRefreshToken() {
        return getToken(KEY_REFRESH_TOKEN);
    }
    private String getToken(String key) {
        return sharedPreferences.getString(key, null);
    }
}