<?php

namespace Api\Providers\Utils;

class Utils
{
  public static function setHeader(string $name, string $value): void
  {
    header($name . ': ' . $value);
  }

  public static function getHeaderValue(string $headerName): string|false
  {
    $headers = getallheaders();
    $headers = array_change_key_case($headers);

    $headerName = strtolower($headerName);

    return trim($headers[$headerName]) ?: false;
  }

  public static function userIp(): string
  {
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
      $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
      $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else {
      $ip = $_SERVER['REMOTE_ADDR'];
    }

    return $ip;
  }

  public static function userAgent(): string
  {
    $agent = $_SERVER['HTTP_USER_AGENT'];
    if (empty($agent)) Errors::create('Запрос отклонён, ошибка прав доступа');
    return $agent;
  }
}