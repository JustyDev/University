-- ===================== Задание 10.1 =====================
-- Создание денормализованной таблицы и события-обновления

CREATE TABLE ClassicModels.denorm_orders_products AS
SELECT
    c.customerName,
    c.phone,
    c.country,
    o.orderNumber,
    p.productCode,
    p.productName,
    p.productLine,
    p.textDescription
FROM ClassicModels.Orders o
JOIN ClassicModels.Customers c ON o.customerNumber = c.customerNumber
JOIN ClassicModels.OrderDetails od ON od.orderNumber = o.orderNumber
JOIN ClassicModels.Products p ON od.productCode = p.productCode;

-- Если textDescription нет в таблице Products, а есть в ProductLines - добавить join
ALTER TABLE ClassicModels.denorm_orders_products ADD COLUMN textDescription VARCHAR(4000);
UPDATE ClassicModels.denorm_orders_products d
JOIN ClassicModels.Products p ON d.productCode = p.productCode
JOIN ClassicModels.ProductLines pl ON p.productLine = pl.productLine
SET d.textDescription = pl.textDescription;

-- Создать процедуру/событие для регулярного обновления (раз в месяц)
DELIMITER $$
CREATE EVENT ev_update_denorm_orders_products
ON SCHEDULE EVERY 1 MONTH
DO
BEGIN
    DELETE FROM ClassicModels.denorm_orders_products;
    INSERT INTO ClassicModels.denorm_orders_products
    (customerName, phone, country, orderNumber, productCode, productName, productLine, textDescription)
    SELECT
        c.customerName,
        c.phone,
        c.country,
        o.orderNumber,
        p.productCode,
        p.productName,
        p.productLine,
        pl.textDescription
    FROM ClassicModels.Orders o
    JOIN ClassicModels.Customers c ON o.customerNumber = c.customerNumber
    JOIN ClassicModels.OrderDetails od ON od.orderNumber = o.orderNumber
    JOIN ClassicModels.Products p ON od.productCode = p.productCode
    JOIN ClassicModels.ProductLines pl ON p.productLine = pl.productLine;
END $$
DELIMITER ;
-- Включить обработку событий, если выключено (разово)
SET GLOBAL event_scheduler = ON;

-- ===================== Задание 10.2 =====================
-- Таблица изображений
CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `type` TINYINT UNSIGNED NOT NULL, -- 0 - овал, 1 - прямоугольник
    blue TINYINT UNSIGNED NOT NULL,
    green TINYINT UNSIGNED NOT NULL,
    red TINYINT UNSIGNED NOT NULL,
    width SMALLINT UNSIGNED NOT NULL,
    height SMALLINT UNSIGNED NOT NULL,
    code BIGINT UNSIGNED NOT NULL
);

-- Процедура генерации (кодирования) записи по параметрам
DELIMITER $$
CREATE PROCEDURE gen_image(
    IN in_type TINYINT UNSIGNED,
    IN in_b TINYINT UNSIGNED,
    IN in_g TINYINT UNSIGNED,
    IN in_r TINYINT UNSIGNED,
    IN in_width SMALLINT UNSIGNED,
    IN in_height SMALLINT UNSIGNED
)
BEGIN
    DECLARE v_code BIGINT UNSIGNED;
    -- Кодируем: тип (1), blue (8), green (8), red (8), width (10), height (10) = 45 бит
    SET v_code =
        (in_type & 1)
        | ((in_b & 255) << 1)
        | ((in_g & 255) << 9)
        | ((in_r & 255) << 17)
        | ((in_width & 1023) << 25)
        | ((in_height & 1023) << 35);
    INSERT INTO images (`type`, blue, green, red, width, height, code)
    VALUES (in_type, in_b, in_g, in_r, in_width, in_height, v_code);
END $$
DELIMITER ;

-- Процедура генерации N случайных записей
DELIMITER $$
CREATE PROCEDURE gen_random_images(IN in_n INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    WHILE i < in_n DO
        CALL gen_image(
            FLOOR(RAND()*2),              -- тип фигуры (0-овал, 1-прямоугольник)
            FLOOR(RAND()*256),            -- blue
            FLOOR(RAND()*256),            -- green
            FLOOR(RAND()*256),            -- red
            FLOOR(RAND()*501),            -- width/малый_диаметр
            FLOOR(RAND()*501)             -- height/большой_диаметр
        );
        SET i = i + 1;
    END WHILE;
END $$
DELIMITER ;

-- Процедура декодирования по id
DELIMITER $$
CREATE PROCEDURE image_decode(IN in_id INT)
BEGIN
    DECLARE v_code BIGINT UNSIGNED;
    DECLARE v_type TINYINT UNSIGNED;
    DECLARE v_b TINYINT UNSIGNED;
    DECLARE v_g TINYINT UNSIGNED;
    DECLARE v_r TINYINT UNSIGNED;
    DECLARE v_width SMALLINT UNSIGNED;
    DECLARE v_height SMALLINT UNSIGNED;

    SELECT code INTO v_code FROM images WHERE id = in_id;
    SET v_type = v_code & 1;
    SET v_b = (v_code >> 1) & 255;
    SET v_g = (v_code >> 9) & 255;
    SET v_r = (v_code >> 17) & 255;
    SET v_width = (v_code >> 25) & 1023;
    SET v_height = (v_code >> 35) & 1023;

    SELECT
        v_type AS `type`, v_b AS blue, v_g AS green, v_r AS red, v_width AS width, v_height AS height;
END $$
DELIMITER ;

-- Пример использования:
-- Генерация 10 изображений
-- CALL gen_random_images(10);

-- Пример декодирования:
-- CALL image_decode(1);

