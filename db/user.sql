INSERT INTO "user" (login, hashed_password, balance)
VALUES ('login', 'hashed_password', 1000);

SELECT * from "user";

UPDATE "user"
SET "balance" = 2000, "is_verified" = true
WHERE "id" = 1;

DELETE FROM "user"
WHERE "id" = 1;

SELECT
    "transaction".id,
    "transaction".amount,
    "transaction".transaction_type,
    "transaction".created_at
FROM
    "transaction"
JOIN
    "user" ON "user".id = "transaction".user_id
WHERE
    "user".id = 1;
