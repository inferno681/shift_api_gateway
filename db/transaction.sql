INSERT INTO "transaction" (user_id, amount, transaction_type)
VALUES (1, 1500, 'credit');

INSERT INTO "transaction" (user_id, amount, transaction_type)
VALUES (1, 1000, 'debit');

SELECT * from "transaction"
WHERE "user_id" = 1;

UPDATE "transaction"
SET "amount" = 2000
WHERE "id" = 1;

DELETE FROM "transaction"
WHERE "id" = 2;
