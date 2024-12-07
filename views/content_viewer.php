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
document.addEventListener("DOMContentLoaded", async function () {
    const accessToken = localStorage.getItem("access_token");
    let headerFile = "header.html";

    
    if (accessToken) {
        try {
            const response = await fetch("http://localhost:8000/api/v1/user/profile/", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            });

            if (response.ok) {
                headerFile = "header_logged_in.html";
            }
        } catch (error) {
            console.error("Error fetching user profile:", error);
        }
    }

    
    fetch(headerFile)
        .then((response) => response.text())
        .then((data) => {
            document.getElementById("header").innerHTML = data;
        })
        .catch((error) => console.error("Error loading header:", error));

  
    try {
        let response = await fetch("http://localhost:8000/api/v1/movie/1/");
        if (response.ok) {
            let data = await response.json();

          
            document.querySelector(".movie-title .title").textContent = data.title;
            document.querySelector(".year p").innerHTML = `<strong>Year:</strong> ${new Date(data.release_date).getFullYear()}`;
            document.querySelector(".duration p").innerHTML = `<strong>Duration:</strong> ${Math.floor(data.details.duration_seconds )}m`;
            document.querySelector(".description").textContent = data.details.synopsis || "No description available";

      
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
            videoSource.src = data.trailer_url || data.url; 
            const videoPlayer = document.querySelector("video");
            videoPlayer.load();
        } else {
            console.error("Ошибка загрузки данных фильма:", response.status);
        }
    } catch (error) {
        console.error("Error fetching movie data:", error);
    }
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

                    <div class="tags">
                        <strong>Genre:</strong>
                        <span class="tag"></span>
                        <span class="tag"></span>
                        <span class="tag"></span>
                        <span class="tag"></span>
                        <span class="tag"></span>
                    </div>

                    <div class="creators">
                        <strong>Creators:</strong>
                       <span class="creator"></span>
                    </div>

                    <div class="cast">
                        <strong>Starring:</strong>
                        <span class="actor"></span>,
                        <span class="actor"></span>,
                        <span class="actor"></span>,
                        <span class="actor"></span>,
                        <span class="actor"></span>,
                        <span class="actor"></span>,
                        <span class="actor"></span>,
                        <span class="actor"></span>,
                        <span class="actor"></span>
                    </div>

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
                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                        </div>
                    </div>
    
                    <div class="comment">
                        <img class="img_account" src="../styles/images/account.png" alt="Account Image">
                        <div class="comment-content">
                            <strong>Nickname</strong>
                            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <?php
        include('footer.html');
        ?>
    </body>
</html>
