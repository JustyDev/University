-- Лабораторная работа 6. MySQL 8.0+

CREATE DATABASE IF NOT EXISTS lab6_superusers
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE lab6_superusers;

DROP TABLE IF EXISTS zzz;

CREATE TABLE zzz (
  user_id INT NOT NULL,
  transaction_id INT NOT NULL,
  transaction_date DATE NOT NULL,
  KEY idx_zzz_user_date (user_id, transaction_date, transaction_id)
) ENGINE=InnoDB;

INSERT INTO zzz (user_id, transaction_id, transaction_date) VALUES
(1, 101, '2022-02-12'),
(2, 105, '2022-02-13'),
(1, 111, '2022-02-14'),
(3, 121, '2022-02-15'),
(1, 101, '2022-02-16'),
(2, 105, '2022-02-17'),
(4, 101, '2022-02-18'),
(3, 105, '2022-02-19');

-- 1. Имитация ROW_NUMBER без оконных функций.
SELECT
  ranked.user_id,
  MIN(CASE WHEN ranked.row_num = 2 THEN ranked.transaction_date END) AS superuser_date
FROM (
  SELECT
    z1.user_id,
    z1.transaction_id,
    z1.transaction_date,
    COUNT(*) AS row_num
  FROM zzz z1
  JOIN zzz z2
    ON z2.user_id = z1.user_id
   AND (
     z2.transaction_date < z1.transaction_date
     OR (z2.transaction_date = z1.transaction_date AND z2.transaction_id <= z1.transaction_id)
   )
  GROUP BY z1.user_id, z1.transaction_id, z1.transaction_date
) ranked
GROUP BY ranked.user_id
ORDER BY superuser_date IS NULL, superuser_date, ranked.user_id;

-- 2. Решение с ROW_NUMBER.
WITH numbered AS (
  SELECT
    user_id,
    transaction_id,
    transaction_date,
    ROW_NUMBER() OVER (
      PARTITION BY user_id
      ORDER BY transaction_date, transaction_id
    ) AS row_num
  FROM zzz
)
SELECT
  user_id,
  MIN(CASE WHEN row_num = 2 THEN transaction_date END) AS superuser_date
FROM numbered
GROUP BY user_id
ORDER BY superuser_date IS NULL, superuser_date, user_id;

