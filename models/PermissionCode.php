<?php
    enum PermissionCode: int {
        case Guest = 0;
        case User = 1;
        case Moderator = 2;
        case Admin = 3;
    }
?>