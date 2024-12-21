package com.filmtime.model;

import java.io.Serializable;

public class PreferencesSaveRequest implements Serializable {
    private int[] genre_ids;
    public PreferencesSaveRequest(int[] genre_ids) {
        this.genre_ids = genre_ids;
    }

    public void setGenre_ids(int[] genre_ids) {
        this.genre_ids = genre_ids;
    }

    public int[] getGenre_ids() {
        return genre_ids;
    }
}
