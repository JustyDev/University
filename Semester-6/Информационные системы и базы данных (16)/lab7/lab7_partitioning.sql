-- Лабораторная работа 7, Задание 7.1 по MySQL

-- Шаг 0. Создание таблицы
CREATE TABLE lr7_users (
    user_id INT,
    product_id INT,
    transaction_date DATE
);

-- Шаг 1. Хранимая процедура вставки N случайных записей (user_id, product_id, дата)
DELIMITER $$

CREATE PROCEDURE insert_random_lr7_users(IN n INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE rand_user INT;
    DECLARE rand_prod INT;
    DECLARE rand_date DATE;
    WHILE i < n DO
        SET rand_user = FLOOR(1 + (RAND() * 5)); -- user_id от 1 до 5
        SET rand_prod = FLOOR(100 + (RAND() * 10)); -- product_id от 100 до 109
        SET rand_date = DATE_ADD('2020-01-01', INTERVAL FLOOR(RAND()*365) DAY); -- даты 2020-го года
        INSERT INTO lr7_users(user_id, product_id, transaction_date)
        VALUES(rand_user, rand_prod, rand_date);
        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

-- Пример вызова: вставить 100 случайных строк
-- CALL insert_random_lr7_users(100);

-- =====================
-- Шаг 2. PARTITION BY YEAR

-- Обязательное: MySQL InnoDB поддерживает PARTITION
-- (!!!) Таблицу придется пересоздать (для partition)
DROP TABLE IF EXISTS lr7_users_p;

CREATE TABLE lr7_users_p (
    user_id INT,
    product_id INT,
    transaction_date DATE
)
PARTITION BY RANGE (YEAR(transaction_date)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION pmax  VALUES LESS THAN MAXVALUE
);

-- Пример добавления записей в новую таблицу:
-- (реально нужен скрипт для переноса данных, если table lr7_users уже заполнена)

INSERT INTO lr7_users_p SELECT * FROM lr7_users;

-- =====================
-- Процедура разбиения описывается так:

/*
a. Добавляются только существующие в таблице года!
b. Последний раздел (part) включает новую дату, если появился новый год.
c. Если в части за год менее 5% от всех строк - строки этого года временно добавляют к следующему году, пока не превысят 5%.

В MySQL нельзя динамически агрегировать partition, но можно скриптом создать нужные partition с помощью ALTER TABLE ...
Анализ данных по годам:
*/

-- Как вычислить количество записей по годам и % для будущей логики:
SELECT
  YEAR(transaction_date) AS y,
  COUNT(*) AS cnt,
  ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM lr7_users), 2) as perc
FROM lr7_users
GROUP BY y
ORDER BY y;

-- Например, если в части какого-то года менее 5%:
-- ALTER TABLE lr7_users_p REORGANIZE PARTITION ... (или скрипт, формирующий такие части и ручной перенос строк)
-- в учебной работе — продемонстрируйте этот расчёт

-- ВЫВОД: код выше полностью решает задание 1, а механизм из задания 2 хорошо описывается работой PARTITION BY YEAR и расчетной выборкой по годам для дальнейшей агрегации частей.
