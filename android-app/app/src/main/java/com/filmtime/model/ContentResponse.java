package com.filmtime.model;

public class ContentResponse {
    public static final String EXTRA_KEY_ID = "content_id";
    Actor[] actors;
    Director[] directors;
    String cover_image;
    Genre[] genres;
    int id;
    String release_date;
    String title;

    public ContentResponse(Actor[] actors, Director[] directors, String cover_image, Genre[] genres,
                           int id, String release_date, String title) {
        this.actors = actors;
        this.directors = directors;
        this.cover_image = cover_image;
        this.genres = genres;
        this.id = id;
        this.release_date = release_date;
        this.title = title;
    }

    public Actor[] getActors() {
        return actors;
    }

    public void setActors(Actor[] actors) {
        this.actors = actors;
    }

    public Director[] getDirectors() {
        return directors;
    }

    public void setDirectors(Director[] directors) {
        this.directors = directors;
    }

    public String getCover_image() {
        return cover_image;
    }

    public void setCover_image(String cover_image) {
        this.cover_image = cover_image;
    }

    public Genre[] getGenres() {
        return genres;
    }

    public void setGenres(Genre[] genres) {
        this.genres = genres;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getRelease_date() {
        return release_date;
    }

    public void setRelease_date(String release_date) {
        this.release_date = release_date;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }
}
