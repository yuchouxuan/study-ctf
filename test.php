<?php

$flag = "flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxx}";
$secret_key = "xxxxxxxxxxxxxxxx"; // the key is safe! no one can know except me

$username = $_POST["username"];
$password = $_POST["password"];
header("hash_key:" . $hash_key);

if (!empty($_COOKIE["getflag"])) {
    if (urldecode($username) === "D0g3" && urldecode($password) != "D0g3") {
        if ($COOKIE["getflag"] === md5($secret_key . urldecode($username . $password))) {
            echo "Great! You're in!\n";
            die ("<!-- The flag is ". $flag . "-->");
        }
        else {
            die ("Go out! Hacker!");
        }
    }
    else {
        die ("LEAVE! You're not one of us!");
    }
}

