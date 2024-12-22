package com.filmtime.model;

public class UserContentInteraction {
    private String comment;
    private String comment_date;
    private int content_id;
    private String content_title;
    private String cover_image;
    private Integer episode_progress;
    private int id;
    private String last_watch;
    private Integer movie_progress;
    private String user_name;
    private Integer user_rating;

    public UserContentInteraction(String comment, String comment_date, int content_id, String content_title,
                                  String cover_image, Integer episode_progress, int id, String last_watch,
                                  Integer movie_progress, String user_name, Integer user_rating) {
        this.comment = comment;
        this.comment_date = comment_date;
        this.content_id = content_id;
        this.content_title = content_title;
        this.cover_image = cover_image;
        this.episode_progress = episode_progress;
        this.id = id;
        this.last_watch = last_watch;
        this.movie_progress = movie_progress;
        this.user_name = user_name;
        this.user_rating = user_rating;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public String getComment_date() {
        return comment_date;
    }

    public void setComment_date(String comment_date) {
        this.comment_date = comment_date;
    }

    public int getContent_id() {
        return content_id;
    }

    public void setContent_id(int content_id) {
        this.content_id = content_id;
    }

    public String getContent_title() {
        return content_title;
    }

    public void setContent_title(String content_title) {
        this.content_title = content_title;
    }

    public String getCover_image() {
        return cover_image;
    }

    public void setCover_image(String cover_image) {
        this.cover_image = cover_image;
    }

    public Integer getEpisode_progress() {
        return episode_progress;
    }

    public void setEpisode_progress(Integer episode_progress) {
        this.episode_progress = episode_progress;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getLast_watch() {
        return last_watch;
    }

    public void setLast_watch(String last_watch) {
        this.last_watch = last_watch;
    }

    public Integer getMovie_progress() {
        return movie_progress;
    }

    public void setMovie_progress(Integer movie_progress) {
        this.movie_progress = movie_progress;
    }

    public String getUser_name() {
        return user_name;
    }

    public void setUser_name(String user_name) {
        this.user_name = user_name;
    }

    public Integer getUser_rating() {
        return user_rating;
    }

    public void setUser_rating(Integer user_rating) {
        this.user_rating = user_rating;
    }
}
