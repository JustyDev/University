-- Лабораторная работа 8. MySQL 8.0+

CREATE DATABASE IF NOT EXISTS lab8_delete_triggers
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE lab8_delete_triggers;

DROP TRIGGER IF EXISTS trg_clients_after_delete;
DROP TRIGGER IF EXISTS trg_delete_users_after_insert;
DROP TRIGGER IF EXISTS trg_delete_users_after_delete;
DROP TABLE IF EXISTS delete_users_by_month;
DROP TABLE IF EXISTS delete_users;
DROP TABLE IF EXISTS Clients;

CREATE TABLE `Clients` (
  `Id` INT NOT NULL,
  `FirstName` VARCHAR(20) COLLATE utf8mb4_general_ci NOT NULL,
  `LastName` VARCHAR(20) COLLATE utf8mb4_general_ci NOT NULL,
  `Phone` VARCHAR(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Email` VARCHAR(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `year` INT NOT NULL DEFAULT '2020',
  `month` INT NOT NULL DEFAULT '1',
  `capital` INT NOT NULL,
  PRIMARY KEY (`Id`),
  KEY idx_clients_year_month (`year`, `month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 1. Таблица удаленных пользователей на основе Clients.
CREATE TABLE delete_users LIKE Clients;

-- 2. Поле date_delete с текущей меткой времени по умолчанию.
ALTER TABLE delete_users
  ADD COLUMN date_delete TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- 4. Таблица количества удаленных пользователей по месяцам.
CREATE TABLE delete_users_by_month (
  `year` INT NOT NULL,
  `month` INT NOT NULL,
  deleted_count INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`year`, `month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DELIMITER //

-- 3. При удалении из Clients запись попадает в delete_users.
CREATE TRIGGER trg_clients_after_delete
AFTER DELETE ON Clients
FOR EACH ROW
BEGIN
  INSERT INTO delete_users (
    Id, FirstName, LastName, Phone, Email, `year`, `month`, capital, date_delete
  )
  VALUES (
    OLD.Id, OLD.FirstName, OLD.LastName, OLD.Phone, OLD.Email,
    OLD.`year`, OLD.`month`, OLD.capital, CURRENT_TIMESTAMP
  );
END//

-- Общая логика пересчета месяца после вставки в архив.
CREATE TRIGGER trg_delete_users_after_insert
AFTER INSERT ON delete_users
FOR EACH ROW
BEGIN
  INSERT INTO delete_users_by_month (`year`, `month`, deleted_count)
  SELECT NEW.`year`, NEW.`month`, COUNT(*)
  FROM delete_users
  WHERE `year` = NEW.`year`
    AND `month` = NEW.`month`
  ON DUPLICATE KEY UPDATE deleted_count = VALUES(deleted_count);
END//

-- Общая логика пересчета месяца после удаления из архива.
CREATE TRIGGER trg_delete_users_after_delete
AFTER DELETE ON delete_users
FOR EACH ROW
BEGIN
  INSERT INTO delete_users_by_month (`year`, `month`, deleted_count)
  SELECT OLD.`year`, OLD.`month`, COUNT(*)
  FROM delete_users
  WHERE `year` = OLD.`year`
    AND `month` = OLD.`month`
  ON DUPLICATE KEY UPDATE deleted_count = VALUES(deleted_count);

  DELETE FROM delete_users_by_month
  WHERE `year` = OLD.`year`
    AND `month` = OLD.`month`
    AND deleted_count = 0;
END//

DELIMITER ;

INSERT INTO Clients (Id, FirstName, LastName, Phone, Email, `year`, `month`, capital) VALUES
(1, 'Ivan', 'Ivanov', '+70000000001', 'i@mail.ru', 2020, 1, 1000),
(2, 'Petr', 'Petrov', '+70000000002', 'p@mail.ru', 2020, 1, 2000),
(3, 'Anna', 'Sidorova', '+70000000003', 'a@mail.ru', 2020, 2, 3000);

DELETE FROM Clients WHERE Id IN (1, 3);

SELECT * FROM delete_users;
SELECT * FROM delete_users_by_month;

