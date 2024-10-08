CREATE OR REPLACE FUNCTION update_user_balance()
RETURNS TRIGGER AS $$
BEGIN
    -- Handling transaction insertion
    IF TG_OP = 'INSERT' THEN
        IF NEW.transaction_type = 'credit' THEN
            UPDATE "user"
            SET balance = balance + NEW.amount
            WHERE id = NEW.user_id;
        ELSIF NEW.transaction_type = 'debit' THEN
            UPDATE "user"
            SET balance = balance - NEW.amount
            WHERE id = NEW.user_id;
        END IF;
    END IF;

    -- Handling transaction update
    IF TG_OP = 'UPDATE' THEN
        -- If the amount field has changed
        IF NEW.transaction_type = OLD.transaction_type THEN
            IF NEW.transaction_type = 'credit' THEN
                UPDATE "user"
                SET balance = balance - OLD.amount + NEW.amount
                WHERE id = NEW.user_id;
            ELSIF NEW.transaction_type = 'debit' THEN
                UPDATE "user"
                SET balance = balance + OLD.amount - NEW.amount
                WHERE id = NEW.user_id;
            END IF;
        ELSE
            -- If the transaction type has changed
            IF OLD.transaction_type = 'credit' THEN
                UPDATE "user"
                SET balance = balance - OLD.amount
                WHERE id = OLD.user_id;
            ELSIF OLD.transaction_type = 'debit' THEN
                UPDATE "user"
                SET balance = balance + OLD.amount
                WHERE id = OLD.user_id;
            END IF;

            IF NEW.transaction_type = 'credit' THEN
                UPDATE "user"
                SET balance = balance + NEW.amount
                WHERE id = NEW.user_id;
            ELSIF NEW.transaction_type = 'debit' THEN
                UPDATE "user"
                SET balance = balance - NEW.amount
                WHERE id = NEW.user_id;
            END IF;
        END IF;
    END IF;

    -- Handling transaction deletion
    IF TG_OP = 'DELETE' THEN
        IF OLD.transaction_type = 'credit' THEN
            UPDATE "user"
            SET balance = balance - OLD.amount
            WHERE id = OLD.user_id;
        ELSIF OLD.transaction_type = 'debit' THEN
            UPDATE "user"
            SET balance = balance + OLD.amount
            WHERE id = OLD.user_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for inserting and updating transactions
CREATE TRIGGER trigger_update_balance
AFTER INSERT OR UPDATE OR DELETE ON "transaction"
FOR EACH ROW
EXECUTE FUNCTION update_user_balance();
