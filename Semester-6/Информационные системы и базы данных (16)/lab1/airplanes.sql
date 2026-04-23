-- 1. Создание таблиц

-- Таблица "Маршрут"
CREATE TABLE Marshrut (
    id INT AUTO_INCREMENT PRIMARY KEY,
    punkt_vyleta VARCHAR(50) NOT NULL,
    punkt_naznacheniya VARCHAR(50) NOT NULL,
    rasstoyanie INT NOT NULL
);

-- Таблица "Самолет"
CREATE TABLE Samolet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomer VARCHAR(10) NOT NULL UNIQUE,
    marka VARCHAR(30) NOT NULL,
    chislo_mest INT NOT NULL,
    skorost_poleta INT NOT NULL
);

-- Таблица "Рейс"
CREATE TABLE Reis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    samolet_id INT NOT NULL,
    marshrut_id INT NOT NULL,
    data_vremya_vyleta TIMESTAMP NOT NULL,
    data_vremya_pribytiya TIMESTAMP NOT NULL,
    kolichestvo_prodannykh_biletov INT NOT NULL,
    FOREIGN KEY (samolet_id) REFERENCES Samolet(id),
    FOREIGN KEY (marshrut_id) REFERENCES Marshrut(id)
);

-- Индексы по внешним ключам (рекомендуется для ускорения поиска)
CREATE INDEX idx_reis_samolet_id ON Reis(samolet_id);
CREATE INDEX idx_reis_marshrut_id ON Reis(marshrut_id);

-----------------------------------------------------------
-- 2. Заполнение таблиц данными

-- Вставка маршрутов
INSERT INTO Marshrut (punkt_vyleta, punkt_naznacheniya, rasstoyanie) VALUES
('Москва', 'Санкт-Петербург', 700),
('Москва', 'Казань', 720),
('Казань', 'Екатеринбург', 900);

-- Вставка самолетов
INSERT INTO Samolet (nomer, marka, chislo_mest, skorost_poleta) VALUES
('SU1001', 'Сухой Суперджет 100', 75, 830),
('AN148', 'Антонов 148', 85, 870),
('TU154', 'Ту-154', 140, 950);

-- Вставка рейсов
INSERT INTO Reis (samolet_id, marshrut_id, data_vremya_vyleta, data_vremya_pribytiya, kolichestvo_prodannykh_biletov) VALUES
(1, 1, '2024-06-01 09:00', '2024-06-01 10:30', 70),
(2, 2, '2024-06-01 11:00', '2024-06-01 12:40', 80),
(3, 3, '2024-06-02 13:00', '2024-06-02 14:30', 120);

-----------------------------------------------------------
-- 3. Запросы на проверку связей

-- Пример вывода инфо по рейсам с деталями по самолету и маршруту
SELECT
    R.id AS reis_number,
    S.nomer AS samolet_nomer,
    S.marka,
    M.punkt_vyleta,
    M.punkt_naznacheniya,
    R.data_vremya_vyleta,
    R.data_vremya_pribytiya,
    R.kolichestvo_prodannykh_biletov
FROM Reis R
JOIN Samolet S ON R.samolet_id = S.id
JOIN Marshrut M ON R.marshrut_id = M.id;

-- Структура и примерные данные полностью соответствуют схеме на вашем рисунке!
