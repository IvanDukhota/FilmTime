package com.filmtime.model;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

public class UserProfileEditRequest implements Serializable {
    private String password;
    private String username;
    private String country;
    private String bio;
    private byte[] profile_picture;
    public UserProfileEditRequest(String username, String country, String bio,
                               byte[] profilePicture, String password) {
        this.username = username;
        this.country = country;
        this.bio = bio;
        this.profile_picture = profilePicture;
        this.password = password;
    }
    private void writeObject(ObjectOutputStream oos) throws IOException {
        oos.defaultWriteObject();
        oos.writeInt(profile_picture.length);
        oos.write(profile_picture);
    }

    private void readObject(ObjectInputStream ois) throws ClassNotFoundException, IOException {
        ois.defaultReadObject();
        int length = ois.readInt();
        profile_picture = new byte[length];
        ois.readFully(profile_picture);
    }
    public void setUsername(String username) {
        this.username = username;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public void setBio(String bio) {
        this.bio = bio;
    }

    public void setProfilePicture(byte[] profilePicture) {
        this.profile_picture = profilePicture;
    }

    public String getUsername() {
        return username;
    }

    public String getCountry() {
        return country;
    }

    public String getBio() {
        return bio;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public byte[] getProfilePicture() {
        return profile_picture;
    }
}
