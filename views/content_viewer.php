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
                        const response = await fetch('http://<?php echo getenv('SERVER_ADDRESS'); ?>/api/v1/user/profile/', {
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
                    <img src="../styles/images/Stranger_things.jpg" alt="Movie Poster" class="movie-poster">

                    <button class="play_trailer_button">
                        <img class="img_play_button" src="../styles/images/play.png" alt="Play Image">
                        Play Trailer
                    </button>
                </div> 

                <div class="movie-details">
                    <div class="movie-title">
                        <div class="title">Stranger Things</div>
                        <button class="save-button">
                            <img class="img_save_button" src="../styles/images/bookmark.png" alt="Save Image">
                        </button>
                    </div>

                    <div class="year"><p><strong>Year:</strong> 2016</p></div>
                    <div class="duration"><p><strong>Duration:</strong> 1h</p></div>

                    <div class="tags">
                        <strong>Genre:</strong>
                        <span class="tag">Drama</span>
                        <span class="tag">Fantasy</span>
                        <span class="tag">Sci-Fi</span>
                        <span class="tag">Horror</span>
                        <span class="tag">Mystery</span>
                    </div>

                    <div class="creators">
                        <strong>Creators:</strong>
                       <span class="creator">The Duffer Brothers</span>
                    </div>

                    <div class="cast">
                        <strong>Starring:</strong>
                        <span class="actor">Winona Ryder</span>,
                        <span class="actor">David Harbour</span>,
                        <span class="actor">Millie Bobby Brown</span>,
                        <span class="actor">Finn Wolfhard</span>,
                        <span class="actor">Gaten Matarazzo</span>,
                        <span class="actor">Caleb McLaughlin</span>,
                        <span class="actor">Natalia Dyer</span>,
                        <span class="actor">Charlie Heaton</span>,
                        <span class="actor">Noah Schnapp</span>
                    </div>

                    <div class="description">
                        When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces, and one strange little girl.
                    </div>
                </div>
            </div>

            <div class="main-content">
                <div class="video-controls">
                    <div class="field_wrapper">
                        <select class="dropdown" id="season">
                            <option value="1">Season 1</option>
                            <option value="2">Season 2</option>
                        </select>
                        <label for="season" class="label_text">Season</label>
                    </div>
    
                    <div class="field_wrapper">
                        <select class="dropdown" id="episode">
                            <option value="1">Episode 1</option>
                            <option value="2">Episode 2</option>
                        </select>
                        <label for="episode" class="label_text">Episode</label>
                    </div>
                </div>
    
                <div class="video-player">
                    <video controls width="100%">
                        <source src="../styles/images/Бітлджус Бітлджус.mp4" type="video/mp4">
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
