DROP TABLE IF EXISTS `invoices_electronics`;
DROP TABLE IF EXISTS `invoices`;
DROP TABLE IF EXISTS `electronics`;
DROP TABLE IF EXISTS `employees`;
DROP TABLE IF EXISTS `customers`;

CREATE TABLE customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(35) NOT NULL,
    last_name VARCHAR(35) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_number CHAR(10) NOT NULL,
    birthday DATE NULL,
    address VARCHAR(70) NOT NULL,
    apt_number VARCHAR(10) NULL,
    city VARCHAR(50) NOT NULL,
    state CHAR(2) NOT NULL,
    zip CHAR(5) NOT NULL,
    PRIMARY KEY (customer_id),
    UNIQUE KEY (email),
    UNIQUE KEY (phone_number)
);



CREATE TABLE employees (
    employee_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(35) NOT NULL,
    last_name VARCHAR(35) NOT NULL,
    ssn CHAR(9) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_number CHAR(10) NOT NULL,
    birthday DATE NOT NULL,
    address VARCHAR(70) NOT NULL,
    apt_number VARCHAR(10) NULL,
    city VARCHAR(50) NOT NULL,
    state CHAR(2) NOT NULL,
    zip CHAR(5) NOT NULL,
    PRIMARY KEY (employee_id),
    UNIQUE KEY (email),
    UNIQUE KEY (phone_number),
    UNIQUE KEY (ssn)
);



CREATE TABLE electronics (
    item_id INT NOT NULL AUTO_INCREMENT,
    make VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    version VARCHAR(50) NULL,
    price DECIMAL(8,2) NOT NULL,
    PRIMARY KEY (item_id)
);



CREATE TABLE invoices (
    invoice_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    employee_id INT NULL DEFAULT NULL,
    total_sale DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (invoice_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL ON UPDATE CASCADE
);



CREATE TABLE invoices_electronics (
    invoice_id INT NOT NULL,
    item_id INT NOT NULL,
    item_quantity INT NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (item_id) REFERENCES electronics(item_id) ON DELETE CASCADE ON UPDATE CASCADE,
	UNIQUE KEY (`invoice_id`,`item_id`)
);



INSERT INTO `customers` (
    `first_name`, 
    `last_name`, 
    `email`,
    `phone_number`,
    `address`,
    `city`,
    `state`,
    `zip`) VALUES (
        "Jim",
        "Smith",
        "jsmith@email.com",
        "5411234567",
        "341 Leaf Street",
        "Buffalo",
        "NY",
        "12345"
    );


INSERT INTO `customers` (
    `first_name`, 
    `last_name`, 
    `email`,
    `phone_number`,
    `address`,
    `city`,
    `state`,
    `zip`) VALUES (
        "Pam",
        "Jones",
        "pjones@email.com",
        "2235419999",
        "894 Tree Street",
        "Los Angeles",
        "CA",
        "90210"
    );


INSERT INTO `customers` (
    `first_name`, 
    `last_name`, 
    `email`,
    `phone_number`,
    `address`,
    `city`,
    `state`,
    `zip`) VALUES (
        "Ron",
        "Mahogany",
        "rmahogany@email.com",
        "1995412247",
        "894 Root Street",
        "Orlando",
        "FL",
        "75315"
    );


INSERT INTO `customers` (
    `first_name`, 
    `last_name`, 
    `email`,
    `phone_number`,
    `address`,
    `city`,
    `state`,
    `zip`) VALUES (
        "Michael",
        "Scott",
        "mscott@email.com",
        "7481620037",
        "894 Paper Street",
        "Scranton",
        "PA",
        "91378"
    );


INSERT INTO `employees` (
    `first_name`, 
    `last_name`, 
    `ssn`,
    `email`,
    `phone_number`,
    `birthday`,
    `address`,
    `city`,
    `state`,
    `zip`) VALUES (
        "Patrick",
        "Longoria",
        "147258931",
        "plongoria@email.com",
        "9291234562",
        "1965-10-15",
        "123 Apple Street",
        "Laramie",
        "WY",
        "23456"
    );


INSERT INTO `employees` (
    `first_name`, 
    `last_name`, 
    `ssn`,
    `email`,
    `phone_number`,
    `birthday`,
    `address`,
    `city`,
    `state`,
    `zip`) VALUES (
        "John",
        "Whitman",
        "369852741",
        "jwhitman@email.com",
        "5591234567",
        "1955-01-05",
        "123 Lebanon Street",
        "Lebanon",
        "OR",
        "97584"
    );


INSERT INTO `employees` (
    `first_name`, 
    `last_name`, 
    `ssn`,
    `email`,
    `phone_number`,
    `birthday`,
    `address`,
    `city`,
    `state`,
    `zip`) VALUES (
        "Bill",
        "Kirkman",
        "946731855",
        "bkirkman@email.com",
        "5031234567",
        "1972-08-20",
        "123 Albany Street",
        "Albany",
        "OR",
        "97331"
    );


INSERT INTO `electronics` (
    `make`, 
    `type`, 
    `model`,
    `version`,
    `price`
    ) VALUES (
        "Samsung",
        "TV",
        "Class QN900A Samsung Neo QLED 8K",
        "1111",
        "5499.99"
    );


INSERT INTO `electronics` (
    `make`, 
    `type`, 
    `model`,
    `version`,
    `price`
    ) VALUES (
        "Pine64",
        "Phone",
        "PinePhone",
        "1.1",
        "149.99"
    );


INSERT INTO `electronics` (
    `make`, 
    `type`, 
    `model`,
    `version`,
    `price`
    ) VALUES (
        "System76",
        "Laptop",
        "Pangolin 15in. Ryzen CPU Radeon AMD",
        "4.1",
        "1199.00"
    );



INSERT INTO `invoices` (
    `employee_id`,
    `customer_id`,
    `total_sale`
) VALUES (
    (SELECT `employee_id` FROM `employees` WHERE `employee_id` = "1"),
    (SELECT `customer_id` FROM `customers` WHERE `customer_id` = "1"),
    "5499.99"
);


INSERT INTO `invoices` (
    `employee_id`,
    `customer_id`,
    `total_sale`
) VALUES (
    (SELECT `employee_id` FROM `employees` WHERE `employee_id` = "3"),
    (SELECT `customer_id` FROM `customers` WHERE `customer_id` = "3"),
    "1348.99"
);


INSERT INTO `invoices` (
    `employee_id`,
    `customer_id`,
    `total_sale`
) VALUES (
    (SELECT `employee_id` FROM `employees` WHERE `employee_id` = "2"),
    (SELECT `customer_id` FROM `customers` WHERE `customer_id` = "2"),
    "149.99"
);


INSERT INTO `invoices_electronics` (
    `invoice_id`,
    `item_id`,
    `item_quantity`
) VALUES (
    (SELECT `invoice_id` FROM `invoices` WHERE `invoice_id` = "1"),
    (SELECT `item_id` FROM `electronics` WHERE `item_id` = "1"),
    "1"
);


INSERT INTO `invoices_electronics` (
    `invoice_id`,
    `item_id`,
    `item_quantity`
) VALUES (
    (SELECT `invoice_id` FROM `invoices` WHERE `invoice_id` = "2"),
    (SELECT `item_id` FROM `electronics` WHERE `item_id` = "2"),
    "1"
);


INSERT INTO `invoices_electronics` (
    `invoice_id`,
    `item_id`,
    `item_quantity`
) VALUES (
    (SELECT `invoice_id` FROM `invoices` WHERE `invoice_id` = "2"),
    (SELECT `item_id` FROM `electronics` WHERE `item_id` = "3"),
    "1"
);


INSERT INTO `invoices_electronics` (
    `invoice_id`,
    `item_id`,
    `item_quantity`
) VALUES (
    (SELECT `invoice_id` FROM `invoices` WHERE `invoice_id` = "3"),
    (SELECT `item_id` FROM `electronics` WHERE `item_id` = "2"),
    "1"
);
