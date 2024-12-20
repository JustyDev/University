<?php

namespace Api\Providers\Utils;

use Api\Providers\Utils\Errors;
use PDO;
use PDOException;

class Database
{
  public static function connection(string $user, string $pass, string $host, string $dbName, $fetchMode = PDO::FETCH_OBJ): PDO|false
  {

    if (!$host || !$pass || !$user || !$dbName) return false;
    try {

      $conn = new PDO("mysql:host=$host;dbname=$dbName;charset=utf8", $user, $pass);
      $conn->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, $fetchMode);
      $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

      return $conn;

    } catch (PDOException $e) {

      Errors::create('Ошибка соединения. Сервис временно недоступен', [
        'additional' => $e->getMessage()
      ]);

      return false;

    }
  }
}