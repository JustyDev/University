<?php

namespace Api\Providers\Utils;

class UPath
{
  public static function join(...$paths): string
  {
    return implode(DIRECTORY_SEPARATOR, $paths);
  }

  public static function multiExplode(array $delimiters, string $string): array
  {
    $ready = str_replace($delimiters, $delimiters[0], $string);
    return explode($delimiters[0], $ready);
  }

  public static function separate(int $level = -1): string|array
  {
    $request_uri = $_SERVER['REQUEST_URI'];
    if (str_starts_with($request_uri, "/")) {
      $request_uri = substr($request_uri, 1);
    }
    $url = explode("?", $request_uri)[0];
    $exploded = UPath::multiExplode(['.', '/'], $url);

    if ($level >= 0) return $exploded[$level];
    return $exploded;
  }
}