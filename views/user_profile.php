<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Profile</title>
        <link rel="stylesheet" href="../styles/user_profile.css">
    </head>
    <body>
        <?php
            include('header_logged_in.html');
        ?>

        <section class="profile_section">
            <div class="profile_card">
                <div class="user_icon"><img src="" alt="Profile Image" id="profileImage"></div>
                <div class="profile_info">
                    <div class="profile_name"></div>
                    <div class="profile_country"></div>
                    <div class="profile_description"></div>
                </div>
                <div class="profile_button">
                    <button class="edit_button"><img class="img_edit_button" src="../styles/images/edit.png" alt="Edit">Edit</button>
                    <button class="logout_button">Log Out</button>
                </div>
            </div>
        </section>

        <div class="form_overlay hidden" id="editForm">
            <div class="form_container">
                <div class="form_content">
                    <div class="left_section">
                        <div class="profile_image">
                            <img src="../styles/images/account.png" alt="Profile Image" id="profileIcon">
                        </div>
                        <div class="field_wrapper">
                            <button class="upload_button" id="uploadButton">
                                <img class="img_upload_button" src="../styles/images/download.png" alt="Upload Image">
                                Upload new photo
                                <input type="file" accept="image/png, image/jpeg, image/webp" style="display: none;">
                            </button>
                        </div>
                    </div>

                    <div class="right_section">
                        <form>
                            <div class="field_wrapper">
                                <input type="text" name="nickname" class="input_field" placeholder="" id="nickname" required>
                                <label for="nickname" class="label_text">Nickname</label>
                            </div>
    
                            <div class="field_wrapper">
                                <input type="password" name="password" class="input_field" placeholder=" " id="password">
                                <label for="password" class="label_text">Password</label>
                            </div>
                
                            <div class="field_wrapper">
                                <input type="password" name="repeat_password" class="input_field" placeholder=" " id="repeat_password">
                                <label for="repeat_password" class="label_text">Repeat password</label>
                            </div>

                            <div class="field_wrapper">
                                <input type="text" name="country" class="input_field" placeholder="" id="country">
                                <label for="country" class="label_text">Country</label>
                            </div>
                        </form>
                    </div>

                    <div class="bottom_section">
                        <div class="field_wrapper">
                            <textarea name="about" class="input_field" placeholder="" id="about"></textarea>
                            <label for="about" class="label_text">About Me</label>
                        </div>

                        <div class="preferences_list">
                            <div class="genres_label">Preferences</div>
                            <div id="genres" class="genres_container"></div>
                        </div>

                        <div class="form_buttons">
                            <button type="button" id="cancelButton" class="cancel_button">Cancel</button>
                            <button type="submit" class="edit_button">Edit</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <section class="content">
            <div class="preferences">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <div class="link_hidden">Preferences</div>
                </div>
                <div class="empty_text"></div>
            </div>

            <div class="recommendations">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <div class="link_hidden">Recommendations</div>
                </div>
                <div class="empty_text"></div>
            </div>

            <div class="saved">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <a href="javascript:void(0)" class="link_hidden" id="savedToggle">Saved
                        <img class="saved_arrow_img" src="../styles/images/arrow_white.png" alt="Arrow">
                    </a>
                </div>
                <div class="form_overlay hidden" id="savedForm">
                    <div class="form_container">
                        <div class="form_header">
                            <button id="closeSavedForm">
                                <img class="saved_close_img" src="../styles/images/close.png" alt="Close">
                            </button>
                        </div>
                        <div class="saved_list" id="savedList"></div>
                    </div>
                </div>
                <div class="empty_text"></div>
            </div>

            <div class="history">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <div class="link_hidden">History</div>
                </div>
                <div class="empty_text"></div>
            </div>
        </section>

        <?php
        include('footer.html');
        ?>
    </body>
    <script>
    const backendUrl = "http://127.0.0.1:8000";

    const refreshAccessToken = async () => {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            console.error('No refresh token available');
            window.location.href = '/login.php';
            return null;
        }

        try {
            const response = await fetch('http://localhost:8000/api/v1/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: refreshToken
                }),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('access_token', data.access);
                return data.access;
            } else {
                console.error('Error refreshing token:', data);
                window.location.href = '/login.php';
                return null;
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            window.location.href = '/login.php';
        }
    };


    const fetchWithToken = async (url, options = {}) => {
        let accessToken = localStorage.getItem('access_token');

        const fetchData = async () => {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...options.headers,
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            if (response.status === 401) {
                console.log('Access token expired. Refreshing...');
                accessToken = await refreshAccessToken();
                if (!accessToken) return null;

                return fetchWithToken(url, options);
            }

            return response;
        };

        return fetchData();
    };

    document.addEventListener("DOMContentLoaded", function() {
        const editButton = document.querySelector(".edit_button");
        const cancelButton = document.querySelector("#cancelButton");
        const editForm = document.querySelector("#editForm");
        const profileImage = document.querySelector("#profileImage");
        const formImage = document.querySelector("#profileIcon");
        const nicknameInput = document.querySelector("#nickname");
        const countryInput = document.querySelector("#country");
        const aboutInput = document.querySelector("#about");
        const preferencesContainer = document.querySelector(".preferences .empty_text");
        const recommendationsContainer = document.querySelector(".recommendations .empty_text");
        const savedContainer = document.querySelector(".saved .empty_text");
        const historyContainer = document.querySelector(".history .empty_text");
        const savedToggle = document.getElementById("savedToggle");
        const savedForm = document.getElementById("savedForm");
        const closeSavedForm = document.getElementById("closeSavedForm");
        const savedList = document.getElementById("savedList");
        const genresContainer = document.getElementById('genres');
        let userPicture = "../styles/images/account.png";
        let currentNickname = "";
        let currentCountry = '';
        let currentBio = '';
        let userGenres = [];

        const loadUserGenres = async () => {
            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/');
                if(response.ok){
                    const genres = await response.json();
                    preferencesContainer.innerHTML = genres.length > 0
                        ? genres.map(genre => `<span class="tag">${genre.name}</span>`).join('')
                        : '<div class="empty_preferences">Choose the genres you like on the edit form</div>';
                } else {
                    console.error("Error fetching genres:", error);
                }
            } catch (error) {
                console.error('Error fetching genres:', error);
            }
        };

        const loadRecommendations = async () => {
            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/');
                if(response.ok){
                    const recommendations = await response.json();
                    recommendationsContainer.innerHTML = recommendations.length > 0
                        ? renderMediaList(recommendations)
                        : '<div class="empty_recommendations">Choose the genres you like on the edit form</div>';
                } else {
                    console.error("Error fetching recommendations:", error);
                }
            } catch (error) {
                console.error('Error fetching recommendations:', error);
            }
        };

        const loadSaved = async () => {
            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/');
                if(response.ok){
                    const saved = await response.json();
                    savedContainer.innerHTML = saved.length > 0
                        ? renderMediaList(saved)
                        : '<div class="empty_saved">You have not saved anything yet</div>';
                } else {
                    console.error("Error fetching saved movies:", error);
                }
            } catch (error) {
                console.error('Error fetching saved movies:', error);
            }
        };

        const loadHistory = async () => {
            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/');
                if(response.ok){
                    const history = await response.json();
                    historyContainer.innerHTML = history.length > 0
                        ? renderMediaList(history)
                        : '<div class="empty_history">You have not watched anything yet</div>';
                } else {
                    console.error("Error fetching history:", error);
                }
            } catch (error) {
                console.error('Error fetching history:', error);
            }
        };

        const renderMediaList = (mediaItems) => {
            return `
                <div class="media_list">
                    ${mediaItems.map(item => `
                        <a href="content_viewer.php" class="media_item">
                            <img class="media" src="${item.content_picture}" alt="${item.title}">
                            <div class="media_title">${item.title}</div>
                        </a>
                    `).join('')}
                </div>
            `;
        };

        savedToggle.addEventListener("click", async () => {
            savedForm.classList.remove("hidden");
            await loadSavedMovies();
        });

        closeSavedForm.addEventListener("click", () => {
            savedForm.classList.add("hidden");
        });

        async function loadSavedMovies() {
            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/');
                if(response.ok){
                    const savedMovies = await response.json();
                    savedList.innerHTML = savedMovies.length > 0
                        ? savedMovies.map(movie => `
                            <a href="content_viewer.php" class="media_item">
                                <img class="media" src="${movie.content_picture}" alt="${movie.title}">
                                <div class="media_title">${movie.title}</div>
                            </a>
                        `).join('')
                        : '<div class="empty_saved_form">No saved movies yet.</div>';
                } else {
                    console.error("Error fetching saved movies:", error);
                }
            } catch (error) {
                console.error('Error fetching saved movies:', error);
            }
        }

        async function loadAllGenres() {
            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/genres/');
                if(response.ok){
                    const data = await response.json();
                    return data;
                } else {
                    console.error("Error loading genres::", error);
                }
            } catch (error) {
                console.error('Error loading genres::', error);
                return [];
            }
        }

        async function populateGenres() {
            const genres = await loadAllGenres();
            genres.forEach(genre => {
                const tag = document.createElement('span');
                tag.classList.add('tag');
                tag.textContent = genre,name;
                tag.dataset.genre = genre.id;

                if(userGenres.includes(genre.id)){
                    tag.classList.add('selected');
                }
                
                tag.addEventListener('click', () => {
                    tag.classList.toggle('selected');
                });

                genresContainer.appendChild(tag);
            });
        }

        async function loadUserFormGenres() {
            let accessToken = localStorage.getItem('access_token');

            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });

                if (response && response.ok) {
                    const data = await response.json();
                    userGenres = data.genres || [];
                } else {
                    console.error('Error fetching user genres:', data);
                }
            } catch (error) {
                console.error('Error fetching user genres:', error);
            }
        }

        function getSelectedGenres() {
            const selectedTags = document.querySelectorAll('.tag.selected');
            return Array.from(selectedTags).map(tag => tag.dataset.genre);
        }

        async function saveGenres() {
            const selectedGenres = getSelectedGenres();
            const accessToken = localStorage.getItem('access_token');

            try {
                //Можливо потрібно замінити посилання
                const response = await fetchWithToken('http://localhost:8000/api/v1/update-user-genres/', {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                    body: JSON.stringify({genres: selectedGenres}),
                });

                if (response.ok) {
                    console.log('Genres saved successfully');
                } else {
                    console.error('Error saving genres:', data);
                }
            } catch (error) {
                console.error("Error saving genres:", error);
            }
        }

        const fetchUserProfile = async () => {
            let accessToken = localStorage.getItem('access_token');

            try {
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });

                if (response && response.ok) {
                    const data = await response.json();
                    document.querySelector('.profile_name').textContent = data.username;
                    document.querySelector(".profile_country").textContent = data.country;
                    document.querySelector(".profile_description").textContent = data.bio;
                    if (data.profile_picture) {
                        profileImage.src = `${backendUrl}${data.profile_picture}`;
                    } else {
                        profileImage.src = "../styles/images/account.png";
                    }
                } else {
                    console.error('Error fetching user profile:', data);
                }
            } catch (error) {
                console.error('Error fetching user profile:', error);
            }
        };

        editButton.addEventListener("click", async () => {
            editForm.classList.remove("hidden");

            await loadUserFormGenres();
            genresContainer.innerHTML = '';
            populateGenres();

            const accessToken = localStorage.getItem('access_token');

            try {
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });

                if (response && response.ok) {
                    const data = await response.json();
                    currentNickname = data.username || '';
                    nicknameInput.value = currentNickname;
                    currentCountry = data.country || '';
                    countryInput.value = currentCountry;
                    currentBio = data.bio || '';
                    aboutInput.value = currentBio;
                    if (data.profile_picture) {
                        formImage.src = `${backendUrl}${data.profile_picture}`;
                        // Если нужно создавать объект URL из файла изображения:
                        fetch(`${backendUrl}${data.profile_picture}`)
                            .then(res => res.blob())
                            .then(imgBlob => {
                                userPicture = URL.createObjectURL(imgBlob);
                            });
                    } else {
                        formImage.src = "../styles/images/account.png";
                    }
                }
            } catch (error) {
                console.error("Error loading profile:", error);
            }
        });

        const uploadButton = document.querySelector(".upload_button");
        const fileInput = uploadButton.querySelector("input[type='file']");

        uploadButton.addEventListener("click", () => {
            fileInput.click();
        });

        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            clearErrors(uploadField.closest(".field_wrapper"));
            if (file) {
                if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
                    addError(uploadField, "Invalid image format. Use JPG, PNG, or WebP.");
                    formImage.src = userPicture;
                } else if (file.size > 5 * 1024 * 1024) {
                    addError(uploadField, "Image must be less than 5MB.");
                    formImage.src = userPicture;
                } else {
                    formImage.src = URL.createObjectURL(file);
                }
                fileInput.value = "";
            }
        });

        cancelButton.addEventListener("click", () => {
            if (confirm("Changes won't be saved. Are you sure?")) {
                editForm.classList.add("hidden");
            }
        });

        const editUserProfile = async (formData) => {
            const accessToken = localStorage.getItem('access_token');

            try {
                const response = await fetchWithToken('http://localhost:8000/api/v1/user/profile/edit/', {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                    body: formData,
                });

                if (response.ok) {
                    alert("Profile updated successfully!");
                    editForm.classList.add("hidden");
                    await fetchUserProfile();
                } else {
                    console.error('Error updating profile:', data);
                }
            } catch (error) {
                console.error("Error updating profile:", error);
            }
        };

        const nicknameField = document.getElementById("nickname");
        const passwordField = document.getElementById("password");
        const repeatPasswordField = document.getElementById("repeat_password");
        const countryField = document.getElementById("country");
        const aboutField = document.getElementById("about");
        const uploadField = document.getElementById("uploadButton")
        const uploadFileInput = document.querySelector(".upload_button input[type='file']");

        function clearErrors(fieldWrapper) {
            const errorMessages = fieldWrapper.querySelectorAll('.error_message');
            errorMessages.forEach(error => error.remove());
        }

        function addError(inputField, message) {
            const errorItem = document.createElement('p');
            errorItem.classList.add('error_message');
            errorItem.innerText = message;
            inputField.parentNode.appendChild(errorItem);
        }

        editForm.querySelector(".edit_button").addEventListener("click", async function(event) {
            let isValid = true;

            clearErrors(nicknameField.closest(".field_wrapper"));
            if (nicknameField.value.trim().length < 4 || nicknameField.value.trim().length > 32) {
                addError(nicknameField, "Nickname must be between 4 and 32 characters.");
                isValid = false;
            }

            clearErrors(passwordField.closest(".field_wrapper"));
            if (passwordField.value.trim().length > 0 && (passwordField.value.length < 8 || passwordField.value.length > 32)) {
                addError(passwordField, "Password must be between 8 and 32 characters.");
                isValid = false;
            }

            clearErrors(repeatPasswordField.closest(".field_wrapper"));
            if (passwordField.value.trim().length > 0 && repeatPasswordField.value.trim() !== passwordField.value.trim()) {
                addError(repeatPasswordField, "Passwords do not match.");
                isValid = false;
            }

            clearErrors(countryField.closest(".field_wrapper"));
            if (countryField.value.trim().length > 0 && (countryField.value.length < 4 || countryField.value.length > 32)) {
                addError(countryField, "Country must be between 4 and 32 characters.");
                isValid = false;
            }

            clearErrors(aboutField.closest(".field_wrapper"));
            if (aboutField.value.trim().length > 256) {
                addError(aboutField, "Description must be less than 256 characters.");
                isValid = false;
            }

            if (!isValid) return;

            const formData = new FormData();
            if (nicknameInput.value.trim() !== currentNickname) {
                formData.append("username", nicknameInput.value.trim());
            }

            if (!formImage.src.includes("account.png")) {
                const response = await fetch(formImage.src);
                const blob = await response.blob();
                formData.append("profile_picture", blob, "updated_profile_picture.png");
            }

            if (countryInput.value.trim() !== currentCountry) {
                formData.append("country", countryInput.value.trim());
            }

            if (aboutInput.value.trim() !== currentBio) {
                formData.append("bio", aboutInput.value.trim());
            }

            if (passwordField.value.trim().length > 0) {
                formData.append("password", passwordField.value.trim());
            }

            await saveGenres();
            await editUserProfile(formData);
        });

        fetchUserProfile();
        loadUserGenres();
        loadRecommendations();
        loadSaved();
        loadHistory();
    });
</script>
</html>