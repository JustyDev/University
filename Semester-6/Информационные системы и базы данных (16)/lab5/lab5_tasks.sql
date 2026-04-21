-- Лабораторная работа 5

-- ============================
-- Задание 5.1 — Показатели отказов
-- ============================

CREATE TABLE lr5_users (
    user_id INT,
    action VARCHAR(10),
    act_date DATE
);

INSERT INTO lr5_users (user_id, action, act_date) VALUES
(1, 'start',  '2025-01-01'),
(1, 'cancel', '2025-01-02'),
(2, 'start',  '2025-01-03'),
(2, 'publish','2025-01-04'),
(3, 'start',  '2025-01-05'),
(3, 'cancel', '2025-01-06'),
(1, 'start',  '2025-01-07'),
(1, 'publish','2025-01-08'),
(4, 'start',  '2025-01-09');

-- Запрос 5.1 (publish_rate и cancel_rate для каждого пользователя)
SELECT
   user_id,
   SUM(action = 'publish') / NULLIF(SUM(action = 'start'), 0) AS publish_rate,
   SUM(action = 'cancel') / NULLIF(SUM(action = 'start'), 0) AS cancel_rate
FROM lr5_users
GROUP BY user_id
ORDER BY user_id;
-- В MySQL логические выражения считаются за 1 (TRUE) и 0 (FALSE), деление выдаст верные доли.

-- ============================
-- Задание 5.2 — Изменения в капитале
-- ============================

CREATE TABLE lr5_transactions (
    sender INT,
    receiver INT,
    amount INT,
    transaction_date DATE
);

INSERT INTO lr5_transactions (sender, receiver, amount, transaction_date) VALUES
(5, 2, 10, '2020-02-12'),
(1, 3, 15, '2020-02-13'),
(2, 1, 20, '2020-02-13'),
(3, 2, 25, '2020-02-14'),
(3, 1, 20, '2020-02-15'),
(2, 3, 15, '2020-02-15'),
(1, 4, 5,  '2020-02-16');

-- Запрос 5.2 (итоговое изменение капитала, отсортировано по убыванию)
SELECT
    u.user AS user,
    SUM(u.net_change) AS net_change
FROM (
    SELECT sender AS user, -amount AS net_change FROM lr5_transactions
    UNION ALL
    SELECT receiver AS user, amount AS net_change FROM lr5_transactions
) u
GROUP BY u.user
ORDER BY net_change DESC, user ASC;
