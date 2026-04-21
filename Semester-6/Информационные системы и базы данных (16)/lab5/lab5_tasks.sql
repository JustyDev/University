-- Лабораторная работа 5. MySQL 8.0+

CREATE DATABASE IF NOT EXISTS lab5_tasks
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE lab5_tasks;

-- Задание 5.1. Показатели отказов.
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id INT NOT NULL,
  action ENUM('start', 'cancel', 'publish') NOT NULL,
  action_date DATE NOT NULL,
  KEY idx_users_user_action (user_id, action),
  KEY idx_users_date (action_date)
) ENGINE=InnoDB;

INSERT INTO users (user_id, action, action_date) VALUES
(1, 'start',   '2020-01-01'),
(1, 'cancel',  '2020-01-02'),
(2, 'start',   '2020-01-03'),
(2, 'publish', '2020-01-04'),
(3, 'start',   '2020-01-05'),
(3, 'cancel',  '2020-01-06'),
(1, 'start',   '2020-01-07'),
(1, 'publish', '2020-01-08');

SELECT
  user_id,
  ROUND(100 * SUM(action = 'cancel') / NULLIF(SUM(action = 'start'), 0), 2) AS cancel_percent,
  ROUND(100 * SUM(action = 'publish') / NULLIF(SUM(action = 'start'), 0), 2) AS publish_percent
FROM users
GROUP BY user_id
ORDER BY user_id;

-- Задание 5.2. Изменения в капитале.
DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
  transaction_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  sender_id INT NOT NULL,
  receiver_id INT NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  transaction_date DATE NOT NULL,
  PRIMARY KEY (transaction_id),
  KEY idx_transactions_sender (sender_id),
  KEY idx_transactions_receiver (receiver_id),
  CONSTRAINT chk_transactions_amount CHECK (amount > 0)
) ENGINE=InnoDB;

INSERT INTO transactions (sender_id, receiver_id, amount, transaction_date) VALUES
(1, 2, 100.00, '2020-01-01'),
(2, 3,  50.00, '2020-01-02'),
(3, 1,  35.00, '2020-01-03'),
(1, 3,  20.00, '2020-01-04');

SELECT
  user_id,
  SUM(delta) AS capital_change
FROM (
  SELECT sender_id AS user_id, -amount AS delta
  FROM transactions
  UNION ALL
  SELECT receiver_id AS user_id, amount AS delta
  FROM transactions
) t
GROUP BY user_id
ORDER BY capital_change DESC, user_id;

