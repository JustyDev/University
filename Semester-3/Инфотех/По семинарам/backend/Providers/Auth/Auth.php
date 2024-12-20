<?php

namespace Api\Providers\Auth;

use Api\Objects\User;
use Api\Providers\App;
use Api\Providers\Utils\Errors;
use Api\Providers\Utils\IProvider;
use Api\Providers\Utils\Response;
use JetBrains\PhpStorm\NoReturn;

class Auth implements IProvider
{
  public function route($uri_part): void
  {
    match ($uri_part) {
      'login' => $this->login(),
      'register' => $this->register(),
      default => Errors::create('Метод не найден')
    };
  }

  #[NoReturn]
  private function register(): void
  {
    $email = App::param('email');
    $password = App::param('password');
    $confirm_password = App::param('confirm_password');
    if (empty($email) || empty($password) || empty($confirm_password)) Errors::create('Все поля должны быть заполненны');

    if ($password !== $confirm_password) Errors::create('Пароли не совпадают');

    if (User::findByEmail($email)) Errors::create('Пользователь с таким Email уже существует');

    $created_user = User::create($email, $password);
    if (!$created_user) Errors::create('Пользователь не был создан');

    Response::set([
      'type' => 'success',
      'session' => $created_user->getSession()
    ]);
  }

  #[NoReturn]
  private function login(): void
  {
    $email = App::param('email');
    $password = App::param('password');
    if (empty($email) || empty($password)) Errors::create('Введите пароль и ник');

    $user = User::findByEmail($email);
    if (!$user || !$user->areValidPassword($password)) {
      Errors::create('Неправильный email или пароль');
    }

    Response::set([
      'type' => 'success',
      'session' => $user->getSession()
    ]);
  }
}