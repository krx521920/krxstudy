-- Learning fixture. Run only in a NEW, EMPTY practice database.
-- Amounts are integer cents. Dates are business dates in Asia/Shanghai.
-- SQLite users: enable PRAGMA foreign_keys = ON before loading this file.
-- No DROP, DELETE, external connection, or real customer data is used.
BEGIN;

CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  customer_name VARCHAR(80) NOT NULL,
  city VARCHAR(40) NOT NULL
);
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_name VARCHAR(80) NOT NULL,
  category VARCHAR(40) NOT NULL
);
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
  created_day DATE NOT NULL,
  paid_day DATE,
  status VARCHAR(12) NOT NULL CHECK (status IN ('paid', 'pending', 'cancelled')),
  amount_cents INTEGER NOT NULL CHECK (amount_cents >= 0),
  CHECK ((status = 'paid' AND paid_day IS NOT NULL)
      OR (status <> 'paid' AND paid_day IS NULL))
);
CREATE TABLE order_items (
  order_id INTEGER NOT NULL REFERENCES orders(order_id),
  line_no INTEGER NOT NULL CHECK (line_no > 0),
  product_id INTEGER NOT NULL REFERENCES products(product_id),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
  PRIMARY KEY (order_id, line_no)
);
CREATE TABLE refunds (
  refund_id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(order_id),
  refund_day DATE NOT NULL,
  amount_cents INTEGER NOT NULL CHECK (amount_cents > 0)
);
CREATE TABLE calendar (day DATE PRIMARY KEY);
CREATE TABLE inventory (
  product_id INTEGER PRIMARY KEY REFERENCES products(product_id),
  stock INTEGER NOT NULL CHECK (stock >= 0),
  version INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE raw_contacts (
  source_id INTEGER PRIMARY KEY,
  email_raw VARCHAR(200),
  name_raw VARCHAR(100),
  updated_day DATE NOT NULL
);

INSERT INTO customers VALUES
  (1, '小林', '上海'), (2, '小周', '北京'), (3, '小陈', '上海'),
  (4, '小吴', '深圳'), (5, '小赵', '杭州');
INSERT INTO products VALUES
  (10, '键盘', '外设'), (20, '鼠标', '外设'), (30, '连接线', '配件');
INSERT INTO orders VALUES
  (101, 1, '2026-08-01', '2026-08-01', 'paid', 15000),
  (102, 1, '2026-08-02', '2026-08-02', 'paid', 5000),
  (103, 2, '2026-08-02', '2026-08-02', 'paid', 20000),
  (104, 2, '2026-08-03', NULL, 'cancelled', 10000),
  (105, 3, '2026-08-04', '2026-08-04', 'paid', 12000),
  (106, 1, '2026-08-04', '2026-08-04', 'paid', 20000),
  (107, 3, '2026-08-05', NULL, 'pending', 10000),
  (108, 2, '2026-08-06', '2026-08-06', 'paid', 5000),
  (109, 3, '2026-08-06', '2026-08-06', 'paid', 5000),
  (110, 5, '2026-08-06', NULL, 'pending', 2000);
INSERT INTO order_items VALUES
  (101, 1, 10, 1, 10000), (101, 2, 20, 1, 5000),
  (102, 1, 20, 1, 5000), (103, 1, 10, 2, 10000),
  (104, 1, 10, 1, 10000),
  (105, 1, 10, 1, 10000), (105, 2, 30, 1, 2000),
  (106, 1, 10, 2, 10000), (107, 1, 10, 1, 10000),
  (108, 1, 20, 1, 5000), (109, 1, 20, 1, 5000),
  (110, 1, 30, 1, 2000);
INSERT INTO refunds VALUES
  (1, 101, '2026-08-05', 2000),
  (2, 101, '2026-08-06', 1000),
  (3, 105, '2026-08-07', 2000);
INSERT INTO calendar VALUES
  ('2026-08-01'), ('2026-08-02'), ('2026-08-03'), ('2026-08-04'),
  ('2026-08-05'), ('2026-08-06'), ('2026-08-07');
INSERT INTO inventory VALUES (10, 1, 0);
INSERT INTO raw_contacts VALUES
  (1, ' Alice@Example.COM ', ' Alice ', '2026-08-01'),
  (2, 'alice@example.com', 'Alice Li', '2026-08-02'),
  (3, '', 'No Email', '2026-08-03'),
  (4, NULL, 'Null Email', '2026-08-04'),
  (5, 'BOB@example.com', ' Bob ', '2026-08-01'),
  (6, 'bob@example.com', 'Bob New', '2026-08-02'),
  (7, ' not-an-email ', 'Bad', '2026-08-03'),
  (8, ' CAROL@example.com ', 'Carol', '2026-08-03');
COMMIT;
