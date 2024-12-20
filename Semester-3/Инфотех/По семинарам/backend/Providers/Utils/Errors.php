<?php

namespace Api\Providers\Utils;

use Exception;

use function ob_get_level;
use function ob_end_clean;
use function json_encode;

final class Errors
{
  public static function setCode(int|false $code): void
  {
    if (!$code) return;
    http_response_code($code);
  }

  public static function cleanOb(): void
  {
    while (ob_get_level()) {
      ob_end_clean();
    }
  }

  public static function create(string $message, array $attach = []): void
  {
    try {
      echo json_encode([
        'error' => [
          'message' => $message,
          'attachments' => (object)$attach
        ]
      ]);

      exit;
    } catch (Exception $fatalError) {
      echo json_encode([
        'error' => [
          'message' => $fatalError->getMessage(),
          'attachments' => (object)[]
        ]
      ]);
    }
  }
}
