package com.filmtime;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.filmtime.api.ApiStatus;
import com.filmtime.api.Content.ContentByIdContract;
import com.filmtime.model.ContentModel;
import com.filmtime.model.ContentResponse;
import com.filmtime.model.Genre;
import com.filmtime.model.UserProfileResponse;
import com.filmtime.ui.MenuAdapter;
import com.filmtime.util.Constants;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.squareup.picasso.Picasso;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.stream.Collectors;

public class ContentPageActivity extends AppCompatActivity implements ContentByIdContract {

    ImageView moviePoster;
    ContentModel contentModel;
    TextView titleTextView;
    TextView yearTextView;
    TextView genresTextView;
    TextView creatorsTextView;
    TextView actorsTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_content_page);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        moviePoster = findViewById(R.id.movie_poster);
        titleTextView = findViewById(R.id.movie_title);
        yearTextView = findViewById(R.id.movie_year);
        genresTextView = findViewById(R.id.movie_genre);
        creatorsTextView = findViewById(R.id.movie_creators);
        actorsTextView = findViewById(R.id.movie_starring);

        contentModel = new ContentModel();

        BottomNavigationView menu = findViewById(R.id.bottomNavigationView);
        menu.setSelectedItemId(R.id.movie);
        MenuAdapter.initMenu(this, menu);

        int contentId = -1;
        try {
            contentId = (int) getIntent().getSerializableExtra(ContentResponse.EXTRA_KEY_ID);
        }
        catch (NullPointerException e) {
            Log.e("CONTENT_EX", "No movie id provided. " + e.getMessage());
        }

        if (contentId != -1) {
            contentModel.fetchContentById(this, contentId);
        }
        else {
            Log.e("CONTENT_EX", "No valid movie id found.");
        }
    }

    public void displayMovie(ContentResponse content) {
        try {
            Picasso.get()
                    .load(content.getCover_image())
                    .placeholder(R.drawable.movie_24)
                    .error(R.drawable.error_icon)
                    .into(moviePoster);
            titleTextView.setText(content.getTitle());
            yearTextView.setText("Year: " + LocalDate.parse(content.getRelease_date()).getYear());
            StringBuilder genres = new StringBuilder();
            for (int i = 0; i < content.getGenres().length - 1; i++) {
                genres.append(content.getGenres()[i].getName());
                genres.append(", ");
            }
            genres.append(content.getGenres()[content.getGenres().length - 1].getName());
            genresTextView.setText("Genres: " + genres.toString());

            StringBuilder actors = new StringBuilder();
            for (int i = 0; i < content.getActors().length - 1; i++) {
                actors.append(content.getActors()[i].getName());
                actors.append(", ");
            }
            actors.append(content.getActors()[content.getActors().length - 1].getName());
            actorsTextView.setText("Starring: " + actors.toString());


            StringBuilder directors = new StringBuilder();
            for (int i = 0; i < content.getDirectors().length - 1; i++) {
                directors.append(content.getDirectors()[i].getName());
                directors.append(", ");
            }
            directors.append(content.getDirectors()[content.getDirectors().length - 1].getName());
            creatorsTextView.setText("Creators: " + directors.toString());
        }
        catch (NullPointerException e) {
            Log.e("CONTENT_EX", e.getMessage());
        }
    }

    @Override
    public void onFetchContentByIdResponse(ApiStatus status) {
        switch (status) {
            case RESPONSE_OK: {
                displayMovie(contentModel.getContentResponse());
                break;
            }
            case FAILURE:
            case RESPONSE_ERR:
                break;
        }
    }
}