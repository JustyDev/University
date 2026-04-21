-- Лабораторная работа 9. MySQL 8.0+

CREATE DATABASE IF NOT EXISTS lab9_hash_indexes
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE lab9_hash_indexes;

-- Задание 9.1. Имитация hash-индекса через CRC32.
DROP TRIGGER IF EXISTS trg_pseudohash_before_insert;
DROP TRIGGER IF EXISTS trg_pseudohash_before_update;
DROP TABLE IF EXISTS pseudohash;

CREATE TABLE pseudohash (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  url VARCHAR(255) NOT NULL,
  url_crc INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_pseudohash_url_crc (url_crc)
) ENGINE=InnoDB;

DELIMITER //

CREATE TRIGGER trg_pseudohash_before_insert
BEFORE INSERT ON pseudohash
FOR EACH ROW
BEGIN
  SET NEW.url_crc = CRC32(NEW.url);
END//

CREATE TRIGGER trg_pseudohash_before_update
BEFORE UPDATE ON pseudohash
FOR EACH ROW
BEGIN
  SET NEW.url_crc = CRC32(NEW.url);
END//

DELIMITER ;

INSERT INTO pseudohash (url) VALUES
('https://example.org/'),
('https://example.org/catalog'),
('https://example.org/catalog/item/1');

-- Поиск использует crc32-индекс и проверяет исходную строку на случай коллизии.
SET @url := 'https://example.org/catalog';

EXPLAIN SELECT *
FROM pseudohash
WHERE url_crc = CRC32(@url)
  AND url = @url;

SELECT *
FROM pseudohash
WHERE url_crc = CRC32(@url)
  AND url = @url;

-- Задание 9.2.
-- Выполнять в установленной базе classicmodels либо заменить USE на нужную БД.
USE classicmodels;

DROP TABLE IF EXISTS order_product_hash;

CREATE TABLE order_product_hash AS
SELECT
  od.orderNumber,
  p.productName,
  p.productLine,
  MD5(CONCAT_WS('#', od.orderNumber, p.productName, p.productLine)) AS hash_md5
FROM orderdetails od
JOIN products p ON p.productCode = od.productCode;

ALTER TABLE order_product_hash
  MODIFY orderNumber INT NOT NULL,
  MODIFY productName VARCHAR(70) NOT NULL,
  MODIFY productLine VARCHAR(50) NOT NULL,
  MODIFY hash_md5 CHAR(32) NOT NULL;

-- Селективность полного MD5-хэша.
SELECT
  COUNT(DISTINCT hash_md5) / COUNT(*) AS full_hash_selectivity,
  COUNT(*) AS rows_total,
  COUNT(DISTINCT hash_md5) AS distinct_hashes
FROM order_product_hash;

-- Минимальная длина префикса, при которой селективность равна селективности полного хэша.
WITH RECURSIVE prefix_lengths AS (
  SELECT 1 AS prefix_len
  UNION ALL
  SELECT prefix_len + 1
  FROM prefix_lengths
  WHERE prefix_len < 32
),
selectivity AS (
  SELECT
    prefix_len,
    COUNT(DISTINCT LEFT(hash_md5, prefix_len)) / COUNT(*) AS prefix_selectivity
  FROM prefix_lengths
  CROSS JOIN order_product_hash
  GROUP BY prefix_len
),
full_selectivity AS (
  SELECT COUNT(DISTINCT hash_md5) / COUNT(*) AS value
  FROM order_product_hash
)
SELECT MIN(s.prefix_len) AS required_prefix_length
FROM selectivity s
CROSS JOIN full_selectivity fs
WHERE s.prefix_selectivity = fs.value;

-- Если предыдущий запрос вернул, например, 8, создаем индекс длины 8.
-- При другом результате заменить 8 на найденное значение.
CREATE INDEX idx_order_product_hash_md5_prefix
  ON order_product_hash (hash_md5(8));

SET @hash := (
  SELECT hash_md5
  FROM order_product_hash
  LIMIT 1
);

EXPLAIN ANALYZE
SELECT *
FROM order_product_hash
WHERE hash_md5 = @hash;

ALTER TABLE order_product_hash DROP INDEX idx_order_product_hash_md5_prefix;

EXPLAIN ANALYZE
SELECT *
FROM order_product_hash
WHERE hash_md5 = @hash;

