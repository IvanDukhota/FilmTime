<?php
    session_start();
    require_once('../models/PermissionCode.php');
    
?>
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FilmTime - AdminPage</title>
        <link rel="stylesheet" href="../styles/admin_moder_mainpage.css">
    </head>
    <body>
        <?php
            $headerFile = 'header_admin_page.html';
            include($headerFile);
        ?>
        <div class="control_panel">
            <h2>Control panel</h2>
            <a href="moder_manage_page">
                <button>Manage moderators</button>
            </a>
            <a href="user_manage_page">
                <button>Manage users</button>
            </a>
            <a href="comment_manage_page">
                <button>Manage comments</button>
            </a>
        </div>
    </body>
</html>