CREATE EXTENSION IF NOT EXISTS vector;

CREATE TYPE "transaction_type" AS ENUM (
  'credit',
  'debit'
);

CREATE TABLE "user" (
  "id" serial PRIMARY KEY,
  "login" varchar UNIQUE,
  "hashed_password" varchar,
  "balance" integer,
  "is_verified" bool DEFAULT false
);

CREATE TABLE "token" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "token" varchar
);

CREATE TABLE "transaction" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "amount" integer,
  "transaction_type" transaction_type,
  "created_at" timestamp DEFAULT 'now()'
);

CREATE TABLE "report" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "start_date" timestamp,
  "end_date" timestamp,
  "debit" integer,
  "credit" integer
);

CREATE TABLE "embedding" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "embedding" vector(128)
);

ALTER TABLE "token" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "embedding" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "transaction" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "report" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

CREATE TABLE "report_transaction" (
  "report_id" serial,
  "transaction_id" serial,
  PRIMARY KEY ("report_id", "transaction_id")
);

ALTER TABLE "report_transaction" ADD FOREIGN KEY ("report_id") REFERENCES "report" ("id");

ALTER TABLE "report_transaction" ADD FOREIGN KEY ("transaction_id") REFERENCES "transaction" ("id");
