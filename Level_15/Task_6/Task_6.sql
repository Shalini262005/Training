USE shopping;
CREATE TABLE customers (customer_id VARCHAR(20) NOT NULL PRIMARY KEY, gender VARCHAR(10) NOT NULL, age INT NOT NULL);
CREATE TABLE shopping_malls (mall_id INT AUTO_INCREMENT PRIMARY KEY, mall_name VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE payment_methods (payment_id INT AUTO_INCREMENT PRIMARY KEY, payment_method VARCHAR(50) NOT NULL UNIQUE);
CREATE TABLE categories (category_id INT AUTO_INCREMENT PRIMARY KEY, category_name VARCHAR(100) NOT NULL UNIQUE);
CREATE TABLE invoices (invoice_no VARCHAR(20) NOT NULL PRIMARY KEY, customer_id VARCHAR(20) NOT NULL, mall_id INT NOT NULL, payment_id INT NOT NULL, invoice_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE, FOREIGN KEY (mall_id) REFERENCES shopping_malls(mall_id) ON DELETE CASCADE, FOREIGN KEY (payment_id) REFERENCES payment_methods(payment_id) ON DELETE CASCADE);
CREATE TABLE invoice_items (invoice_item_id INT AUTO_INCREMENT PRIMARY KEY, invoice_no VARCHAR(20) NOT NULL, category_id INT NOT NULL, quantity INT NOT NULL, price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (invoice_no) REFERENCES invoices(invoice_no) ON DELETE CASCADE, FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE);
INSERT INTO shopping_malls (mall_name)
SELECT DISTINCT shopping_mall FROM customer_shopping_data;

INSERT INTO payment_methods (payment_method)
SELECT DISTINCT payment_method FROM customer_shopping_data;

INSERT INTO categories (category_name)
SELECT DISTINCT category FROM customer_shopping_data;

INSERT INTO customers (customer_id, gender, age)
SELECT DISTINCT customer_id, gender, age FROM customer_shopping_data;

INSERT INTO invoices (invoice_no, customer_id, mall_id, payment_id, invoice_date)
SELECT c.invoice_no, c.customer_id, m.mall_id, p.payment_id, STR_TO_DATE(c.invoice_date, '%d/%m/%Y')
FROM customer_shopping_data c
JOIN shopping_malls m ON c.shopping_mall = m.mall_name
JOIN payment_methods p ON c.payment_method = p.payment_method;

INSERT INTO invoice_items (invoice_no, category_id, quantity, price)
SELECT c.invoice_no, cat.category_id, c.quantity, c.price
FROM customer_shopping_data c
JOIN categories cat ON c.category = cat.category_name;
    
select*from customers;
select*from categories;
select*from shopping_malls;
select*from payment_methods;
select*from invoices;
select*from invoice_items;

