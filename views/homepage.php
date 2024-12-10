<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Homepage</title>
        <link rel="stylesheet" href="../styles/homepage.css">
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

        <section class="hero">
            <div class="hero_content">
                <h1>Unlimited movies, TV shows, cartoons, and more</h1>
                <input type="text" placeholder="Name of the movie or TV show">
                <button class="search_button"><img class="img_search_button" src="../styles/images/loupe.png" alt="Search">Search</button>
            </div>

            <img class="tv_img" src="../styles/images/tv.png" alt="TV">
        </section>

        <section class="content">
            <div class="movies">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <a href="movies" class="link_hidden">Movies
                        <img class="arrow_img" src="../styles/images/arrow_white.png" alt="Arrow">
                    </a>
                </div>
                <div class="media_list"></div>
            </div>

            <div class="tv_shows">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <a href="tv_show" class="link_hidden">TV Shows
                        <img class="arrow_img" src="../styles/images/arrow_white.png" alt="Arrow">
                    </a>
                </div>
                <div class="media_list"></div>
            </div>

            <div class="cartoons">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <a href="cartoons" class="link_hidden">Cartoons
                        <img class="arrow_img" src="../styles/images/arrow_white.png" alt="Arrow">
                    </a>
                </div>
                <div class="media_list"></div>
            </div>
        </section>

        <?php
        include('footer.html');
        ?>
    </body>
    <script>
        const loadContent = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/v1/movie/');
                if (response.ok) {
                    const data = await response.json();

                    const moviesContainer = document.querySelector('.movies .media_list');
                    const tvShowsContainer = document.querySelector('.tv_shows .media_list');
                    const cartoonsContainer = document.querySelector('.cartoons .media_list');

                    const movies = [];
                    const tvShows = [];
                    const cartoons = [];

                    data.forEach((item) => {
                        if(item.content_type === 'movie' && movies.length < 4){
                            movies.push(item);
                        } else if(item.content_type === 'series' && tvShows.length < 4) {
                            tvShows.push(item);
                        } else if(item.content_type === 'animation' && cartoons.length < 4){
                            cartoons.push(item);
                        }
                    });

                    const createMediaItem = (items, container) => {
                        container.innerHTML = "";
                        items.forEach((item) => {
                            const mediaItem = document.createElement('a');
                            mediaItem.href = `content_viewer.html?id=${item.id}`;
                            mediaItem.classList.add('media_item');

                            const mediaImage = document.createElement('img');
                            mediaImage.src = item.cover_image || '';
                            mediaImage.alt = item.title || 'No title';
                            mediaImage.classList.add('media');

                            const mediaTitle = document.createElement('div');
                            mediaTitle.textContent = item.title || 'No title';
                            mediaTitle.classList.add('media_title');

                            mediaItem.appendChild(mediaImage);
                            mediaItem.appendChild(mediaTitle);
                            container.appendChild(mediaItem);
                        });
                    };

                    createMediaItem(movies, moviesContainer);
                    createMediaItem(tvShows, tvShowsContainer);
                    createMediaItem(cartoons, cartoonsContainer);
                } else {
                    console.error('Failed to load content:', response.status);
                }
            } catch (error) {
                console.error('Error fetching content:', error);
            }
        };

        document.addEventListener('DOMContentLoaded', loadContent);

    </script>
</html>