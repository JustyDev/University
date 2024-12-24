<?php

namespace Api\Objects;

use Api\Providers\App;
use Api\Providers\Utils\Utils;

class User
{
  public int $id;
  public string $password;
  public string $email;
  public int $register_time;
  public string $register_ip;

  public static function findById(?int $user_id): ?User
  {
    if (!$user_id) return null;
    $sgs = App::conn()->prepare('SELECT * FROM `users` WHERE `id` = ? LIMIT 1');
    $sgs->execute([$user_id]);

    return $sgs->fetchObject('\Api\Objects\User') ?: null;
  }

  public static function findByEmail(?string $email): ?User
  {
    if (!$email) return null;
    $sgs = App::conn()->prepare('SELECT * FROM `users` WHERE email = ? LIMIT 1');
    $sgs->execute([$email]);

    return $sgs->fetchObject('\Api\Objects\User') ?: null;
  }

  public function getId(): int
  {
    return $this->id;
  }

  public function getPassword(): string
  {
    return $this->password;
  }

  public function getEmail(): string
  {
    return $this->email;
  }

  public function getRegisterTime(): int
  {
    return $this->register_time;
  }

  public function getRegisterIP(): int
  {
    return $this->register_ip;
  }

  public function getSession(): array
  {
    return [
      'id' => $this->getId(),
      'email' => $this->getEmail(),
    ];
  }

  public function areValidPassword(string $password): bool
  {
    return password_verify($password, $this->getPassword());
  }

  public static function create(?string $email, ?string $password): ?User
  {
    if (!$email || !$password) return null;

    $hash = password_hash($password, PASSWORD_DEFAULT);

    App::conn()
      ->prepare('INSERT INTO `users` (`email`, `password`, `register_time`, `register_ip`) VALUES (?, ?, ?, ?)')
      ->execute([$email, $hash, time(), Utils::userIp()]);

    return User::findById(App::conn()->lastInsertId());
  }
}