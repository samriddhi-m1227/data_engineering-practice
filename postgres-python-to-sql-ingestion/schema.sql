DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
  customer_id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name  TEXT NOT NULL,
  address_1  TEXT,
  address_2  TEXT,
  city       TEXT,
  state      TEXT,
  zip_code   TEXT,
  join_date  DATE
);

CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_code TEXT,
  product_description TEXT
);

CREATE TABLE transactions (
  transaction_id TEXT PRIMARY KEY,
  transaction_date DATE NOT NULL,
  product_id INTEGER NOT NULL,
  product_code TEXT,
  product_description TEXT,
  quantity INTEGER NOT NULL,
  account_id INTEGER NOT NULL,
  CONSTRAINT fk_transactions_product
    FOREIGN KEY (product_id) REFERENCES products(product_id),
  CONSTRAINT fk_transactions_account
    FOREIGN KEY (account_id) REFERENCES accounts(customer_id)
);

CREATE INDEX idx_transactions_product_id ON transactions(product_id);
CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
