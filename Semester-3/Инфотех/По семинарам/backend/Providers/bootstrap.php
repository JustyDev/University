<?php

namespace Api\Providers;

require __DIR__ . '/../vendor/autoload.php';

use Api\Providers\Auth\Auth;
use Api\Providers\Common\Common;
use Api\Providers\User\User;
use Api\Providers\Utils\Errors;
use Api\Providers\Utils\IProvider;
use Api\Providers\Utils\UPath;
use Api\Providers\Utils\Utils;

error_reporting(E_ALL);

register_shutdown_function(function () {
  $error = error_get_last();
  if (is_array($error) && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
    Errors::cleanOb();
    Errors::create('Сервис временно недоступен', [
      'info' => $error
    ]);
  }
});

class Entry
{
  public function __construct()
  {
    $this->headers();
    $high = UPath::separate(0);

    $provider = match ($high) {
      'auth' => new Auth(),
      'common' => new Common(),
      'user' => new User(),
      default => false
    };

    if (!($provider instanceof IProvider)) Errors::create('Метод не найден');

    $provider->route(UPath::separate(1));
  }

  private function headers(): void
  {
    /*
     * CORS Headers
     */

    Utils::setHeader('Access-Control-Allow-Origin', $_SERVER['HTTP_ORIGIN'] ?: '*');
    Utils::setHeader('Access-Control-Allow-Credentials', 'true');
    Utils::setHeader('Access-Control-Max-Age', '3600');
    Utils::setHeader('Access-Control-Expose-Headers', 'Content-Type, Authorization, API');
    Utils::setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, API, X-Dev-Auth, AccessToken');
    Utils::setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');

    /*
     * Security Headers
     * */

    Utils::setHeader('X-Frame-Options', 'DENY');
    Utils::setHeader('X-XSS-Protection', '1; mode=block');
    Utils::setHeader('X-Content-Type-Options', 'nosniff');
    Utils::setHeader('Server', 'Overland/1.0');

    /*
     * Misc Headers
     */

    Utils::setHeader('Content-Type', 'application/json; charset=UTF-8');
    Utils::setHeader('X-Robots-Tag', 'noindex, nofollow');
  }
}

new Entry();