<?php

namespace Api\Providers\Common;

use Api\Objects\Session;
use Api\Providers\Utils\Errors;
use Api\Providers\Utils\IProvider;
use Api\Providers\Utils\Response;
use JetBrains\PhpStorm\NoReturn;

class Common implements IProvider
{
  public function route($uri_part): void
  {
    match ($uri_part) {
      'initial' => $this->initial(),
      default => Errors::create('Метод не найден')
    };
  }

  #[NoReturn]
  private function initial(): void
  {
    $token = $_COOKIE['AccessToken'] ?? null;
    $session = Session::findByKey($token);

    $user = $session?->getUser();

    Response::set([
      'session' => $session ? [
        'id' => $session->getId(),
        'user' => [
          'id' => $user->getId(),
          'email' => $user->getEmail(),
        ]
      ] : null
    ]);
  }
}