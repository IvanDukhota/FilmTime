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

            const savedForm = document.getElementById("savedForm");
            const createListForm = document.getElementById("createListForm");
            const closeSavedForm = document.getElementById("closeSavedForm");
            const createListButton = document.getElementById("createListButton");
            const cancelCreateList = document.getElementById("cancelCreateList");
            const createListSubmit = document.getElementById("createListSubmit");
            const savedButton = document.querySelector(".save-button");
            const savedListContainer = document.getElementById("savedList");

            savedButton.addEventListener("click", () => {
                savedForm.classList.remove("hidden");
                loadSavedLists();
            });

            closeSavedForm.addEventListener("click", () => {
                savedForm.classList.add("hidden");
            });
            createListButton.addEventListener("click", () => {
                createListForm.classList.remove("hidden");
            });

            cancelCreateList.addEventListener("click", () => {
                createListForm.classList.add("hidden");
            });

            createListSubmit.addEventListener("click", async () => {
                const listName = document.getElementById("listName").value.trim();
                if (listName) {
                    try {
                        const response = await fetch("http://localhost:8000/api/v1/content-list/", {
                            method: "POST",
                            headers: {
                                Authorization: `Bearer ${accessToken}`,
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                name: listName
                            }),
                        });

                        if (response.ok) {
                            alert("List created successfully!");
                            createListForm.classList.add("hidden");
                            loadSavedLists();
                        } else {
                            console.error('Error creating list:', error);
                        }
                    } catch (error) {
                        console.error('Error creating list:', error);
                    }
                } else {
                    alert("Please enter a valid list name.")
                }
            });

            async function loadSavedLists() {
                const savedListContainer = document.getElementById("savedList");
                try {
                    const response = await fetch("http://localhost:8000/api/v1/content/content-list/", {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${accessToken}`,
                            "Content-Type": "application/json",
                        },
                    });

                    if (response.ok) {
                        const lists = await response.json();
                        savedListContainer.innerHTML = lists.length > 0 ?
                            lists.map((list) => `
                    <div class="list_item" data-id="${list.id}">
                        <img class="list_img" src="../styles/images/open-folder.png" alt="List">
                        ${list.list_name}
                    </div>`).join("") :
                            '<div class="empty_saved_form">No created lists yet.</div>';

                        // Add event listener to each list item
                        document.querySelectorAll('.list_item').forEach(item => {
                            item.addEventListener('click', function() {
                                const listId = item.dataset.id;
                                const url = new URL(window.location.href);
                                const movieId = url.searchParams.get('content_id');
                                // Call the function to add content (movie) to the list
                                addContentToList(listId, movieId); // `movieId` should be the movie you want to add
                            });
                        });

                    } else {
                        console.error('Error loading lists:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error loading lists:', error);
                }
            }

            // Function to add movie to selected list
            async function addContentToList(listId, movieId) {
                let accessToken = localStorage.getItem('access_token');
                const url = 'http://localhost:8000/api/v1/content/content-list/content/'; // Your API endpoint

                try {
                    const response = await fetch(url, {
                        method: "POST",
                        headers: {
                            "Authorization": `Bearer ${accessToken}`,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            list_id: listId,
                            content_id: movieId, // The movie ID that you want to add
                        }),
                    });

                    if (response.ok) {
                        const result = await response.json();
                        console.log("Content added successfully:", result);
                    } else {
                        console.error('Error adding content to list:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error adding content to list:', error);
                }
            }


            savedListContainer.addEventListener("click", async (event) => {
                const clickedElement = event.target.closest(".list_item");
                if (clickedElement) {
                    const listId = clickedElement.getAttribute("data-id");
                    const urlParams = new URLSearchParams(window.location.search);
                    const movieId = urlParams.get("id");

                    if (movieId && listId) {
                        try {
                            const accessToken = localStorage.getItem("access_token");
                            const response = await fetch("http://localhost:8000/api/v1/content/content-list/", {
                                method: "POST",
                                headers: {
                                    Authorization: `Bearer ${accessToken}`,
                                    "Content-Type": "application/json",
                                },
                                body: JSON.stringify({
                                    'list_id': listId,
                                    'content_id': movieId,
                                }),

                            });


                            if (response.ok) {
                                alert("Movie successfully added to the list!");
                            } else {
                                const errorData = await response.json();
                                console.error("Error adding movie to list:", errorData);
                            }
                        } catch (error) {
                            console.error("Error during request:", error);
                        }
                    }
                }
            });


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
                })
                .catch(error => console.error('Error loading header:', error));
        });
    </script>

    <div id="header" class="page_header"></div>

    <div class="container">
        <div class="movie-header">
            <div class="left-section">
                <img src="../styles/images/default-poster.png" alt="Movie Poster" class="movie-poster" id="movie-poster">

                <button class="play_trailer_button" id="play-trailer-button">
                    <img class="img_play_button" src="../styles/images/play.png" alt="Play Image">
                    Play Trailer
                </button>
            </div>


            <div class="movie-details">
                <div class="movie-title">
                    <div class="title" id="movie-title"></div>
                    <button class="save-button" id="save-button">
                        <img class="img_save_button" src="../styles/images/bookmark.png" alt="Save Image">
                    </button>
                </div>

                <div class="year">
                    <p><strong>Year:</strong> <span id="movie-year"></span></p>
                </div>
                <div class="duration">
                    <p><strong>Duration:</strong> <span id="movie-duration"></span>m</p>
                </div>

                <div class="tags"><strong>Genre:</strong> <span id="movie-genres"></span></div>
                <div class="creators"><strong>Creators:</strong> <span id="movie-creators"></span></div>
                <div class="cast"><strong>Starring:</strong> <span id="movie-actors"></span></div>
                <div class="description" id="movie-description"></div>
            </div>
        </div>

        <div class="main-content">
            <div class="video-player">
                <video controls width="100%" id="trailer-video">
                    <source src="" type="video/mp4" id="trailer-source">
                    Your browser does not support the video tag.
                </video>
            </div>

            <div class="line"></div>

            <div class="movie-rating">
                <h3>Please rate your impressions after watching:</h3>
                <div class="stars" data-rating="0">
                    <span class="star" data-value="1">&#9734;</span>
                    <span class="star" data-value="2">&#9734;</span>
                    <span class="star" data-value="3">&#9734;</span>
                    <span class="star" data-value="4">&#9734;</span>
                    <span class="star" data-value="5">&#9734;</span>
                </div>
            </div>

            <div class="line"></div>


            <h3>Share your thoughts after watching:</h3>
            <div class="comment-section">
                <div class="comment-input-container">
                    <input type="text" class="comment-input" placeholder="Add a comment..." maxlength="500">
                    <button id="submit-comment"><img class="img_send_button" src="../styles/images/send.png" alt="Send Image"></button>
                </div>
            </div>

            <div class="line"></div>


            <h3>View comments:</h3>
            <div class="comment">
                <div id="comments-container">

                </div>
            </div>
        </div>
    </div>

    <div class="form_overlay hidden" id="savedForm">
        <div class="form_container">
            <div class="form_header">
                <button class="create_list_button" id="createListButton">
                    <img class="create_list_img" src="../styles/images/add.png" alt="CreateList">
                    Create a new list
                </button>
                <button id="closeSavedForm">
                    <img class="saved_close_img" src="../styles/images/close.png" alt="Close">
                </button>
            </div>
            <div class="saved_list" id="savedList"></div>
        </div>
    </div>
    </div>

    <div class="form_overlay hidden" id="createListForm">
        <div class="form_container">
            <div class="form_header">
                <h3>Create a New List</h3>
            </div>
            <div class="field_wrapper">
                <input type="text" name="listName" class="input_field" placeholder="" id="listName" required>
                <label for="listName" class="label_text">List name</label>
            </div>
            <div class="form_footer">
                <button id="cancelCreateList">Cancel</button>
                <button id="createListSubmit">Create</button>
            </div>
        </div>
    </div>


    <?php include('footer.html'); ?>



    <script>
        document.addEventListener("DOMContentLoaded", async function() {

            const urlParams = new URLSearchParams(window.location.search);
            const contentId = urlParams.get('content_id');



            if (!contentId) {
                console.error("Content ID not specified.");
                alert("No content specified.");

                return;
            }

            let hasRecordedView = false;

            function escapeHTML(str) {
                var div = document.createElement('div');
                div.appendChild(document.createTextNode(str));
                return div.innerHTML;
            }

            const recordMovieView = async () => {
                if (!hasRecordedView) {
                    const accessToken = localStorage.getItem("access_token");

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
                                console.log("Просмотр успешно записан.");
                                hasRecordedView = true;
                            } else {
                                console.error("Не удалось записать просмотр:", response.status);
                            }
                        } catch (error) {
                            console.error("Ошибка при записи просмотра:", error);
                        }
                    } else {
                        console.error("Токен доступа не найден.");
                    }
                }
            };


            const loadMovieData = async () => {
                try {
                    const response = await fetch(`http://localhost:8000/api/v1/content/movie/${contentId}/`);
                    if (response.ok) {
                        const data = await response.json();
                        console.log("Movie Data:", data);


                        const moviePoster = document.getElementById("movie-poster");
                        console.log("Movie Poster Element:", moviePoster);

                        if (data.cover_image) {
                            console.log("Setting movie poster src to:", data.cover_image);
                            moviePoster.src = data.cover_image;
                            moviePoster.alt = `${data.title} Poster`;
                        } else {
                            console.log("No cover_image found, using default poster.");
                            moviePoster.src = "../styles/images/default-poster.png";
                            moviePoster.alt = "Default Movie Poster";
                        }


                        document.getElementById("movie-title").textContent = data.title;
                        document.getElementById("movie-year").textContent = new Date(data.release_date).getFullYear();
                        document.getElementById("movie-duration").textContent = Math.floor(data.movie.duration);
                        document.getElementById("movie-description").textContent = data.synopsis || "No description available";

                        const genresContainer = document.getElementById("movie-genres");
                        genresContainer.innerHTML = data.genres.map(genre => `<span class="tag">${genre.name}</span>`).join(", ");

                        const actorsContainer = document.getElementById("movie-actors");
                        actorsContainer.innerHTML = data.actors.map(actor => `<span class="actor">${actor.name}</span>`).join(", ");


                        const creatorsContainer = document.getElementById("movie-creators");
                        creatorsContainer.innerHTML = data.directors.map(director => `<span class="creator">${director.name}</span>`).join(", ");

                        const videoSource = document.getElementById("trailer-source");
                        videoSource.src = data.trailer_url;
                        const videoPlayer = document.getElementById("trailer-video");
                        videoPlayer.load();

                        videoPlayer.addEventListener("play", recordMovieView);
                    } else {
                        console.error("Не удалось загрузить данные фильма:", response.statusText);
                        alert("Failed to load movie data.");
                    }
                } catch (error) {
                    console.error("Ошибка при получении данных фильма:", error);
                    alert("An error occurred while fetching movie data.");
                }
            };


            const handleRating = () => {
                const stars = document.querySelectorAll(".stars .star");
                const starsContainer = document.querySelector(".stars");

                fetchUserRating();

                stars.forEach((star) => {
                    star.addEventListener("mouseover", () => {
                        const value = parseFloat(star.getAttribute("data-value"));
                        highlightStars(value);
                    });

                    star.addEventListener("mouseout", () => {
                        const currentRating = parseFloat(starsContainer.getAttribute("data-rating"));
                        highlightStars(currentRating);
                    });

                    star.addEventListener("click", () => {
                        const value = parseFloat(star.getAttribute("data-value"));
                        starsContainer.setAttribute("data-rating", value);
                        highlightStars(value);


                        const rating = parseFloat(starsContainer.getAttribute("data-rating"));


                        if (rating >= 1 && rating <= 5) {
                            fetch('http://localhost:8000/api/v1/user/submit-rating/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                                    },
                                    body: JSON.stringify({
                                        user_rating: rating,
                                        content_id: contentId
                                    }),
                                })
                                .then((response) => {
                                    if (!response.ok) {
                                        throw new Error('Network response was not ok');
                                    }
                                    return response.json();
                                })
                                .then((data) => {
                                    console.log('Рейтинг успешно отправлен:', data);

                                    alert('Ваш рейтинг успешно сохранён!');
                                })
                                .catch((error) => {
                                    console.error('Ошибка при отправке рейтинга:', error);
                                    alert('Произошла ошибка при сохранении рейтинга.');
                                });
                        } else {
                            alert('Пожалуйста, выберите рейтинг от 1 до 5 звезд.');
                        }
                    });
                });

                function highlightStars(value) {
                    stars.forEach((star) => {
                        if (parseFloat(star.getAttribute("data-value")) <= value) {
                            star.classList.add("filled");
                        } else {
                            star.classList.remove("filled");
                        }
                    });
                }

                async function fetchUserRating() {
                    try {
                        const response = await fetch(`http://localhost:8000/api/v1/user/get-user-rating/?content_id=${contentId}`, {
                            method: 'GET',
                            headers: {
                                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                                'Content-Type': 'application/json',
                            },
                        });

                        if (response.ok) {
                            const data = await response.json();
                            if (data && data.user_rating) {
                                starsContainer.setAttribute("data-rating", data.user_rating);
                                highlightStars(data.user_rating);
                            }
                        } else if (response.status === 404) {
                            console.log("Рейтинг ещё не выставлен пользователем.");
                        } else {
                            console.error("Не удалось получить рейтинг:", response.statusText);
                        }
                    } catch (error) {
                        console.error("Ошибка при получении рейтинга:", error);
                    }
                }
            };


            const fetchComments = async () => {
                try {
                    const response = await fetch(`http://localhost:8000/api/v1/user/get-comments/?content_id=${contentId}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });
                    if (response.ok) {
                        const data = await response.json();
                        const commentsContainer = document.getElementById('comments-container');
                        commentsContainer.innerHTML = '';

                        if (data.length === 0) {
                            commentsContainer.innerHTML = '<p>No comments yet. Be the first to comment!</p>';
                            return;
                        }

                        data.forEach(comment => {
                            const commentBlock = document.createElement('div');
                            commentBlock.classList.add('comment-content');

                            commentBlock.innerHTML = `
                                <div class="comment-content">
                                    <strong>${escapeHTML(comment.user_name)}</strong>
                                    <p>${escapeHTML(comment.comment)}</p>
                                    <span class="comment-date">${new Date(comment.comment_date).toLocaleString()}</span>
                                </div>
                            `;

                            commentsContainer.appendChild(commentBlock);
                        });
                    } else {
                        console.error('Не удалось получить комментарии:', response.statusText);
                    }
                } catch (error) {
                    console.error('Ошибка при получении комментариев:', error);
                }
            };

            const handleComments = () => {
                const submitButton = document.getElementById("submit-comment");
                const commentInput = document.querySelector(".comment-input");
                const commentsContainer = document.getElementById('comments-container');

                submitButton.addEventListener("click", (e) => {
                    e.preventDefault();
                    const comment = commentInput.value.trim();

                    if (comment !== "") {
                        fetch('http://localhost:8000/api/v1/user/submit-comment/', {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                                },
                                body: JSON.stringify({
                                    comment: comment,
                                    content_id: contentId
                                }),
                            })
                            .then((response) => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                if (response.status === 204) {
                                    return {};
                                } else {
                                    return response.json();
                                }
                            })
                            .then((data) => {
                                console.log('Комментарий успешно отправлен:', data);
                                commentInput.value = '';
                                fetchComments();
                                alert('Ваш комментарий успешно отправлен!');
                            })
                            .catch((error) => {
                                console.error('Ошибка при отправке комментария:', error);
                                alert('Произошла ошибка при отправке комментария.');
                            });
                    } else {
                        alert('Пожалуйста, напишите комментарий перед отправкой.');
                    }
                });


            };

            const initialize = async () => {
                await loadMovieData();
                handleRating();
                handleComments();
                fetchComments();
            };

            initialize();
        });
    </script>
</body>

</html>