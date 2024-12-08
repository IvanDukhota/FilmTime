<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Page</title>
        <link rel="stylesheet" href="../styles/content_viewer.css">
    </head>
    <body>
    <script>
        document.addEventListener("DOMContentLoaded", async function() {
            const accessToken = localStorage.getItem('access_token');
            let headerFile = 'header.html';

            if(accessToken) {
                try {
                    const response = await fetch('http://localhost:8000/api/v1/registration/user/profile/', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${accessToken}`,
                        },
                    });

                    if (response.ok) {
                        headerFile = 'header_logged_in.html';
                    }
                } catch (error) {
                    console.error('Error fetching user profile:', error);
                }
            }

            fetch(headerFile)
                .then(response => response.text())
                .then(data => {
                    document.getElementById("header").innerHTML = data;
                })
                .catch(error => console.error('Error loading header:', error));
        });
    </script>
    
    <div id="header" class="page_header"></div>

    <div class="container">
        <div class="movie-header">
            <div class="left-section">
                <img src="../styles/images/shutter island.png" alt="Movie Poster" class="movie-poster">

                <button class="play_trailer_button">
                    <img class="img_play_button" src="../styles/images/play.png" alt="Play Image">
                    Play Trailer
                </button>
            </div>

            <div class="movie-details">
                <div class="movie-title">
                    <div class="title"></div>
                    <button class="save-button">
                        <img class="img_save_button" src="../styles/images/bookmark.png" alt="Save Image">
                    </button>
                </div>

                <div class="year"><p><strong>Year:</strong> </p></div>
                <div class="duration"><p><strong>Duration:</strong> </p></div>

                <div class="tags"><strong>Genre:</strong></div>
                <div class="creators"><strong>Creators:</strong></div>
                <div class="cast"><strong>Starring:</strong></div>
                <div class="description"></div>
            </div>
        </div>

        <div class="main-content">
            <div class="video-player">
                <video controls width="100%">
                    <source src="" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>

            <div class="comment-section">
                <div class="comment-input-container">
                    <input type="text" class="comment-input" placeholder="Add a comment...">
                    <button><img class="img_send_button" src="../styles/images/send.png" alt="Send Image"></button>
                </div>

                <div class="comment">
                    <img class="img_account" src="../styles/images/account.png" alt="Account Image">
                    <div class="comment-content">
                        <strong>Nickname</strong>
                        <p>Sample comment text.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <?php include('footer.html'); ?>

    <script>
        document.addEventListener("DOMContentLoaded", async function () {
            let hasRecordedView = false;

            // Watching History
            const recordMovieView = async () => {
                if (!hasRecordedView) {
                    const accessToken = localStorage.getItem("access_token");
                    const contentId = 1; 

                    if (accessToken) {
                        try {
                            const response = await fetch(`http://localhost:8000/api/v1/content/movie/${contentId}/record-view/`, {
                                method: "POST",
                                headers: {
                                    Authorization: `Bearer ${accessToken}`,
                                    "Content-Type": "application/json",
                                },
                            });

                            if (response.ok) {
                                console.log("View recorded successfully.");
                                hasRecordedView = true;
                            } else {
                                console.error("Failed to record view:", response.status);
                            }
                        } catch (error) {
                            console.error("Error recording view:", error);
                        }
                    } else {
                        console.error("Access token not found.");
                    }
                }
            };

            const loadMovieData = async () => {
                try {
                    const response = await fetch("http://localhost:8000/api/v1/content/movie/1/");
                    if (response.ok) {
                        const data = await response.json();

                        document.querySelector(".movie-title .title").textContent = data.title;
                        document.querySelector(".year p").innerHTML = `<strong>Year:</strong> ${new Date(data.release_date).getFullYear()}`;
                        document.querySelector(".duration p").innerHTML = `<strong>Duration:</strong> ${Math.floor(data.movie.duration)}m`;
                        document.querySelector(".description").textContent = data.synopsis || "No description available";

                        const genresContainer = document.querySelector(".tags");
                        genresContainer.innerHTML = `<strong>Genre:</strong>`;
                        data.genres.forEach((genre) => {
                            const genreTag = document.createElement("span");
                            genreTag.classList.add("tag");
                            genreTag.textContent = genre.name;
                            genresContainer.appendChild(genreTag);
                        });

                        const actorsContainer = document.querySelector(".cast");
                        actorsContainer.innerHTML = `<strong>Starring:</strong>`;
                        data.actors.forEach((actor, index) => {
                            const actorSpan = document.createElement("span");
                            actorSpan.classList.add("actor");
                            actorSpan.textContent = actor.name;
                            actorsContainer.appendChild(actorSpan);
                            if (index < data.actors.length - 1) {
                                actorsContainer.innerHTML += ", ";
                            }
                        });

                        const creatorsContainer = document.querySelector(".creators");
                        creatorsContainer.innerHTML = `<strong>Creators:</strong>`;
                        data.directors.forEach((director) => {
                            const directorSpan = document.createElement("span");
                            directorSpan.classList.add("creator");
                            directorSpan.textContent = director.name;
                            creatorsContainer.appendChild(directorSpan);
                        });

                        const videoSource = document.querySelector("video > source");
                        videoSource.src = data.movie.content_url;
                        const videoPlayer = document.querySelector("video");
                        videoPlayer.load();

                   
                        videoPlayer.addEventListener("play", recordMovieView);
                    } else {
                        console.error("Failed to load movie data:", response.status);
                    }
                } catch (error) {
                    console.error("Error fetching movie data:", error);
                }
            };

            await loadHeader();
            await loadMovieData();
        });
    </script>
</body>
</html>
