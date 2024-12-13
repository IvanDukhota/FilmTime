package com.filmtime.util;

import android.content.Context;
import android.content.Intent;
import android.text.TextUtils;
import android.util.Patterns;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class Util {
    private final static int PWD_MIN_LENGTH = 8;
    private final static int PWD_MAX_LENGTH = 32;
    private final static int USERNAME_MIN_LENGTH = 4;
    private final static int USERNAME_MAX_LENGTH = 32;

    public static void redirectToActivity(AppCompatActivity from, Class to) {
        Intent myIntent = new Intent(from, to);
        from.startActivity(myIntent);
    }

    public static boolean isValidEmail(CharSequence target) {
        return (!TextUtils.isEmpty(target) && Patterns.EMAIL_ADDRESS.matcher(target).matches());
    }

    public static boolean isValidUsername(String username) {
        return username.length() >= USERNAME_MIN_LENGTH && username.length() <= USERNAME_MAX_LENGTH;
    }

    public static boolean validatePasswordInputs(Context context, EditText passwordEditText,
                                                 EditText passwordRepeatEditText) {
        String password = passwordEditText.getText().toString();
        String passwordRepeat = passwordRepeatEditText.getText().toString();
        if (!password.equals(passwordRepeat)) {
            passwordRepeatEditText.setText("");
            Toast.makeText(context, "Passwords don't match!", Toast.LENGTH_SHORT).show();
            return false;
        }

        if (!Util.isValidPassword(password)) {
            passwordRepeatEditText.setText("");
            Toast.makeText(context,
                    String.format("Password must be between %d and %d characters.", PWD_MIN_LENGTH, PWD_MAX_LENGTH),
                    Toast.LENGTH_SHORT).show();
            return false;
        }

        return true;
    }

    private static boolean isValidPassword(String password) {
        return password.length() >= PWD_MIN_LENGTH && password.length() <= PWD_MAX_LENGTH;
    }
}
