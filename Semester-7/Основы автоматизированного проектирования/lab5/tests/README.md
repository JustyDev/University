# Тесты к ЛР 5

- `unit.test.js` — 20 модульных тестов серверной части TransLark (маршрутизация
  Флойда — Уоршелла, реестр языков, токены SID, лимиты запросов, транслитерация).
  Запускаются на скомпилированном коде сервера: собрать backend командой
  `tsc -p backend/tsconfig.json --outDir ../tl-dist` рядом с этой папкой, затем
  `node --test unit.test.js`. Протокол прогона — `unit-output.txt`.
- `system.test.mjs` — 15 системных тестов «чёрного ящика» на https://translark.ru
  (доступность, SSR-страницы, HTTPS, защита API, лимиты, время отклика).
  Запуск: `node system.test.mjs`, результаты — `system-results.json`.
