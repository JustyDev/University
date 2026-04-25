-- ========== Задание 9.1 - pseudohash, хеш-индекс через crc32 ==========

CREATE TABLE pseudohash (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    url VARCHAR(255) NOT NULL,
    url_crc INT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    INDEX idx_crc (url_crc)
);

DELIMITER //
CREATE TRIGGER pseudohash_before_insert
BEFORE INSERT ON pseudohash
FOR EACH ROW
BEGIN
    SET NEW.url_crc = CRC32(NEW.url);
END;
//
CREATE TRIGGER pseudohash_before_update
BEFORE UPDATE ON pseudohash
FOR EACH ROW
BEGIN
    SET NEW.url_crc = CRC32(NEW.url);
END;
//
DELIMITER ;

-- ========== Задание 9.2 ==========

-- 1. Создать таблицу с orderNumber, productName, productLine и hash_md5

CREATE TABLE orderdetails_products_hash (
    orderNumber INT(11) NOT NULL,
    productName VARCHAR(70) NOT NULL,
    productLine VARCHAR(50) NOT NULL,
    hash_md5 CHAR(32) NOT NULL,
    PRIMARY KEY (orderNumber, productName)
);

-- 2. Заполнение с вычислением hash_md5
INSERT INTO orderdetails_products_hash (orderNumber, productName, productLine, hash_md5)
SELECT
    od.orderNumber,
    p.productName,
    p.productLine,
    MD5(CONCAT(od.orderNumber, '|', p.productName, '|', p.productLine))
FROM ClassicModels.OrderDetails od
JOIN ClassicModels.Products p ON od.productCode = p.productCode;

-- 3. Оценка селективности хэша и выбор необходимой длины префикса

-- Селективность по всему хэшу
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT hash_md5) AS unique_hashes,
    ROUND(100 * COUNT(DISTINCT hash_md5) / COUNT(*), 2) AS selectivity_percent
FROM orderdetails_products_hash;

-- Анализ уникальности по префиксам 8, 12, 16 символов
SELECT
    COUNT(DISTINCT LEFT(hash_md5, 8))  AS uniq8,
    COUNT(DISTINCT LEFT(hash_md5,12))  AS uniq12,
    COUNT(DISTINCT LEFT(hash_md5,16))  AS uniq16,
    COUNT(*) AS total
FROM orderdetails_products_hash;

-- 4. Создать индекс по необходимой длине (обычно 12-16 символов префикса гарантирует селективность для md5)
CREATE INDEX idx_md5_12 ON orderdetails_products_hash (hash_md5(12));

-- 5. Сравнение скорости запроса с индексом и без индекса:
-- (A) С индексом:
EXPLAIN SELECT * FROM orderdetails_products_hash WHERE hash_md5 = MD5('10100|1928 Mercedes-Benz SSK|Vintage Cars');

-- (B) Без индекса (удалить индекс, затем повторить explain):
DROP INDEX idx_md5_12 ON orderdetails_products_hash;
EXPLAIN SELECT * FROM orderdetails_products_hash WHERE hash_md5 = MD5('10100|1928 Mercedes-Benz SSK|Vintage Cars');

-- Запросы для анализа времени выполнения тестируются в клиенте вручную.
