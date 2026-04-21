-- Дополняем таблицы Marshrut, Samolet и Reis

-- 1. Маршруты (id подбирай по автоинкременту или подбери вручную)
INSERT INTO Marshrut (punkt_vyleta, punkt_naznacheniya, rasstoyanie) VALUES
('Чугуев', 'Мерефа', 120),     -- id = 4
('Москва', 'Васюки', 250),     -- id = 5
('Казань', 'Екатеринбург', 900), -- id = 6
('Новосибирск', 'Томск', 240); -- id = 7

-- 2. Самолёты
INSERT INTO Samolet (nomer, marka, chislo_mest, skorost_poleta) VALUES
('870', 'ТУ-154', 150, 950),   -- id = 4
('871', 'ТУ-154', 150, 950),   -- id = 5
('880', 'Боинг-737', 160, 900), -- id = 6
('881', 'Як-40', 32, 600);      -- id = 7

-- 3. Рейсы (чтобы нужные маршруты-самолёты-даты сочетались!)
-- Рейсы 'ТУ-154' по маршруту 'Чугуев'-'Мерефа'
INSERT INTO Reis (samolet_id, marshrut_id, data_vremya_vyleta, data_vremya_pribytiya, kolichestvo_prodannykh_biletov) VALUES
(4, 4, '2023-05-01 08:00', '2023-05-01 09:25', 110),  -- разовые для расчёта среднего времени
(5, 4, '2023-06-12 16:15', '2023-06-12 17:40', 120);

-- Рейсы других марок по такому же маршруту
INSERT INTO Reis (samolet_id, marshrut_id, data_vremya_vyleta, data_vremya_pribytiya, kolichestvo_prodannykh_biletov) VALUES
(6, 4, '2023-07-15 10:00', '2023-07-15 11:20', 90),
(7, 4, '2023-07-18 11:00', '2023-07-18 12:20', 25),
(6, 4, '2023-07-19 17:30', '2023-07-19 18:50', 120);

-- Рейсы для маршрута 'Москва'-'Васюки' и других маршрутов для тренировки
INSERT INTO Reis (samolet_id, marshrut_id, data_vremya_vyleta, data_vremya_pribytiya, kolichestvo_prodannykh_biletov) VALUES
(4, 5, '2023-08-20 12:00', '2023-08-20 13:00', 60),
(6, 5, '2023-10-02 18:00', '2023-10-02 19:00', 70),
(4, 7, '2023-11-14 10:00', '2023-11-14 11:00', 80);

-- Рейсы со слабой заполняемостью (< 70%): для теста задания 3
INSERT INTO Reis (samolet_id, marshrut_id, data_vremya_vyleta, data_vremya_pribytiya, kolichestvo_prodannykh_biletov) VALUES
(7, 6, '2023-05-01 05:00', '2023-05-01 06:20', 30), -- 32 места, заполнение < 70%
(7, 5, '2023-10-12 13:40', '2023-10-12 14:45', 21);

-- Рейс №870, 31 декабря 2000 года (для задания 4)
INSERT INTO Reis (samolet_id, marshrut_id, data_vremya_vyleta, data_vremya_pribytiya, kolichestvo_prodannykh_biletov) VALUES
(4, 5, '2000-12-31 15:00', '2000-12-31 16:30', 140);








-- 1. Среднее расчетное время полета для самолёта 'ТУ-154' по маршруту 'Чугуев' - 'Мерефа'
SELECT
    AVG(EXTRACT(EPOCH FROM (r.data_vremya_pribytiya - r.data_vremya_vyleta))/60) AS avg_flight_minutes
FROM Reis r
JOIN Samolet s ON r.samolet_id = s.id
JOIN Marshrut m ON r.marshrut_id = m.id
WHERE s.marka = 'ТУ-154'
  AND m.punkt_vyleta = 'Чугуев'
  AND m.punkt_naznacheniya = 'Мерефа';
-- Среднее время в минутах (для PostgreSQL: EXTRACT(EPOCH ...)/60). Для SQLite/Oracle/MySQL выражение может отличаться.

-- 2. Марка самолёта, которая чаще всего летает по маршруту 'Чугуев' - 'Мерефа'
SELECT
    s.marka, COUNT(*) AS kolichestvo_reisov
FROM Reis r
JOIN Samolet s ON r.samolet_id = s.id
JOIN Marshrut m ON r.marshrut_id = m.id
WHERE m.punkt_vyleta = 'Чугуев'
  AND m.punkt_naznacheniya = 'Мерефа'
GROUP BY s.marka
ORDER BY kolichestvo_reisov DESC
LIMIT 1;
-- Чаще всего летавшая марка (если несколько — вернёт одну, самые частые можно выбрать HAVING COUNT(*)=максимум)

-- 3. Маршруты, по которым чаще всего летают рейсы, заполненные менее чем на 70%
SELECT
    m.punkt_vyleta,
    m.punkt_naznacheniya,
    COUNT(*) AS kolichestvo_reisov
FROM Reis r
JOIN Samolet s ON r.samolet_id = s.id
JOIN Marshrut m ON r.marshrut_id = m.id
WHERE (CAST(r.kolichestvo_prodannykh_biletov AS FLOAT) / s.chislo_mest) < 0.7
GROUP BY m.punkt_vyleta, m.punkt_naznacheniya
HAVING COUNT(*) = (
    SELECT MAX(cnt) FROM (
        SELECT COUNT(*) AS cnt
        FROM Reis r2
        JOIN Samolet s2 ON r2.samolet_id = s2.id
        WHERE (CAST(r2.kolichestvo_prodannykh_biletov AS FLOAT) / s2.chislo_mest) < 0.7
        GROUP BY r2.marshrut_id
    ) sub
);
-- Самые "незаполненные" маршруты по частоте таких рейсов

-- 4. Определить наличие свободных мест на рейс №870 31 декабря 2000г.
SELECT
    s.nomer AS nomer_rejsa,
    r.data_vremya_vyleta,
    s.chislo_mest - r.kolichestvo_prodannykh_biletov AS svobodnye_mesta
FROM Reis r
JOIN Samolet s ON r.samolet_id = s.id
WHERE s.nomer = '870'
  AND DATE(r.data_vremya_vyleta) = '2000-12-31';
-- Свободные места на нужном рейсе
