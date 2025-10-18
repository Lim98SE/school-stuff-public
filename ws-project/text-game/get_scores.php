<?php

$dbname = "liam_stockgame";

include("../sqlib.php");

$scores = json_encode(select($conn, "scores", array("name", "score")));

echo $scores;

?>