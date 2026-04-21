-- Лабораторная работа 2.
-- Запросы по тексту Word-файла. MySQL 8.0+

CREATE DATABASE IF NOT EXISTS library_lab2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE library_lab2;

DROP TABLE IF EXISTS book_loans;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS readers;

CREATE TABLE readers (
  reader_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  full_name VARCHAR(120) NOT NULL,
  PRIMARY KEY (reader_id),
  KEY idx_readers_full_name (full_name)
) ENGINE=InnoDB;

CREATE TABLE books (
  book_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(160) NOT NULL,
  PRIMARY KEY (book_id),
  KEY idx_books_title (title)
) ENGINE=InnoDB;

CREATE TABLE book_loans (
  loan_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  book_id INT UNSIGNED NOT NULL,
  reader_id INT UNSIGNED NOT NULL,
  issue_date DATE NOT NULL,
  return_date DATE NULL,
  PRIMARY KEY (loan_id),
  KEY idx_book_loans_issue_date (issue_date),
  KEY idx_book_loans_return_date (return_date),
  CONSTRAINT fk_book_loans_book
    FOREIGN KEY (book_id) REFERENCES books (book_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_book_loans_reader
    FOREIGN KEY (reader_id) REFERENCES readers (reader_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

INSERT INTO readers (full_name) VALUES
('Alice Brown'),
('Charles Green'),
('George Adams'),
('Helen Stone');

INSERT INTO books (title) VALUES
('Databases'),
('SQL Practice'),
('Algorithms'),
('Networks');

INSERT INTO book_loans (book_id, reader_id, issue_date, return_date) VALUES
(1, 1, '2003-10-03', NULL),
(2, 2, '2003-10-04', '2003-10-12'),
(3, 3, '2003-10-05', NULL),
(4, 4, '2003-10-03', '2003-10-20');

-- 1. Все книги, выданные 3 и 4 октября 2003 г. с использованием IN.
SELECT b.book_id, b.title, bl.issue_date, r.full_name
FROM book_loans bl
JOIN books b ON b.book_id = bl.book_id
JOIN readers r ON r.reader_id = bl.reader_id
WHERE bl.issue_date IN ('2003-10-03', '2003-10-04');

-- 1. То же условие с использованием BETWEEN.
SELECT b.book_id, b.title, bl.issue_date, r.full_name
FROM book_loans bl
JOIN books b ON b.book_id = bl.book_id
JOIN readers r ON r.reader_id = bl.reader_id
WHERE bl.issue_date BETWEEN '2003-10-03' AND '2003-10-04';

-- 2. Все читатели, чьи имена начинаются с буквы в диапазоне от A до G.
SELECT reader_id, full_name
FROM readers
WHERE LEFT(full_name, 1) BETWEEN 'A' AND 'G';

-- 3. Все читатели, чьи имена начинаются с C.
SELECT reader_id, full_name
FROM readers
WHERE full_name LIKE 'C%';

-- 4. Все книги с нулевым/NULL значением в поле возврата.
SELECT b.book_id, b.title, bl.issue_date, bl.return_date, r.full_name
FROM book_loans bl
JOIN books b ON b.book_id = bl.book_id
JOIN readers r ON r.reader_id = bl.reader_id
WHERE bl.return_date IS NULL OR bl.return_date = '0000-00-00';

