<?php

namespace Api\Providers;

use Api\Providers\Utils\Errors;
use Api\Providers\Utils\IProvider;
use Api\Shared\Config;
use Api\Providers\Utils\Database;
use PDO;

abstract class App implements IProvider
{
  private static PDO|false $db = false;
  protected static mixed $data = false;

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

  public static function param(string $name, bool $associative = false): mixed
  {
    if (!self::$data || $associative) {
      self::$data = json_decode(file_get_contents('php://input'), $associative);
    }

    if ($associative) {
      return self::$data[$name] ?: false;
    }

    return self::$data?->$name ?: false;
  }
}