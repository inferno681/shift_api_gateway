INSERT INTO report (user_id, start_date, end_date, debit, credit)
SELECT
    t.user_id,
    '2024-01-01 00:00:00'::timestamp AS start_date,
    '2024-12-31 23:59:59'::timestamp AS end_date,
    SUM(CASE WHEN t.transaction_type = 'debit' THEN t.amount ELSE 0 END) AS debit,
    SUM(CASE WHEN t.transaction_type = 'credit' THEN t.amount ELSE 0 END) AS credit
FROM
    transaction t
WHERE
    t.user_id = 1
    AND t.created_at >= '2024-01-01 00:00:00'
    AND t.created_at <= '2024-12-31 23:59:59'
GROUP BY
    t.user_id;
