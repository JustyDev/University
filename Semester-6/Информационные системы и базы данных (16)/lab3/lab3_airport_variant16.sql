-- Лабораторная работа 3. Вариант 16.
-- Запросы используют схему airport_v16 из lab1_airport_variant16.sql.

USE airport_v16;

-- 1. Определить наличие свободных мест на рейс N 870 31 декабря 2000 года.
SELECT
  f.flight_no,
  DATE(f.scheduled_departure) AS flight_date,
  ac.model,
  ac.seats AS total_seats,
  f.sold_seats,
  ac.seats - f.sold_seats AS free_seats,
  CASE WHEN ac.seats > f.sold_seats THEN 'Есть свободные места' ELSE 'Свободных мест нет' END AS availability
FROM flights f
JOIN aircraft ac ON ac.aircraft_id = f.aircraft_id
WHERE f.flight_no = 870
  AND DATE(f.scheduled_departure) = '2000-12-31';

-- 2. Рассчитать дальность полета самолета по каждому маршруту.
-- Если в таблице маршрутов хранится фактическая дальность, она выводится напрямую.
SELECT
  dep.city AS departure_city,
  arr.city AS arrival_city,
  r.distance_km AS route_distance_km,
  ac.model,
  ROUND(ac.speed_kmh * TIMESTAMPDIFF(MINUTE, f.scheduled_departure, f.scheduled_arrival) / 60, 2) AS calculated_distance_km
FROM flights f
JOIN routes r ON r.route_id = f.route_id
JOIN airports dep ON dep.airport_id = r.departure_airport_id
JOIN airports arr ON arr.airport_id = r.arrival_airport_id
JOIN aircraft ac ON ac.aircraft_id = f.aircraft_id
ORDER BY dep.city, arr.city, ac.model;

-- 3. Создать таблицу расписания самолетов по маршруту "Москва" - "Васюки".
DROP TABLE IF EXISTS moscow_vasyuki_schedule;

CREATE TABLE moscow_vasyuki_schedule AS
SELECT
  f.flight_no,
  dep.city AS departure_city,
  arr.city AS arrival_city,
  ac.board_number,
  ac.model,
  f.scheduled_departure,
  f.scheduled_arrival,
  ac.seats,
  f.sold_seats,
  ac.seats - f.sold_seats AS free_seats
FROM flights f
JOIN routes r ON r.route_id = f.route_id
JOIN airports dep ON dep.airport_id = r.departure_airport_id
JOIN airports arr ON arr.airport_id = r.arrival_airport_id
JOIN aircraft ac ON ac.aircraft_id = f.aircraft_id
WHERE dep.city = 'Москва'
  AND arr.city = 'Васюки';

ALTER TABLE moscow_vasyuki_schedule
  ADD PRIMARY KEY (flight_no, scheduled_departure);

SELECT * FROM moscow_vasyuki_schedule;

-- 4. Увеличить число мест самолетов "ТУ" на 5 человек.
UPDATE aircraft
SET seats = seats + 5
WHERE model LIKE 'ТУ%';

-- 5. Создать сводную таблицу количества вылетов самолетов по маршрутам.
DROP TABLE IF EXISTS flight_count_by_route;

CREATE TABLE flight_count_by_route AS
SELECT
  dep.city AS departure_city,
  arr.city AS arrival_city,
  COUNT(*) AS flights_count
FROM flights f
JOIN routes r ON r.route_id = f.route_id
JOIN airports dep ON dep.airport_id = r.departure_airport_id
JOIN airports arr ON arr.airport_id = r.arrival_airport_id
GROUP BY dep.city, arr.city;

ALTER TABLE flight_count_by_route
  ADD PRIMARY KEY (departure_city, arrival_city);

SELECT * FROM flight_count_by_route;

-- 10. Уменьшить скорость самолетов "Боинг" на 10%.
UPDATE aircraft
SET speed_kmh = ROUND(speed_kmh * 0.90, 2)
WHERE model LIKE 'Боинг%';

