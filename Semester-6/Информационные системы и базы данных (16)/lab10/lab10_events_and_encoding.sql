-- Лабораторная работа 10. MySQL 8.0+

-- Задание 10.1.
-- Выполнять в базе classicmodels.
USE classicmodels;

SET GLOBAL event_scheduler = ON;

DROP EVENT IF EXISTS refresh_denormalized_order_info;
DROP TABLE IF EXISTS denormalized_order_info;

CREATE TABLE denormalized_order_info (
  customerName VARCHAR(50) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  country VARCHAR(50) NOT NULL,
  orderNumber INT NOT NULL,
  productCode VARCHAR(15) NOT NULL,
  productLine VARCHAR(50) NOT NULL,
  textDescription TEXT NOT NULL,
  PRIMARY KEY (orderNumber, productCode),
  KEY idx_denorm_customer (customerName),
  KEY idx_denorm_country (country)
) ENGINE=InnoDB;

DELIMITER //

CREATE EVENT refresh_denormalized_order_info
ON SCHEDULE EVERY 1 HOUR
STARTS CURRENT_TIMESTAMP
DO
BEGIN
  TRUNCATE TABLE denormalized_order_info;

  INSERT INTO denormalized_order_info (
    customerName, phone, country, orderNumber, productCode, productLine, textDescription
  )
  SELECT
    c.customerName,
    c.phone,
    c.country,
    o.orderNumber,
    od.productCode,
    p.productLine,
    pl.textDescription
  FROM customers c
  JOIN orders o ON o.customerNumber = c.customerNumber
  JOIN orderdetails od ON od.orderNumber = o.orderNumber
  JOIN products p ON p.productCode = od.productCode
  JOIN productlines pl ON pl.productLine = p.productLine;
END//

DELIMITER ;

-- Первичное заполнение без ожидания события.
INSERT INTO denormalized_order_info (
  customerName, phone, country, orderNumber, productCode, productLine, textDescription
)
SELECT
  c.customerName,
  c.phone,
  c.country,
  o.orderNumber,
  od.productCode,
  p.productLine,
  pl.textDescription
FROM customers c
JOIN orders o ON o.customerNumber = c.customerNumber
JOIN orderdetails od ON od.orderNumber = o.orderNumber
JOIN products p ON p.productCode = od.productCode
JOIN productlines pl ON pl.productLine = p.productLine;

-- Задание 10.2.
CREATE DATABASE IF NOT EXISTS lab10_image_encoding
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE lab10_image_encoding;

DROP PROCEDURE IF EXISTS generate_images;
DROP PROCEDURE IF EXISTS decode_image_by_id;
DROP TABLE IF EXISTS images;

CREATE TABLE images (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  figure_type TINYINT UNSIGNED NOT NULL COMMENT '0 - овал, 1 - прямоугольник',
  blue TINYINT UNSIGNED NOT NULL,
  green TINYINT UNSIGNED NOT NULL,
  red TINYINT UNSIGNED NOT NULL,
  width_or_small_diameter SMALLINT UNSIGNED NOT NULL,
  height_or_big_diameter SMALLINT UNSIGNED NOT NULL,
  code BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  KEY idx_images_code (code),
  CONSTRAINT chk_images_type CHECK (figure_type IN (0, 1)),
  CONSTRAINT chk_images_width CHECK (width_or_small_diameter <= 500),
  CONSTRAINT chk_images_height CHECK (height_or_big_diameter <= 500)
) ENGINE=InnoDB;

DELIMITER //

CREATE PROCEDURE generate_images(IN p_count INT)
BEGIN
  DECLARE i INT DEFAULT 0;
  DECLARE v_type TINYINT UNSIGNED;
  DECLARE v_blue TINYINT UNSIGNED;
  DECLARE v_green TINYINT UNSIGNED;
  DECLARE v_red TINYINT UNSIGNED;
  DECLARE v_w SMALLINT UNSIGNED;
  DECLARE v_h SMALLINT UNSIGNED;
  DECLARE v_code BIGINT UNSIGNED;

  WHILE i < p_count DO
    SET v_type = FLOOR(RAND() * 2);
    SET v_blue = FLOOR(RAND() * 256);
    SET v_green = FLOOR(RAND() * 256);
    SET v_red = FLOOR(RAND() * 256);
    SET v_w = FLOOR(RAND() * 501);
    SET v_h = FLOOR(RAND() * 501);

    -- Раскладка битов:
    -- 1 бит тип, 8 бит B, 8 бит G, 8 бит R, 9 бит ширина/малый диаметр,
    -- 9 бит высота/большой диаметр. Всего 43 бита.
    SET v_code =
      (CAST(v_type AS UNSIGNED) << 42) |
      (CAST(v_blue AS UNSIGNED) << 34) |
      (CAST(v_green AS UNSIGNED) << 26) |
      (CAST(v_red AS UNSIGNED) << 18) |
      (CAST(v_w AS UNSIGNED) << 9) |
      CAST(v_h AS UNSIGNED);

    INSERT INTO images (
      figure_type, blue, green, red,
      width_or_small_diameter, height_or_big_diameter, code
    )
    VALUES (v_type, v_blue, v_green, v_red, v_w, v_h, v_code);

    SET i = i + 1;
  END WHILE;
END//

CREATE PROCEDURE decode_image_by_id(IN p_id INT UNSIGNED)
BEGIN
  SELECT
    id,
    code,
    CASE ((code >> 42) & 1)
      WHEN 0 THEN 'овал'
      ELSE 'прямоугольник'
    END AS figure_type,
    (code >> 34) & 255 AS blue,
    (code >> 26) & 255 AS green,
    (code >> 18) & 255 AS red,
    (code >> 9) & 511 AS width_or_small_diameter,
    code & 511 AS height_or_big_diameter
  FROM images
  WHERE id = p_id;
END//

DELIMITER ;

CALL generate_images(10);
CALL decode_image_by_id(1);

