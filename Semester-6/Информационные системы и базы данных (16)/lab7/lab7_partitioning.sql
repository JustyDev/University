-- Лабораторная работа 7. MySQL 8.0+
-- Таблица zzz совместима с заданием 6: user_id, transaction_id, transaction_date.

CREATE DATABASE IF NOT EXISTS lab7_partitioning
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE lab7_partitioning;

DROP PROCEDURE IF EXISTS fill_zzz_random;
DROP PROCEDURE IF EXISTS rebuild_zzz_partitions;
DROP TABLE IF EXISTS zzz_partitioned;
DROP TABLE IF EXISTS zzz;

CREATE TABLE zzz (
  user_id INT NOT NULL,
  transaction_id INT NOT NULL,
  transaction_date DATE NOT NULL,
  KEY idx_zzz_user_date (user_id, transaction_date, transaction_id),
  KEY idx_zzz_date (transaction_date)
) ENGINE=InnoDB;

DELIMITER //

CREATE PROCEDURE fill_zzz_random(IN p_rows INT)
BEGIN
  DECLARE i INT DEFAULT 0;

  WHILE i < p_rows DO
    INSERT INTO zzz (user_id, transaction_id, transaction_date)
    VALUES (
      1 + FLOOR(RAND() * 20),
      100 + FLOOR(RAND() * 900),
      DATE_ADD('1999-01-01', INTERVAL FLOOR(RAND() * 3650) DAY)
    );

    SET i = i + 1;
  END WHILE;
END//

CREATE PROCEDURE rebuild_zzz_partitions()
BEGIN
  DECLARE v_total INT DEFAULT 0;
  DECLARE v_not_added INT DEFAULT 0;
  DECLARE v_accumulated INT DEFAULT 0;
  DECLARE v_year INT;
  DECLARE v_count INT;
  DECLARE v_done BOOL DEFAULT FALSE;
  DECLARE v_partitions TEXT DEFAULT '';

  DECLARE year_cursor CURSOR FOR
    SELECT YEAR(transaction_date) AS y, COUNT(*) AS c
    FROM zzz
    GROUP BY YEAR(transaction_date)
    ORDER BY y;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

  SELECT COUNT(*) INTO v_total FROM zzz;
  SET v_not_added = v_total;

  DROP TABLE IF EXISTS zzz_partitioned;

  IF v_total = 0 THEN
    CREATE TABLE zzz_partitioned (
      user_id INT NOT NULL,
      transaction_id INT NOT NULL,
      transaction_date DATE NOT NULL,
      KEY idx_zzzp_user_date (user_id, transaction_date, transaction_id),
      KEY idx_zzzp_date (transaction_date)
    ) ENGINE=InnoDB;
  ELSE
    OPEN year_cursor;

    read_loop: LOOP
      FETCH year_cursor INTO v_year, v_count;
      IF v_done THEN
        LEAVE read_loop;
      END IF;

      SET v_accumulated = v_accumulated + v_count;

      IF v_accumulated > v_not_added * 0.05 THEN
        SET v_partitions = CONCAT(
          v_partitions,
          IF(v_partitions = '', '', ', '),
          'PARTITION p', v_year, ' VALUES LESS THAN (', v_year + 1, ')'
        );
        SET v_not_added = v_not_added - v_accumulated;
        SET v_accumulated = 0;
      END IF;
    END LOOP;

    CLOSE year_cursor;

    SET v_partitions = CONCAT(
      v_partitions,
      IF(v_partitions = '', '', ', '),
      'PARTITION pmax VALUES LESS THAN MAXVALUE'
    );

    SET @sql_create = CONCAT(
      'CREATE TABLE zzz_partitioned (',
      'user_id INT NOT NULL,',
      'transaction_id INT NOT NULL,',
      'transaction_date DATE NOT NULL,',
      'KEY idx_zzzp_user_date (user_id, transaction_date, transaction_id),',
      'KEY idx_zzzp_date (transaction_date)',
      ') ENGINE=InnoDB ',
      'PARTITION BY RANGE (YEAR(transaction_date)) (',
      v_partitions,
      ')'
    );

    PREPARE stmt FROM @sql_create;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    INSERT INTO zzz_partitioned (user_id, transaction_id, transaction_date)
    SELECT user_id, transaction_id, transaction_date
    FROM zzz;
  END IF;
END//

DELIMITER ;

CALL fill_zzz_random(100);
CALL rebuild_zzz_partitions();

SELECT PARTITION_NAME, TABLE_ROWS
FROM information_schema.PARTITIONS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'zzz_partitioned'
ORDER BY PARTITION_ORDINAL_POSITION;

