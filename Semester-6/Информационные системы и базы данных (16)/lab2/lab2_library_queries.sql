-- Читатели
CREATE TABLE Reader (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Книги
CREATE TABLE Book (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

-- Выдача книг
CREATE TABLE BookIssue (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL,
    reader_id INT NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE, -- может быть NULL, если книгу не вернули
    FOREIGN KEY (book_id) REFERENCES Book(id),
    FOREIGN KEY (reader_id) REFERENCES Reader(id)
);

-- Примерные данные
INSERT INTO Reader (name) VALUES
('Anna Ivanova'),
('Boris Petrov'),
('Galina Smirnova'),
('Dmitry Sokolov'),
('Ekaterina Fedorova'),
('Catherine Miles'),
('George Miller');

INSERT INTO Book (title) VALUES
('SQL For Beginners'),
('War and Peace'),
('Harry Potter'),
('C# Programming');

INSERT INTO BookIssue (book_id, reader_id, issue_date, return_date) VALUES
(1, 1, '2003-10-03', '2003-10-10'),
(2, 2, '2003-10-04', '2003-10-11'),
(3, 3, '2003-10-03', NULL),
(4, 4, '2003-10-02', '2003-10-06'),
(1, 5, '2003-10-04', NULL),
(3, 6, '2003-10-10', NULL),
(2, 7, '2003-09-29', '2003-10-02');



-- 1. Запрос: все книги, выданные 3 и 4 октября 2003 с использованием IN
SELECT * FROM BookIssue
WHERE issue_date IN ('2003-10-03', '2003-10-04');
-- Использование оператора IN для выбора конкретных дат

-- 1. Запрос: все книги, выданные 3 и 4 октября 2003 с использованием BETWEEN
SELECT * FROM BookIssue
WHERE issue_date BETWEEN '2003-10-03' AND '2003-10-04';
-- Использование BETWEEN для выбора диапазона дат

-- 2. Запрос: все читатели, чьи имена начинаются с буквы от 'A' до 'G'
SELECT * FROM Reader
WHERE LEFT(name, 1) BETWEEN 'A' AND 'G';
-- Проверка первой буквы имени в диапазоне от "A" до "G"

-- 3. Запрос: все читатели, чьи имена начинаются с буквы 'C'
SELECT * FROM Reader
WHERE name LIKE 'C%';
-- Поиск по шаблону имени, начинающемуся на "C"

-- 4. Запрос: все книги, имеющие NULL в поле возврата (еще не возвращены)
SELECT * FROM BookIssue
WHERE return_date IS NULL;
-- Выдачи книг, у которых дата возврата отсутствует (книга не возвращена)
