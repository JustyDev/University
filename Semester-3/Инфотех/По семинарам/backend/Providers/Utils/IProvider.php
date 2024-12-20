<?php

namespace Api\Providers\Utils;

interface IProvider {
  public function route(string $uri_part): void;
}