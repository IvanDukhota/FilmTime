<?php
    session_start();
    require_once('../models/PermissionCode.php');
    
?>
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Homepage</title>
        <link rel="stylesheet" href="../styles/homepage.css">
    </head>
    <body>
        <?php
            $headerFile = 'header.html';
            if(isset($_SESSION['permission']) && $_SESSION['permission'] == PermissionCode::User->value) {
                $headerFile = 'header-logged-in.html';
            }
            include($headerFile);
        ?>

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
                <div class="media_list">
                    <a href="" class="media_item">
                        <img class="media" src="../styles/images/The_hunger_game.jpg" alt="The Hunger Games">
                        <div class="media_title">The Hunger Games: The Ballad of Songbirds & Snakes</div>
                    </a>
                    <a href="" class="media_item">
                        <img class="media" src="../styles/images/Harry_potter.jpg" alt="Harry Potter">
                        <div class="media_title">Harry Potter and the Philosopher's Stone</div>
                    </a>
                    <a href="" class="media_item">
                        <img class="media" src="../styles/images/Pirates_of_the_caribbean.jpg" alt="Pirates of the Caribbean">
                        <div class="media_title">Pirates of the Caribbean: The Curse of the Black Pearl</div>
                    </a>
                    <a href="" class="media_item">
                        <img class="media" src="../styles/images/Fear_street.jpg" alt="Fear Street">
                        <div class="media_title">Fear Street Part One: 1994</div>
                    </a>
                </div>
            </div>

            <div class="tv_shows">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
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
                    <div class="header-line-row"><div class="header-line"></div></div>
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