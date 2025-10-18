<?php

$dbname = "liam_stockgame";

include("../sqlib.php");

if (null !== $_POST["name"] & null !== $_POST["score"]) {
    insert($conn, "scores", array(
        "score" => $_POST["score"],
        "name" => $_POST["name"]
    ));
}

$previous = "javascript:history.go(-1)";
if(isset($_SERVER['HTTP_REFERER'])) {
    $previous = $_SERVER['HTTP_REFERER'];
}
header("Location: " . $_SERVER["HTTP_REFERER"]);