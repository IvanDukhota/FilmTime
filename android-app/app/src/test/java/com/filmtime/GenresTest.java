package com.filmtime;

import org.junit.Test;

import static org.junit.Assert.*;

import com.filmtime.model.Genre;
import com.google.gson.Gson;

public class GenresTest {
    @Test
    public void serializesGenres() {
        Genre[] genres = {
                new Genre(1, "genre1"),
                new Genre(2, "genre2"),
                new Genre(3, "genre3"),
        };
        Gson gson = new Gson();
        String json = gson.toJson(genres);
        String expectedJson= "[{\"name\":\"genre1\",\"id\":1}," +
                "{\"name\":\"genre2\",\"id\":2}," +
                "{\"name\":\"genre3\",\"id\":3}]";
        assertEquals(json, expectedJson);
    }
    @Test
    public void deserializesGenres() {
        Genre[] genres = {
                new Genre(1, "genre1"),
                new Genre(2, "genre2"),
                new Genre(3, "genre3"),
        };
        String json = "[{\"id\":1,\"name\":\"genre1\"}," +
                "{\"id\":2,\"name\":\"genre2\"}," +
                "{\"id\":3,\"name\":\"genre3\"}]";

        Gson gson = new Gson();
        Genre[] actualGenres = gson.fromJson(json, Genre[].class);
        for (int i = 0; i < genres.length; i++) {
            assertEquals(genres[i].getId(), actualGenres[i].getId());
            assertEquals(genres[i].getName(), actualGenres[i].getName());
        }
    }
}