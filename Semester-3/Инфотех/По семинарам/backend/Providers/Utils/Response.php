<?php

namespace Api\Providers\Utils;

use JetBrains\PhpStorm\NoReturn;

class Response
{
  #[NoReturn] public static function set(array $data, bool $isClean = false): void
  {

    echo json_encode($isClean ? $data : [
      'response' => $data
    ]);

    exit;
  }

  #[NoReturn] public static function html(string $data): void
  {

    Utils::setHeader('Content-Type', 'text/html');

    echo $data;

    exit;
  }
}