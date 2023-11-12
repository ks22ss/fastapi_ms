CREATE TABLE fastms.user (
  email VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255),
  signup_ts TIMESTAMP default CURRENT_TIMESTAMP
);

CREATE TABLE fastms.product (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  model VARCHAR(255),
  price VARCHAR(255),
  description VARCHAR(255),
  start_date TIMESTAMP
);

CREATE TABLE fastms.customer (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  address VARCHAR(255),
  phone VARCHAR(255),
  signup_ts TIMESTAMP default CURRENT_TIMESTAMP
);

CREATE TABLE fastms.orders (
  id SERIAL PRIMARY KEY,
  qty INT,
  product_id INT,
  order_date TIMESTAMP default CURRENT_TIMESTAMP,
  ship_date TIMESTAMP,
  service_officer VARCHAR(255),
  customer_id INT,
  foreign key (product_id) references fastms.product (id),
  foreign key (service_officer) references fastms.user (email),
  foreign key (customer_id) references fastms.customer (id)
);

