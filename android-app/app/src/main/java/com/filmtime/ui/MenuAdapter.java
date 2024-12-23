package com.filmtime.ui;

import androidx.appcompat.app.AppCompatActivity;

import com.filmtime.HistoryActivity;
import com.filmtime.MainActivity;
import com.filmtime.R;
import com.filmtime.UserProfileActivity;
import com.filmtime.util.Util;
import com.google.android.material.bottomnavigation.BottomNavigationView;

abstract public class MenuAdapter {
    private final static int MOVIE = R.id.movie;
    private final static int HISTORY = R.id.history;
    private final static int USER_PROFILE = R.id.user_profile;
    public static void initMenu(AppCompatActivity activity, BottomNavigationView menu) {
        menu.setOnItemSelectedListener(item -> {
            switch (item.getItemId()) {
                case MOVIE: {
                    Util.redirectToActivity(activity, MainActivity.class);
                    break;
                }
                case HISTORY: {
                    Util.redirectToActivity(activity, HistoryActivity.class);
                    break;
                }
                case USER_PROFILE: {
                    Util.redirectToActivity(activity, UserProfileActivity.class);
                    break;
                }
            }
            return true;
        });
        menu.setOnItemReselectedListener(item -> {
            return;
        });
    }
}
