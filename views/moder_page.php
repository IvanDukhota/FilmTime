<?php
    session_start();
    require_once('../models/PermissionCode.php');
    
?>
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FilmTime - ModerPage</title>
        <link rel="stylesheet" href="../styles/admin_moder_mainpage.css">
    </head>
    <body>
        <?php
            $headerFile = 'header_moder_page.html';
            include($headerFile);
        ?>
        <div class="control_panel">
            <h2>Control panel</h2>
            <a href="manage_media.php">
                <button>Manage media content</button>
            </a>
            <a href="add_media.php">
                <button>Add media content</button>
            </a>
        </div>
    </body>
</html>