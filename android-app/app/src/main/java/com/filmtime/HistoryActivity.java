package com.filmtime;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.ContextThemeWrapper;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.helper.widget.Flow;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.ApiStatus;
import com.filmtime.api.UserProfile.HistoryFetchContract;
import com.filmtime.model.ContentResponse;
import com.filmtime.model.UserContentInteraction;
import com.filmtime.model.UserHistoryModel;
import com.filmtime.ui.MenuAdapter;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.squareup.picasso.Picasso;
import com.squareup.picasso.Target;

import java.util.HashMap;

public class HistoryActivity extends AppCompatActivity implements HistoryFetchContract {

    UserHistoryModel userHistoryModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_history);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        userHistoryModel = new UserHistoryModel();
        userHistoryModel.fetchHistory(this, this);

        BottomNavigationView menu = findViewById(R.id.bottomNavigationView);
        menu.setSelectedItemId(R.id.history);
        MenuAdapter.initMenu(this, menu);
    }

    @Override
    public void onHistoryFetchResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                displayHistory(userHistoryModel.getUserInteractions());
                break;
            }
            case FAILURE:
            case RESPONSE_ERR: {
                Toast.makeText(this, "Error: failed to fetch user history.", Toast.LENGTH_SHORT).show();
                break;
            }
        }
    }
    private void displayHistory(UserContentInteraction[] history) {
        LinearLayout layout = findViewById(R.id.history_container);
        if (history == null || history.length == 0) {
            TextView historyView = new TextView(new ContextThemeWrapper(this, R.style.HistoryButtonStyle));
            historyView.setId(View.generateViewId());
            historyView.setText("User history is empty");
            layout.addView(historyView);
        }

        for (UserContentInteraction interaction : history) {
            TextView historyView = new TextView(new ContextThemeWrapper(this, R.style.HistoryButtonStyle));
            historyView.setId(View.generateViewId());
            historyView.setText(interaction.getContent_title());

            Picasso.get().load(interaction.getCover_image()).into(new Target() {
                @Override
                public void onBitmapLoaded(Bitmap bitmap, Picasso.LoadedFrom from) {
                    Drawable drawable = new BitmapDrawable(getResources(), bitmap);
                    drawable.setBounds(0, 0, drawable.getIntrinsicWidth(), drawable.getIntrinsicHeight());
                    historyView.setCompoundDrawables(drawable, null, null, null);
                }

                @Override
                public void onBitmapFailed(Exception e, Drawable errorDrawable) {
                    historyView.setCompoundDrawablesWithIntrinsicBounds(R.drawable.error_icon, 0, 0, 0);
                }

                @Override
                public void onPrepareLoad(Drawable placeHolderDrawable) {
                    historyView.setCompoundDrawablesWithIntrinsicBounds(R.drawable.error_icon, 0, 0, 0);
                }
            });

            historyView.setOnClickListener(v -> {
                Intent intent = new Intent(HistoryActivity.this, ContentPageActivity.class);
                intent.putExtra(ContentResponse.EXTRA_KEY_ID, interaction.getContent_id());
                HistoryActivity.this.startActivity(intent);
            });
            layout.addView(historyView);
        }
    }
}