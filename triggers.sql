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
-- Delete Product Trigger
CREATE TABLE product_delete(
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL,
    description TEXT NOT NULL,
    deleted_on TIMESTAMP(6) NOT NULL
);
CREATE OR REPLACE FUNCTION log_product_delete() RETURNS trigger AS $product_stamp_del$ BEGIN
INSERT INTO product_delete(
        product_id,
        name,
        price,
        description,
        deleted_on
    )
VALUES(
        OLD.id,
        OLD.name,
        OLD.price,
        OLD.description,
        NOW()
    );
RETURN OLD;
END;
$product_stamp_del$ LANGUAGE plpgsql;
CREATE TRIGGER deleted_product BEFORE DELETE ON products FOR EACH ROW EXECUTE PROCEDURE log_product_delete();
-- Delete Purchases Trigger
CREATE TABLE purchases_delete(
    id SERIAL PRIMARY KEY,
    purchase_id INT NOT NULL,
    quantity INT NOT NULL,
    date_purchases VARCHAR(20) NOT NULL,
    client_id INT NOT NULL,
    client_name VARCHAR(50) NOT NULL,
    product_id INT,
    product_name VARCHAR(50),
    deleted_on TIMESTAMP(6) NOT NULL
);
CREATE OR REPLACE FUNCTION log_purchases_delete() RETURNS trigger AS $purchases_stamp_delete$ BEGIN
INSERT INTO purchases_delete(
        purchase_id,
        quantity,
        date_purchases,
        client_id,
        client_name,
        product_id,
        product_name,
        deleted_on
    )
SELECT pu.id as purchase_id,
    pu.quantity as quantity,
    pu.date_purchase as date_purchases,
    c.id as client_id,
    c.name as client_name,
    pr.id as product_id,
    pr.name as product_name,
    NOW() as deleted_on
FROM purchases pu,
    users c,
    products pr
WHERE pu.client_id = c.id
    AND pu.product_id = pr.id
    AND pu.id = OLD.ID;
RETURN OLD;
END;
$purchases_stamp_delete$ LANGUAGE plpgsql;
CREATE TRIGGER remove_purchases BEFORE DELETE ON purchases FOR EACH ROW EXECUTE PROCEDURE log_purchases_delete();