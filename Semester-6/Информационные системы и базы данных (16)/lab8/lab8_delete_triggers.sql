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

-- 1. Создание таблицы delete_users (структура аналогична Clients)
CREATE TABLE delete_users LIKE Clients;

-- Переносим все ключи и ограничения (если были внешние ключи или индексы - они будут скопированы, если в Clients их нет, этот шаг условен).

-- 2. Добавление в end таблицы delete_users поля date_delete (метка времени по умолчанию)
ALTER TABLE delete_users
ADD COLUMN date_delete TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- 3. Добавим триггер, который при удалении записи из Clients вставляет её в delete_users
DELIMITER $$
CREATE TRIGGER trg_clients_after_delete
AFTER DELETE ON Clients
FOR EACH ROW
BEGIN
    INSERT INTO delete_users (Id, FirstName, LastName, Phone, Email, year, month, capital)
    VALUES (OLD.Id, OLD.FirstName, OLD.LastName, OLD.Phone, OLD.Email, OLD.year, OLD.month, OLD.capital);
    -- поле date_delete заполнится автоматически CURRENT_TIMESTAMP
END;
$$
DELIMITER ;

-- 4. Создание таблицы delete_users_by_month
CREATE TABLE delete_users_by_month (
    year INT NOT NULL,
    month INT NOT NULL,
    count_deleted INT NOT NULL DEFAULT 0,
    PRIMARY KEY (year, month)
);

-- 5. При добавлении записи в delete_users увеличиваем count_deleted по month/year
DELIMITER $$
CREATE TRIGGER trg_delete_users_after_insert
AFTER INSERT ON delete_users
FOR EACH ROW
BEGIN
    INSERT INTO delete_users_by_month (year, month, count_deleted)
    VALUES (NEW.year, NEW.month, 1)
    ON DUPLICATE KEY UPDATE count_deleted = count_deleted + 1;
END;
$$
DELIMITER ;

-- 6. При удалении записи из delete_users уменьшаем count_deleted
DELIMITER $$
CREATE TRIGGER trg_delete_users_after_delete
AFTER DELETE ON delete_users
FOR EACH ROW
BEGIN
    UPDATE delete_users_by_month
    SET count_deleted = count_deleted - 1
    WHERE year = OLD.year AND month = OLD.month;
    -- Если значение стало 0, можно удалить запись, если требуется:
    DELETE FROM delete_users_by_month
    WHERE year = OLD.year AND month = OLD.month AND count_deleted <= 0;
END;
$$
DELIMITER ;
