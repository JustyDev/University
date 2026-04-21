-- Структура из ЛР 1
-- ==== ЗАПРОСЫ К ЛАБОРАТОРНОЙ 3 ====

-- 1. Определить наличие свободных мест на рейс № 870 31 декабря 2000 года.
SELECT
    S.nomer,
    R.data_vremya_vyleta,
    (S.chislo_mest - R.kolichestvo_prodannykh_biletov) AS svobodnye_mesta
FROM Reis R
JOIN Samolet S ON R.samolet_id = S.id
WHERE S.nomer = '870'
  AND DATE(R.data_vremya_vyleta) = '2000-12-31';
-- Показывает количество свободных мест на рейсе № 870 в указанный день

-- 2. Рассчитать дальность полёта самолёта по каждому маршруту.
SELECT
    S.nomer AS samolet_nomer,
    S.marka,
    M.punkt_vyleta,
    M.punkt_naznacheniya,
    M.rasstoyanie
FROM Reis R
JOIN Samolet S ON R.samolet_id = S.id
JOIN Marshrut M ON R.marshrut_id = M.id;
-- Выводит все маршруты, по которым летал каждый самолёт, вместе с расстоянием

-- 3. Создать таблицу расписания самолётов по маршруту «Москва»-«Васюки».
SELECT
    R.id AS reis_id,
    S.nomer AS samolet_nomer,
    S.marka,
    R.data_vremya_vyleta,
    R.data_vremya_pribytiya
FROM Reis R
JOIN Marshrut M ON R.marshrut_id = M.id
JOIN Samolet S ON R.samolet_id = S.id
WHERE M.punkt_vyleta = 'Москва' AND M.punkt_naznacheniya = 'Васюки';
-- Вывод расписания по определённому маршруту

-- 4. Увеличить число мест самолётов «ТУ» на 5 человек.
UPDATE Samolet
SET chislo_mest = chislo_mest + 5
WHERE marka LIKE 'ТУ%';
-- Увеличивает число мест у всех самолётов марки, начинающейся на "ТУ"

-- 5. Создать сводную таблицу количества вылетов самолётов по маршрутам.
SELECT
    M.punkt_vyleta,
    M.punkt_naznacheniya,
    COUNT(R.id) AS kolichestvo_vyletov
FROM Reis R
JOIN Marshrut M ON R.marshrut_id = M.id
GROUP BY M.punkt_vyleta, M.punkt_naznacheniya;
-- Количество вылетов по каждому маршруту

-- 6. Уменьшить скорость самолётов «Боинг» на 10%.
UPDATE Samolet
SET skorost_poleta = skorost_poleta * 0.9
WHERE marka LIKE '%Боинг%';
-- Уменьшает скорость у всех самолётов марок, содержащих "Боинг"
