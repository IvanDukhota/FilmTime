<!DOCTYPE html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content searching</title>
    <link rel="stylesheet" href="../styles/content_searching.css">
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

    <div class="hero">
    <div class="filters">
        <div class="filter-group">
            <div class="topic-header">
                <div class="header-line-row"><div class="header-line"></div></div>
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
                <div class="header-line-row"><div class="header-line"></div></div>
                <h3 onclick="toggleCategory(this)">Genre
                    <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                </h3>
            </div>
            <div class="filter-content">
                <input type="text" class="search-input" placeholder="Search" oninput="filterGenres(this, 'genres')">
                <div class="genres">
                    <label><input type="checkbox" unchecked> Adventure</label>
                    <label><input type="checkbox" unchecked> Comedy</label>
                    <label><input type="checkbox" unchecked> Drama</label>
                    <label><input type="checkbox" unchecked> Historical</label>
                </div>
            </div>
        </div>
        <div class="filter-group">
            <div class="topic-header">
                <div class="header-line-row"><div class="header-line"></div></div>
                <h3 onclick="toggleCategory(this)">Rating
                    <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                </h3>
            </div>
            <div class="filter-content">
                <label><input type="checkbox" unchecked> ★★★★★ and more</label>
                <label><input type="checkbox" unchecked> ★★★★☆ and more</label>
                <label><input type="checkbox" unchecked> ★★★☆☆ and more</label>
                <label><input type="checkbox" unchecked> ★★☆☆☆ and more</label>
                <label><input type="checkbox" unchecked> ★☆☆☆☆ and more</label>
            </div>
        </div>
        <div class="filter-group">
            <div class="topic-header">
                <div class="header-line-row"><div class="header-line"></div></div>
                <h3 onclick="toggleCategory(this)">Actor
                    <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                </h3>
            </div>
            <div class="filter-content">
                <input type="text" class="search-input" placeholder="Search" oninput="filterActor(this, 'actors')">
                <div class="actors">
                    <label><input type="checkbox" unchecked> Winona Ryder</label>
                    <label><input type="checkbox" unchecked> David Harbour</label>
                    <label><input type="checkbox" unchecked> Millie Bobby Brown</label>
                    <label><input type="checkbox" unchecked> Joe Keery</label>
                </div>
            </div>
        </div>
        <div class="filter-group">
            <div class="topic-header">
                <div class="header-line-row"><div class="header-line"></div></div>
                <h3 onclick="toggleCategory(this)">Creator
                    <img class="arrow_img" src="../styles/images/down-arrow.png" alt="Arrow">
                </h3>
            </div>
            <div class="filter-content">
                <input type="text" class="search-input" placeholder="Search" oninput="filterCreator(this, 'creators')">
                <div class="creators">
                    <label><input type="checkbox" unchecked> Ross Duffer</label>
                    <label><input type="checkbox" unchecked> Matt Duffer</label>
                    <label><input type="checkbox" unchecked> Paul Dichter</label>
                    <label><input type="checkbox" unchecked> Kate Trefry</label>
                </div>
            </div>
        </div>
        <button class="apply_button">Apply</button>
        <button class="clear_button" onclick="clearAll()">Clear all</button>
    </div>
    <div class="movies-container">
        <div class="search-movies">
            <input type="text" placeholder="Search for movies or TV shows">
            <button class="search_button"><img class="img_search_button" src="../styles/images/loupe.png" alt="Search">Search</button>
        </div>
        <div class="media_list"></div>
    </div>
    </div>

    <?php
    include('footer.html');
    ?>
</body>
<script>
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

    const minYearInput = document.getElementById('minYearInput');
    const maxYearInput = document.getElementById('maxYearInput');
    const sliderLeftThumb = document.getElementById('sliderLeftThumb');
    const sliderRightThumb = document.getElementById('sliderRightThumb');
    const sliderHighlight = document.getElementById('sliderHighlight');
    const MIN_YEAR = 1960;
    const MAX_YEAR = 2024;

    function handleYearInputChange(type) {
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
        const minPercent = ((minVal - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)) * 100;
        const maxPercent = ((maxVal - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)) * 100;

        sliderLeftThumb.style.left = `${minPercent}%`;
        sliderRightThumb.style.left = `${maxPercent}%`;
        sliderHighlight.style.marginLeft = `${minPercent}%`;
        sliderHighlight.style.width = `${maxPercent - minPercent}%`;
    }

    let currentThumb = null;

    function initDrag(type) {
        currentThumb = type;
        document.addEventListener('mousemove', handleDrag);
        document.addEventListener('mouseup', stopDrag);
    }

    function handleDrag(event) {
        const sliderRect = sliderHighlight.parentElement.getBoundingClientRect();
        const sliderWidth = sliderRect.width;
        const offsetX = event.clientX - sliderRect.left;

        const percent = Math.min(Math.max((offsetX / sliderWidth) * 100, 0), 100);
        const yearValue = Math.round(MIN_YEAR + (percent / 100) * (MAX_YEAR - MIN_YEAR));

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


    function filterGenres(input, className) {
        const filter = input.value.toLowerCase();
        const items = document.querySelectorAll(`.${className} label`);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(filter) ? '' : 'none';
        });
    }

    function filterActor(input, className) {
        const filter = input.value.toLowerCase();
        const items = document.querySelectorAll(`.${className} label`);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(filter) ? '' : 'none';
        });
    }

    function filterCreator(input, className) {
        const filter = input.value.toLowerCase();
        const items = document.querySelectorAll(`.${className} label`);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(filter) ? '' : 'none';
        });
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
</script>
</html>
