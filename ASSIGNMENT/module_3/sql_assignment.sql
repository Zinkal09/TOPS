use assignment_3;

-- Customers
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    cust_name VARCHAR(50),
    city VARCHAR(50),
    grade INT,
    salesman_id INT
);

INSERT INTO customers VALUES
(1, 'Alice', 'New York', 120, 101),
(2, 'Bob', 'Los Angeles', 95, 102),
(3, 'Charlie', 'New York', 90, 101),
(4, 'David', 'Chicago', 105, 103),
(5, 'Eve', 'New York', 110, 104);

-- Orders
CREATE TABLE orders (
    order_no INT PRIMARY KEY,
    purchase_amount DECIMAL(10,2),
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO orders VALUES
(1001, 3500.00, 1),
(1002, 4200.00, 2),
(1003, 1000.00, 3),
(1004, 5500.00, 4),
(1005, 7000.00, 5);

-- Departments
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50),
    location VARCHAR(50)
);

INSERT INTO departments VALUES
(10, 'Finance', 'New York'),
(20, 'Marketing', 'Toronto'),
(40, 'HR', 'Chicago'),
(80, 'IT', 'Toronto');

-- Jobs
CREATE TABLE jobs (
    job_id VARCHAR(10) PRIMARY KEY,
    job_title VARCHAR(50),
    min_salary DECIMAL(10,2),
    max_salary DECIMAL(10,2)
);

INSERT INTO jobs VALUES
('AD_VP', 'Admin VP', 5000, 15000),
('IT_PROG', 'Programmer', 4000, 10000),
('MK_MAN', 'Marketing Manager', 6000, 12000),
('FI_ACCOUNT', 'Accountant', 3000, 8000);

-- Employees
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    job_id VARCHAR(10),
    salary DECIMAL(10,2),
    commission_pct DECIMAL(5,2),
    department_id INT,
    manager_id INT,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

INSERT INTO employees VALUES
(101, 'John', 'Smith', 'MK_MAN', 8000, NULL, 20, 201),
(102, 'Jane', 'Doe', 'IT_PROG', 6000, 0.05, 80, 201),
(103, 'Mike', 'Brown', 'FI_ACCOUNT', 7500, 0.1, 10, 201),
(104, 'Sara', 'Connor', 'AD_VP', 12000, NULL, 40, 201),
(105, 'Will', 'White', 'IT_PROG', 5000, 0.03, 80, 201),
(106, 'Nina', 'Grey', 'FI_ACCOUNT', 7000, NULL, 10, 201),
(169, 'Lily', 'Rose', 'IT_PROG', 6500, NULL, 80, 201),
(182, 'Ethan', 'Hunt', 'MK_MAN', 9000, NULL, 20, 201);

-- Products
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    price DECIMAL(10,2)
);

INSERT INTO products VALUES
(1, 'Laptop', 1000.00),
(2, 'Mouse', 25.50),
(3, 'Keyboard', 45.00),
(4, 'Monitor', 200.00),
(5, 'Printer', 150.00);

-- /////////////////1//////////////////

SELECT customer_id, cust_name, city, grade, salesman_id
FROM customers
WHERE city = 'New York' OR grade <= 100;

-- /////////////////2//////////////////////
SELECT customer_id, cust_name, city, grade, salesman_id
FROM customers
WHERE city = 'New York' AND grade > 100;
--

-- ////////////////////////3////////////////////

SELECT order_no,purchase_amount,
(purchase_amount / 6000) * 100 AS achieved_percent,
(100 - ((purchase_amount / 6000) * 100) )AS unachieved_percent
FROM orders
WHERE purchase_amount > 3000;

-- //////////////////4///////////////////////////

SELECT SUM(purchase_amount) AS total_purchase_amount
FROM orders;

-- ////////////5////////////////////////////
SELECT customer_id, MAX(purchase_amount) AS max_purchase
FROM orders
GROUP BY customer_id;

-- //////////////////6 ///////////////////////

SELECT AVG(price) AS average_product_price
FROM products;

-- ////////////////7///////////////////

SELECT first_name, last_name, employee_id, job_id
FROM employees e
JOIN departments d 
ON e.department_id = d.department_id
WHERE d.location = 'Toronto';

-- //////////////8///////////////////////

SELECT employee_id, first_name, last_name, job_id
FROM employees
WHERE salary < (
    SELECT MIN(salary)
    FROM employees
    WHERE job_id = 'MK_MAN'
)
AND job_id != 'MK_MAN';

-- ////////////////////9///////////////////
SELECT first_name, last_name, d.department_id, department_name
FROM employees e
JOIN departments d ON 
e.department_id = d.department_id
WHERE e.department_id IN (80, 40);
-- ////////////////////////10////////////////////////
SELECT d.department_name,
       ROUND(AVG(e.salary), 2) AS average_salary,
       COUNT(e.commission_pct) AS num_employees_with_commission
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name;
-- ////////////////////////////11////////////////////////
SELECT first_name, last_name, department_id, job_id
FROM employees
WHERE job_id = (
    SELECT job_id FROM employees WHERE employee_id = 169
);

-- ////////////////////////////12/////////////////////////

SELECT employee_id, first_name, last_name
FROM employees
WHERE salary > (
    SELECT AVG(salary) FROM employees
);

-- ////////////////////13////////////////////
SELECT d.department_id, first_name, job_id, department_name
FROM employees e
JOIN departments d 
ON e.department_id = d.department_id
WHERE d.department_name = 'Finance';

-- //////////////////14///////////////////
SELECT first_name, last_name, salary
FROM employees
WHERE salary < (
    SELECT salary FROM employees WHERE employee_id = 182
);

-- /////////////////////15/////////////////
DELIMITER $$

CREATE PROCEDURE CountEmployeesByDept()
BEGIN
    SELECT department_id, COUNT(*) AS total_employees
    FROM employees
    GROUP BY department_id;
END $$

DELIMITER ;


-- ////////////////////////16//////////////////////////
DELIMITER $$
-- /////////////////18//////////////////////////////
CREATE PROCEDURE GetTopPaidEmployees()
BEGIN
    SELECT e.department_id, d.department_name, e.first_name, e.last_name, e.salary
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE (e.department_id, e.salary) IN (
        SELECT department_id, MAX(salary)
        FROM employees
        GROUP BY department_id
    );
END $$

DELIMITER ;

-- ///////////////////////19///////////////////////
DELIMITER $$

CREATE PROCEDURE PromoteEmployee (
    IN p_employee_id INT,
    IN p_new_salary DECIMAL(10,2),
    IN p_new_job_id VARCHAR(10)
)
BEGIN
    UPDATE employees
    SET salary = p_new_salary,
        job_id = p_new_job_id
    WHERE employee_id = p_employee_id;
END $$

DELIMITER ;

-- //////////////////////20/////////////////
DELIMITER $$

CREATE PROCEDURE AssignManagerToDepartment (
    IN p_department_id INT,
    IN p_new_manager_id INT
)
BEGIN
    UPDATE employees
    SET manager_id = p_new_manager_id
    WHERE department_id = p_department_id;
END $$

DELIMITER ;



