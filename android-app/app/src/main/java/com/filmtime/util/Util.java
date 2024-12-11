package com.filmtime.util;

import android.content.Intent;
import androidx.appcompat.app.AppCompatActivity;

public class Util {
    public static void redirectToActivity(AppCompatActivity from, Class to) {
        Intent myIntent = new Intent(from, to);
        from.startActivity(myIntent);
    }
}
