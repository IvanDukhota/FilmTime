CREATE DATABASE FilmTime;
\c "FilmTime";

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(32) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(10) CHECK (role IN ('user', 'admin', 'moderator')) NOT NULL
);

CREATE TABLE UserProfiles (
    user_profile_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    username VARCHAR(32) UNIQUE NOT NULL,
    profile_picture BYTEA,
    country VARCHAR(100),
    bio TEXT,
    status VARCHAR(10) CHECK (status IN ('active', 'banned')) NOT NULL
);

CREATE TABLE Content (
    content_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE,
    content_type VARCHAR(20) CHECK (content_type IN ('Movie', 'Series', 'Animation')) NOT NULL,
    trailer_url VARCHAR(255),
    rating FLOAT
);

CREATE TABLE Genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE ContentGenres (
    content_genre_id SERIAL PRIMARY KEY,
    content_id INT REFERENCES Content(content_id) ON DELETE CASCADE ON UPDATE CASCADE,
    genre_id INT REFERENCES Genres(genre_id) ON DELETE CASCADE ON UPDATE CASCADE,
);

CREATE TABLE Actors (
    actor_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Directors (
    director_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE ContentActors (
    content_actor_id SERIAL PRIMARY KEY,
    content_id INT REFERENCES Content(content_id) ON DELETE CASCADE ON UPDATE CASCADE,
    actor_id INT REFERENCES Actors(actor_id) ON DELETE CASCADE ON UPDATE CASCADE,
    character_name VARCHAR(255),
);

CREATE TABLE ContentDirectors (
    content_actor_id SERIAL PRIMARY KEY,
    content_id INT REFERENCES Content(content_id) ON DELETE CASCADE ON UPDATE CASCADE,
    director_id INT REFERENCES Directors(director_id) ON DELETE CASCADE ON UPDATE CASCADE,
);

CREATE TABLE SubscriptionPlans (
    subscription_plan_id SERIAL PRIMARY KEY,
    plan_name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    content_access_level VARCHAR(50) NOT NULL
);

CREATE TABLE UserSubscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    subscription_plan_id INT REFERENCES SubscriptionPlans(subscription_plan_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE UserPreferredGenres (
    user_preference_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    genre_id INT REFERENCES Genres(genre_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ContentHistory (
    history_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    content_id INT REFERENCES Content(content_id) ON DELETE CASCADE ON UPDATE CASCADE,
    watch_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paused_at_second INT
);

CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    content_id INT REFERENCES Content(content_id) ON DELETE CASCADE ON UPDATE CASCADE,
    rating FLOAT CHECK (rating >= 0 AND rating <= 10),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE UserLists (
    list_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    list_name VARCHAR(255) NOT NULL
);

CREATE TABLE ListItems (
    list_item_id SERIAL PRIMARY KEY,
    list_id INT REFERENCES UserLists(list_id) ON DELETE CASCADE ON UPDATE CASCADE,
    content_id INT REFERENCES Content(content_id) ON DELETE CASCADE ON UPDATE CASCADE,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    content_id INT REFERENCES Content(content_id) ON DELETE SET NULL ON UPDATE CASCADE,
    message TEXT NOT NULL,
    date_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);

CREATE TABLE ContentDetails (
    content_details_id SERIAL PRIMARY KEY,
    content_id INT REFERENCES Content(content_id) ON DELETE CASCADE ON UPDATE CASCADE,
    synopsis TEXT,
    duration_seconds INT,
    content_rating VARCHAR(10)
);

CREATE INDEX idx_user_email ON Users(email);
CREATE INDEX idx_content_title ON Content(title);
CREATE INDEX idx_genre_name ON Genres(name);
CREATE INDEX idx_actor_name ON Actors(name);
CREATE INDEX idx_director_name ON Directors(name);
