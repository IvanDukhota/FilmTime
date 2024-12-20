<!DOCTYPE html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content searching</title>
    <link rel="stylesheet" href="../styles/content_searching.css">
</head>

<body>
    <script>
        
        let allGenres = [];
        let allActors = [];
        let allDirectors = [];

       
        function filterAndRender(type) {
            let inputElement, dataArray, containerClass;
            if (type === 'genre') {
                
                inputElement = document.querySelector('.genres').parentElement.querySelector('.search-input');
                dataArray = allGenres;
                containerClass = 'genres';
            } else if (type === 'actor') {
                
                inputElement = document.querySelector('.actors-filter .search-input');
                dataArray = allActors;
                containerClass = 'actors';
            } else if (type === 'director') {
               
                inputElement = document.querySelector('.creators-filter .search-input');
                dataArray = allDirectors;
                containerClass = 'creators';
            }

            const query = inputElement.value.trim().toLowerCase();
            let filtered = dataArray;
            if (query) {
                filtered = dataArray.filter(item => item.name.toLowerCase().includes(query));
            }

            const container = document.querySelector(`.${containerClass}`);
            container.innerHTML = filtered.slice(0, 5).map(item => `
            <label><input type="checkbox" value="${item.name}"> ${item.name}</label>
        `).join('');
        }

        function toggleCategory(header) {
            const filterGroup = header.parentElement.parentElement;
            const content = filterGroup.querySelector('.filter-content');
            const arrow = header.querySelector('.arrow_img');

            content.classList.toggle('active');
            if (content.classList.contains('active')) {
                arrow.style.transform = 'rotate(180deg)';
            } else {
                arrow.style.transform = 'rotate(0deg)';
            }
        }

        const MIN_YEAR = 1960;
        const MAX_YEAR = 2024;
        let currentThumb = null;

        function handleYearInputChange(type) {
            const minYearInput = document.getElementById('minYearInput');
            const maxYearInput = document.getElementById('maxYearInput');
            let minVal = parseInt(minYearInput.value);
            let maxVal = parseInt(maxYearInput.value);

            if (type === 'min') {
                if (minVal < MIN_YEAR) minVal = MIN_YEAR;
                if (minVal > maxVal) minVal = maxVal;
                minYearInput.value = minVal;
            } else if (type === 'max') {
                if (maxVal > MAX_YEAR) maxVal = MAX_YEAR;
                if (maxVal < minVal) maxVal = minVal;
                maxYearInput.value = maxVal;
            }

            updateSliderPositions(minVal, maxVal);
        }

        function updateSliderPositions(minVal, maxVal) {
            const sliderLeftThumb = document.getElementById('sliderLeftThumb');
            const sliderRightThumb = document.getElementById('sliderRightThumb');
            const sliderHighlight = document.getElementById('sliderHighlight');
            const minPercent = ((minVal - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)) * 100;
            const maxPercent = ((maxVal - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)) * 100;

            sliderLeftThumb.style.left = `${minPercent}%`;
            sliderRightThumb.style.left = `${maxPercent}%`;
            sliderHighlight.style.marginLeft = `${minPercent}%`;
            sliderHighlight.style.width = `${maxPercent - minPercent}%`;
        }

        function initDrag(type) {
            currentThumb = type;
            document.addEventListener('mousemove', handleDrag);
            document.addEventListener('mouseup', stopDrag);
        }


        function handleDrag(event) {
            const sliderHighlight = document.getElementById('sliderHighlight');
            const sliderRect = sliderHighlight.parentElement.getBoundingClientRect();
            const sliderWidth = sliderRect.width;
            const offsetX = event.clientX - sliderRect.left;

            const percent = Math.min(Math.max((offsetX / sliderWidth) * 100, 0), 100);
            const yearValue = Math.round(MIN_YEAR + (percent / 100) * (MAX_YEAR - MIN_YEAR));

            const minYearInput = document.getElementById('minYearInput');
            const maxYearInput = document.getElementById('maxYearInput');
            if (currentThumb === 'min' && yearValue <= parseInt(maxYearInput.value)) {
                minYearInput.value = yearValue;
                updateSliderPositions(yearValue, parseInt(maxYearInput.value));
            } else if (currentThumb === 'max' && yearValue >= parseInt(minYearInput.value)) {
                maxYearInput.value = yearValue;
                updateSliderPositions(parseInt(minYearInput.value), yearValue);
            }
        }

        function stopDrag() {
            document.removeEventListener('mousemove', handleDrag);
            document.removeEventListener('mouseup', stopDrag);
            currentThumb = null;
        }

        function clearAll() {
            const checkboxes = document.querySelectorAll('.filter-content input[type="checkbox"]');
            checkboxes.forEach(checkbox => checkbox.checked = false);

            const minYearInput = document.getElementById('minYearInput');
            const maxYearInput = document.getElementById('maxYearInput');
            minYearInput.value = MIN_YEAR;
            maxYearInput.value = MAX_YEAR;

            updateSliderPositions(MIN_YEAR, MAX_YEAR);
        }

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
                })
                .catch(error => console.error('Error loading header:', error));

            const searchInput = document.querySelector('.search-input-field');
            const searchButton = document.querySelector('.search_button');
            const mediaList = document.querySelector('.media_list');
            let searchResults = [];

          
            searchInput.addEventListener('input', async function() {
                const query = searchInput.value.trim();
                if (!query) {
                    mediaList.innerHTML = '';
                    searchResults = [];
                    return;
                }

                const url = `http://localhost:8000/api/v1/content/movies/filter/?title=${encodeURIComponent(query)}`;
                try {
                    const response = await fetch(url);
                    if (response.ok) {
                        const data = await response.json();
                        searchResults = data;
                        renderSearchResults(data);
                    } else {
                        console.error('Error fetching search results:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error fetching search results:', error);
                }
            });


            searchButton.addEventListener('click', function() {
                if (searchResults && searchResults.length > 0) {
                    const firstResult = searchResults[0];
                    window.location.href = `content_viewer.php?content_id=${firstResult.id}`;
                } else {
                    alert("No search results found.");
                }
            });

            function renderSearchResults(results) {
                if (results.length === 0) {
                    mediaList.innerHTML = '<div class="empty_results">No results found</div>';
                    return;
                }

                mediaList.innerHTML = `
                <div class="media_list">
                    ${results.map(item => `
                        <div class="media_item" data-id="${item.id}">
                            <img class="media" src="${item.cover_image ? item.cover_image : '../styles/images/default_cover.png'}" alt="${item.title}">
                            <div class="media_title">${item.title}</div>
                        </div>
                    `).join('')}
                </div>
            `;

                const items = mediaList.querySelectorAll('.media_item');
                items.forEach(item => {
                    item.addEventListener('click', () => {
                        const id = item.getAttribute('data-id');
                        window.location.href = `content_viewer.php?content_id=${id}`;
                    });
                });
            }

          
            try {
                const [genresResp, actorsResp, directorsResp] = await Promise.all([
                    fetch('http://localhost:8000/api/v1/content/genres/'),
                    fetch('http://localhost:8000/api/v1/content/actors/'),
                    fetch('http://localhost:8000/api/v1/content/directors/')
                ]);

                if (genresResp.ok) {
                    allGenres = await genresResp.json();
                }
                if (actorsResp.ok) {
                    allActors = await actorsResp.json();
                }
                if (directorsResp.ok) {
                    allDirectors = await directorsResp.json();
                }
            } catch (error) {
                console.error('Error loading filters:', error);
            }

            function renderFilterList(classSelector, dataArray) {
                const container = document.querySelector(`.${classSelector}`);
                if (!container) return;

                container.innerHTML = dataArray.slice(0, 5).map(item => `
                <label><input type="checkbox" value="${item.name}"> ${item.name}</label>
            `).join('');
            }

     
            renderFilterList('genres', allGenres);
            renderFilterList('actors', allActors);
            renderFilterList('creators', allDirectors);

        
            const applyButton = document.querySelector('.apply_button');
            applyButton.addEventListener('click', async function() {
                const minYearInput = document.getElementById('minYearInput');
                const maxYearInput = document.getElementById('maxYearInput');
                const minYear = parseInt(minYearInput.value);
                const maxYear = parseInt(maxYearInput.value);
                const start_year = minYear;
                const end_year = maxYear;
                const selectedGenres = Array.from(document.querySelectorAll('.genres input[type="checkbox"]:checked')).map(i => i.value);
                const selectedActors = Array.from(document.querySelectorAll('.actors input[type="checkbox"]:checked')).map(i => i.value);
                const selectedDirectors = Array.from(document.querySelectorAll('.creators input[type="checkbox"]:checked')).map(i => i.value);

                const ratingCheckboxes = document.querySelectorAll('.ratings input[type="checkbox"]:checked');
                let rating = null;
                if (ratingCheckboxes.length > 0) {
                    rating = Math.max(...Array.from(ratingCheckboxes).map(c => parseInt(c.value)));
                }

                const params = new URLSearchParams();

                if (start_year && end_year) {
                    params.append('start_year', start_year);
                    params.append('end_year', end_year);
                }


                if (rating) {
                    params.append('rating', rating);
                }

                selectedActors.forEach(a => params.append('actors', a));
                console.log(params.data);
                if (selectedDirectors.length > 0) {
                    params.append('director', selectedDirectors[0]);
                }

          
                selectedGenres.forEach(g => params.append('genre', g));

                const url = `http://localhost:8000/api/v1/content/movies/filter/?${params.toString()}`;

                try {
                    const response = await fetch(url);
                    if (response.ok) {
                        const data = await response.json();
                        if (data.length === 0) {
                            mediaList.innerHTML = '<div class="empty_results">No results found</div>';
                        } else {
                            mediaList.innerHTML = `
                            <div class="media_list">
                                ${data.map(item => `
                                    <div class="media_item" data-id="${item.id}">
                                        <img class="media" src="${item.cover_image ? item.cover_image : '../styles/images/default_cover.png'}" alt="${item.title}">
                                        <div class="media_title">${item.title}</div>
                                    </div>
                                `).join('')}
                            </div>
                        `;

                            const items = mediaList.querySelectorAll('.media_item');
                            items.forEach(item => {
                                item.addEventListener('click', () => {
                                    const id = item.getAttribute('data-id');
                                    window.location.href = `content_viewer.php?content_id=${id}`;
                                });
                            });
                        }
                    } else {
                        console.error('Error fetching filtered results:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error fetching filtered results:', error);
                }
            });
        });
    </script>

    <div id="header" class="page_header"></div>


    <div class="hero">
        <div class="filters">
            <div class="filter-group">
                <div class="topic-header">
                    <div class="header-line-row">
                        <div class="header-line"></div>
                    </div>
                    <h3 onclick="toggleCategory(this)">Year
                        <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                    </h3>
                </div>
                <div class="filter-content">
                    <div class="year-range">
                        <input type="number" id="minYearInput" value="1960" min="1960" max="2024" oninput="handleYearInputChange('min')">
                        <input type="number" id="maxYearInput" value="2024" min="1960" max="2024" oninput="handleYearInputChange('max')">
                    </div>
                    <div class="rz-slider-wrapper">
                        <div class="rz-slider">
                            <div class="rz-slider__range-center">
                                <div id="sliderHighlight" class="rz-slider__range-space" style="margin-left: 0%; width: 100%;"></div>
                            </div>
                            <button id="sliderLeftThumb" type="button" class="rz-slider__range-button rz-slider__range-button_type_left" style="left: 0%;" onmousedown="initDrag('min')"></button>
                            <button id="sliderRightThumb" type="button" class="rz-slider__range-button rz-slider__range-button_type_right" style="left: 100%;" onmousedown="initDrag('max')"></button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="filter-group">
                <div class="topic-header">
                    <div class="header-line-row">
                        <div class="header-line"></div>
                    </div>
                    <h3 onclick="toggleCategory(this)">Genre
                        <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                    </h3>
                </div>
                <div class="filter-content">
                    <input type="text" class="search-input" placeholder="Search" oninput="filterAndRender('genre')">
                    <div class="genres"></div>
                </div>
            </div>

            <div class="filter-group">
                <div class="topic-header">
                    <div class="header-line-row">
                        <div class="header-line"></div>
                    </div>
                    <h3 onclick="toggleCategory(this)">Rating
                        <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                    </h3>
                </div>
                <div class="filter-content ratings">
                    <label><input type="checkbox" value="10"> Rating ≥10</label>
                    <label><input type="checkbox" value="9"> Rating ≥9</label>
                    <label><input type="checkbox" value="8"> Rating ≥8</label>
                    <label><input type="checkbox" value="7"> Rating ≥7</label>
                    <label><input type="checkbox" value="6"> Rating ≥6</label>
                    <label><input type="checkbox" value="5"> Rating ≥5</label>
                    <label><input type="checkbox" value="4"> Rating ≥4</label>
                    <label><input type="checkbox" value="3"> Rating ≥3</label>
                    <label><input type="checkbox" value="2"> Rating ≥2</label>
                    <label><input type="checkbox" value="1"> Rating ≥1</label>
                </div>
            </div>

            <div class="filter-group">
                <div class="topic-header">
                    <div class="header-line-row">
                        <div class="header-line"></div>
                    </div>
                    <h3 onclick="toggleCategory(this)">Actor
                        <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                    </h3>
                </div>
                <div class="filter-content actors-filter">
                    <input type="text" class="search-input" placeholder="Search" oninput="filterAndRender('actor')">
                    <div class="actors"></div>
                </div>
            </div>

            <div class="filter-group">
                <div class="topic-header">
                    <div class="header-line-row">
                        <div class="header-line"></div>
                    </div>
                    <h3 onclick="toggleCategory(this)">Creator
                        <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                    </h3>
                </div>
                <div class="filter-content creators-filter">

                    <input type="text" class="search-input" placeholder="Search" oninput="filterAndRender('director')">
                    <div class="creators"></div>
                </div>
            </div>

            <button class="apply_button">Apply</button>
            <button class="clear_button" onclick="clearAll()">Clear all</button>
        </div>
        <div class="movies-container">
            <div class="search-movies">
                <input type="text" class="search-input-field" placeholder="Search for movies or TV shows">
                <button class="search_button"><img class="img_search_button" src="../styles/images/loupe.png" alt="Search">Search</button>
            </div>
            <div class="media_list"></div>
        </div>
    </div>

    <?php
    include('footer.html');
    ?>

    </html>