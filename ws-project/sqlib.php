<?php

$dbname = "liam_stockgame";

?>

<?php

// dbname should be done BEFORE this

$servername = "localhost";
$username = "dbuser";
$password = "password";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

function closeConnection($conn) {
    $conn->close();
}

function execute_sql($conn, $sql) {
    if ($conn->query($sql) !== TRUE) {
        echo "Error with SQL: " . $conn->error;
    }
}

function insert($conn, $table_name, $data) {
    $prep = array();
    foreach($data as $k => $v ) {
        $prep[':'.$k] = "'" . $v . "'";
    }

    $sql = "INSERT INTO $table_name (" . implode(', ',array_keys($data)) . ") VALUES (" . implode(', ',array_values($prep)) . ")";
    echo $sql;

    if ($conn->query($sql) !== TRUE) {
        echo "Error with SQL: " . $conn->error;
    }
}

function getdata($conn, $table_name, $columns = null) {
    $prep = array();
    foreach($columns as $k => $v ) {
        $prep[':'.$k] = "'" . $v . "'";
    }

    if ($columns == null) {
        $columns = "*";
    } else {
        $columns = implode(", ", array_values($prep));
    }

    $result = $conn->query("SELECT ($columns) FROM $table_name");

    if ()
}

?>

<?php

?>