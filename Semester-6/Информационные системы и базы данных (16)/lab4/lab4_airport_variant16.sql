-- Лабораторная работа 4. Вариант 16.
-- Запросы используют схему airport_v16 из lab1_airport_variant16.sql.

USE airport_v16;

-- 1. Среднее расчетное время полета для самолета "ТУ-154"
-- по маршруту "Чугуев" - "Мерефа".
SELECT
  ac.model,
  dep.city AS departure_city,
  arr.city AS arrival_city,
  ROUND(AVG(TIMESTAMPDIFF(MINUTE, f.scheduled_departure, f.scheduled_arrival)), 2) AS avg_flight_minutes
FROM flights f
JOIN aircraft ac ON ac.aircraft_id = f.aircraft_id
JOIN routes r ON r.route_id = f.route_id
JOIN airports dep ON dep.airport_id = r.departure_airport_id
JOIN airports arr ON arr.airport_id = r.arrival_airport_id
WHERE ac.model = 'ТУ-154'
  AND dep.city = 'Чугуев'
  AND arr.city = 'Мерефа'
GROUP BY ac.model, dep.city, arr.city;

-- 2. Марка самолета, которая чаще всего летает по тому же маршруту.
SELECT
  ac.model,
  COUNT(*) AS flights_count
FROM flights f
JOIN aircraft ac ON ac.aircraft_id = f.aircraft_id
JOIN routes r ON r.route_id = f.route_id
JOIN airports dep ON dep.airport_id = r.departure_airport_id
JOIN airports arr ON arr.airport_id = r.arrival_airport_id
WHERE dep.city = 'Чугуев'
  AND arr.city = 'Мерефа'
GROUP BY ac.model
ORDER BY flights_count DESC
LIMIT 1;

-- 3. Маршрут/маршруты, по которым чаще всего летают рейсы,
-- заполненные менее чем на 70%.
WITH low_loaded_flights AS (
  SELECT
    f.flight_id,
    r.route_id,
    dep.city AS departure_city,
    arr.city AS arrival_city
  FROM flights f
  JOIN aircraft ac ON ac.aircraft_id = f.aircraft_id
  JOIN routes r ON r.route_id = f.route_id
  JOIN airports dep ON dep.airport_id = r.departure_airport_id
  JOIN airports arr ON arr.airport_id = r.arrival_airport_id
  WHERE f.sold_seats / ac.seats < 0.70
),
route_counts AS (
  SELECT
    route_id,
    departure_city,
    arrival_city,
    COUNT(*) AS low_loaded_count
  FROM low_loaded_flights
  GROUP BY route_id, departure_city, arrival_city
)
SELECT departure_city, arrival_city, low_loaded_count
FROM route_counts
WHERE low_loaded_count = (SELECT MAX(low_loaded_count) FROM route_counts);

-- 4. Наличие свободных мест на рейс N 870 31 декабря 2000 г.
SELECT
  f.flight_no,
  DATE(f.scheduled_departure) AS flight_date,
  dep.city AS departure_city,
  arr.city AS arrival_city,
  ac.model,
  ac.seats AS total_seats,
  f.sold_seats,
  ac.seats - f.sold_seats AS free_seats
FROM flights f
JOIN aircraft ac ON ac.aircraft_id = f.aircraft_id
JOIN routes r ON r.route_id = f.route_id
JOIN airports dep ON dep.airport_id = r.departure_airport_id
JOIN airports arr ON arr.airport_id = r.arrival_airport_id
WHERE f.flight_no = 870
  AND DATE(f.scheduled_departure) = '2000-12-31';

