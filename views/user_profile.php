<?php
    session_start();
    require_once('../models/PermissionCode.php');
    
?>
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
                <div class="user_icon"><img src="../styles/images/account.png" alt="User Icon"></div>
                <div class="profile_info">
                    <div class="profile_name">Nickname</div>
                </div>
                <div class="profile_button">
                    <button class="edit_button"><img class="img_edit_button" src="../styles/images/edit.png" alt="Edit">Edit</button>
                    <button class="logout_button">Log Out</button>
                </div>
            </div>
        </section>

        <section class="content">
            <div class="preferences">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <div class="link_hidden">Preferences</div>
                </div>
                <div class="empty_text">
                    <a href="" class="choose_genre">Choose the genres you like
                        <img class="arrow_img" src="../styles/images/arrow_gray.png" alt="Arrow">
                    </a>
                </div>
            </div>

            <div class="recommendations">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <div class="link_hidden">Recommendations</div>
                </div>
                <div class="empty_text">
                    <a href="" class="choose_genre">Choose the genres you like
                        <img class="arrow_img" src="../styles/images/arrow_gray.png" alt="Arrow">
                    </a>
                </div>
            </div>

            <div class="history">
                <div class="topic-header">
                    <div class="header-line-row"><div class="header-line"></div></div>
                    <div class="link_hidden">History</div>
                </div>
                <div class="empty_text">
                    <div class="empty_history">You haven't watched anything yet</div>
                </div>
            </div>
        </section>

        <?php
        include('footer.html');
        ?>
    </body>
</html>