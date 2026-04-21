-- 1. Создание таблицы users
CREATE TABLE users (
    user_id INT,
    product_id INT,
    transaction_date DATE
);

-- 2. Вставка данных
INSERT INTO users VALUES
(1, 101, '2020-02-12'),
(2, 105, '2020-02-13'),
(1, 111, '2020-02-14'),
(3, 121, '2020-02-15'),
(1, 101, '2020-02-16'),
(2, 105, '2020-02-17'),
(4, 101, '2020-02-18'),
(3, 105, '2020-02-15'); -- (дату для 3 пользователя и product_id=105 подставил по образцу из скриншота)

-- 6.1. Имитация ROW_NUMBER без оконных функций (MySQL 5.x)
-- Найти вторую по времени транзакцию для каждого пользователя

SELECT
    u.user_id,
    MIN(u2.transaction_date) AS superuser_date
FROM
    users u
    JOIN users u2 ON u.user_id = u2.user_id AND u.transaction_date < u2.transaction_date
GROUP BY
    u.user_id
HAVING
    COUNT(*) >= 1

UNION

SELECT
    u.user_id, NULL
FROM
    users u
WHERE
    u.user_id NOT IN (
        SELECT user_id
        FROM users
        GROUP BY user_id
        HAVING COUNT(*) >= 2
    )
GROUP BY u.user_id
ORDER BY user_id;

-- 6.2. Решение с использованием ROW_NUMBER (MySQL 8.0+)

SELECT
    user_id,
    CASE
        WHEN COUNT(*) >= 2 THEN
            MIN(CASE WHEN rn = 2 THEN transaction_date END)
        ELSE NULL
    END AS superuser_date
FROM
(
    SELECT
        user_id,
        transaction_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY transaction_date) AS rn
    FROM users
) t
GROUP BY user_id
ORDER BY user_id;

