<?php

namespace Api\Providers\User;

use Api\Objects\Session;
use Api\Providers\App;
use Api\Providers\Utils\Errors;
use Api\Providers\Utils\IProvider;
use Api\Providers\Utils\Response;
use JetBrains\PhpStorm\NoReturn;

class User implements IProvider
{
  public function route($uri_part): void
  {
    match ($uri_part) {
      'update' => Session::access(fn(Session $session) => $this->update($session)),
      default => Errors::create('Метод не найден')
    };
  }

  #[NoReturn]
  private function update(Session $session): void
  {
    $user = $session->getUser();

    $name = App::param('name');
    $surname = App::param('surname');

    if (!empty($name)) {
      $user->setName($name);
    }

    if (!empty($surname)) {
      $user->setSurname($surname);
    }

    Response::set([
      'type' => 'success'
    ]);
  }
}