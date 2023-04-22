CREATE TABLE product_audits(
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL,
    description TEXT NOT NULL,
    image VARCHAR(255) NOT NULL,
    changed_on TIMESTAMP(6) NOT NULL
);
CREATE OR REPLACE FUNCTION log_price_changes() RETURNS trigger AS $prod_stamp$ BEGIN IF NEW.price <> OLD.price THEN
INSERT INTO product_audits(
        product_id,
        name,
        price,
        description,
        image,
        changed_on
    )
VALUES(
        OLD.id,
        OLD.name,
        OLD.price,
        OLD.description,
        OLD.image,
        NOW()
    );
END IF;
RETURN NEW;
END;
$prod_stamp$ LANGUAGE plpgsql;
CREATE TRIGGER price_changes BEFORE
UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE log_price_changes();