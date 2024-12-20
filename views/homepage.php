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

            if (accessToken) {
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
                    loadMoviesOnHomepage();
                })
                .catch(error => console.error('Error loading header:', error));
        });

        async function loadMoviesOnHomepage() {
            const movieIds = [1, 2, 3, 4, 6]; 
            const moviesContainer = document.getElementById('moviesContainer');

            let movieItemsHTML = '';

            for (let id of movieIds) {
                const movieData = await fetchMovieData(id);
                if (movieData) {
                    movieItemsHTML += `
                <a href="content_viewer.php?content_id=${id}" class="media_item">
                    <img class="media" src="${movieData.cover_image ? movieData.cover_image : '../styles/images/default_cover.png'}" alt="${movieData.title}">
                    <div class="media_title">${movieData.title}</div>
                </a>
            `;
                } else {
                    movieItemsHTML += `
                <a href="#" class="media_item">
                    <img class="media" src="../styles/images/default_cover.png" alt="No Data">
                    <div class="media_title">No Data</div>
                </a>
            `;
                }
            }

            moviesContainer.innerHTML = movieItemsHTML;
        }

        async function fetchMovieData(id) {
            try {
                const response = await fetch(`http://localhost:8000/api/v1/content/movies/filter/?id=${id}`);

                if (response.ok) {
                    const data = await response.json();

                    if (Array.isArray(data) && data.length > 0) {
                        return {
                            title: data[0].title,
                            cover_image: data[0].cover_image
                        };
                    } else {
                        return null;
                    }
                } else {
                    console.error('Error fetching movie data:', response.statusText);
                    return null;
                }
            } catch (error) {
                console.error('Error fetching movie data:', error);
                return null;
            }
        }
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
                <div class="header-line-row">
                    <div class="header-line"></div>
                </div>
                <a href="movies" class="link_hidden">Movies
                    <img class="arrow_img" src="../styles/images/arrow_white.png" alt="Arrow">
                </a>
            </div>
            <div class="media_list" id="moviesContainer"></div>
        </div>


        <div class="tv_shows">
            <div class="topic-header">
                <div class="header-line-row">
                    <div class="header-line"></div>
                </div>
                <a href="tv_show" class="link_hidden">TV Shows
                    <img class="arrow_img" src="../styles/images/arrow_white.png" alt="Arrow">
                </a>
            </div>
            <div class="media_list">
                <a href="" class="media_item">
                    <img class="media" src="#" alt="Stranger Things">
                    <div class="media_title">Stranger Things</div>
                </a>
                <a href="" class="media_item">
                    <img class="media" src="#" alt="Panic">
                    <div class="media_title">Panic</div>
                </a>
                <a href="" class="media_item">
                    <img class="media" src="#" alt="One Piece">
                    <div class="media_title">One Piece</div>
                </a>
                <a href="" class="media_item">
                    <img class="media" src="#" alt="Bridgerton">
                    <div class="media_title">Bridgerton</div>
                </a>
            </div>
        </div>

        <div class="cartoons">
            <div class="topic-header">
                <div class="header-line-row">
                    <div class="header-line"></div>
                </div>
                <a href="cartoons" class="link_hidden">Cartoons
                    <img class="arrow_img" src="../styles/images/arrow_white.png" alt="Arrow">
                </a>
            </div>
            <div class="media_list">
                <a href="" class="media_item">
                    <img class="media" src="#" alt="Puss in Boots">
                    <div class="media_title">Puss in Boots</div>
                </a>
                <a href="" class="media_item">
                    <img class="media" src="#" alt="Kung Fu Panda">
                    <div class="media_title">Kung Fu Panda</div>
                </a>
                <a href="" class="media_item">
                    <img class="media" src="#" alt="Garfield">
                    <div class="media_title">Garfield</div>
                </a>
                <a href="" class="media_item">
                    <img class="media" src="#" alt="The Simpsons">
                    <div class="media_title">The Simpsons</div>
                </a>
            </div>
        </div>
    </section>

    <?php
    include('footer.html');
    ?>
</body>

</html>