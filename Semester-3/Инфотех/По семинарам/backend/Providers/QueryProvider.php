<?php

namespace Api\Providers;

use Api\Providers\Utils\Errors;
use Api\Providers\Utils\IProvider;
use Api\Utils\Database;
use PDO;

abstract class QueryProvider implements IProvider
{
  private static PDO|false $db = false;

  public static function getMethod(): string
  {
    return strtoupper(trim($_SERVER['REQUEST_METHOD']));
  }

  public static function createConnection(): void
  {

    $database = new Database();

    $connection = $database->connection(Config::DB_USER, Config::DB_PASS, Config::DB_HOST, Config::DB_NAME);

    if (!$connection) {
      Errors::create('Ошибка соединения. Сервис временно недоступен');
    }

    self::$db = $connection;

  }

  public static function conn(): PDO
  {
    if (!self::$db) self::createConnection();
    return self::$db;
  }
}