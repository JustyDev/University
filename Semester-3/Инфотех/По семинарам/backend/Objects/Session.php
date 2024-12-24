<?php

namespace Api\Objects;

use Api\Providers\App;
use Api\Providers\Utils\Errors;
use Api\Providers\Utils\Utils;

class Session
{
  public int $id;
  public int $user_id;
  public string $key;
  public int $create_time;
  public string $create_ip;

  public function getId(): int
  {
    return $this->id;
  }

  public function getUserId(): int
  {
    return $this->user_id;
  }

  public function getUser(): User
  {
    return User::findById($this->getUserId());
  }

  public function getKey(): string
  {
    return $this->key;
  }

  public function toCookie(): void
  {
    Utils::useCookie('AccessToken', $this->getKey(), 2592000);
  }

  public function remove(): void
  {
    App::conn()
      ->prepare('DELETE FROM `sessions` WHERE `id` = ? LIMIT 1')
      ->execute([$this->getId()]);

    Utils::deleteCookie('AccessToken');
  }

  public static function access(callable $method)
  {
    $token = $_COOKIE['AccessToken'] ?? null;
    $session = self::findByKey($token);

    if (!$session) {
      Utils::deleteCookie('AccessToken');
      Errors::create('Сессия устарела, войдите в аккаунт снова');
    }

    return $method($session);
  }

  public static function findById(?int $user_id): ?Session
  {
    if (!$user_id) return null;
    $sgs = App::conn()->prepare('SELECT * FROM `sessions` WHERE `id` = ? LIMIT 1');
    $sgs->execute([$user_id]);

    return $sgs->fetchObject('\Api\Objects\Session') ?: null;
  }

  public static function findByKey(?string $key): ?Session
  {
    if (!$key) return null;
    $sgs = App::conn()->prepare('SELECT * FROM `sessions` WHERE `key` = ? LIMIT 1');
    $sgs->execute([$key]);

    return $sgs->fetchObject('\Api\Objects\Session') ?: null;
  }

  public static function create(?int $user_id): ?Session
  {
    if (!$user_id) return null;

    $key = Utils::genDefectedString(48);

    App::conn()
      ->prepare('INSERT INTO `sessions` (`user_id`, `create_time`, `create_ip`, `key`) VALUES (?, ?, ?, ?)')
      ->execute([$user_id, time(), Utils::userIp(), $key]);

    return Session::findById(App::conn()->lastInsertId());
  }
}