--==============================================================
--Customers
--==============================================================

--SELECT
-- select an existing customer by id
SELECT * FROM customers WHERE customer_id = :cid

-- INSERT
-- insert a new customer

INSERT INTO customers (first_name, last_name, phone_number, email, address, apt_number, city, state, zip, birthday) VALUES (:fname, :lname, :phone, :email, :address, :apt, :city, :state, :zip, :bday)

--UPDATE
--update an existing customer

UPDATE customers SET first_name=:fname, last_name=:lname, phone_number=:phone, email=:email, address=:address, apt_number=:apt, city=:city, state=:state, zip=:zip, birthday=bday: WHERE customer_id=:cid


--DELETE
--delete an existing customer

DELETE FROM customers WHERE customer_id=:cid

--==============================================================
--Employees
--==============================================================

--SELECT
-- select an existing employee by id
SELECT * FROM employees WHERE employee_id = :eid

--INSERT
-- insert a new employee

INSERT INTO employees (first_name, last_name, ssn, phone_number, email, address, apt_number, city, state, zip, birthday) VALUES (:fname, :lname, :ssn, :phone, :email, :address, :apt, :city, :state, :zip, :bday)

--UPDATE
--update an existing employee

UPDATE employees SET first_name=:fname, last_name=:lname, ssn=:ssn, phone_number=:phone, email=:email, address=:address, apt_number=:apt, city=:city, state=:state, zip=:zip, birthday=:bday WHERE employee_id=:eid

--DELETE
--delete an existing employee

DELETE FROM employees WHERE employee_id=:eid


--==============================================================
--Electronics
--==============================================================

--SELECT
-- select an existing electronic by id
SELECT * FROM electronics WHERE item_id = :itemid

--INSERT
-- insert a new electronics

INSERT INTO electronics (make, type, model, version, price) VALUES (:make, :type, :model, :version, :price)

--UPDATE
--update an existing electronics

UPDATE electronics SET make=:make, type=:type, model=:model, version=:version, price=:price WHERE item_id=:itemid


--DELETE
--delete an existing electronics

DELETE FROM electronics WHERE item_id=:itemid


--==============================================================
--Invoices
--==============================================================

--SELECT
-- select an existing invoice by id
SELECT * FROM invoices WHERE invoice_id = :invoiceid

--INSERT
-- insert a new invoice

INSERT INTO invoices (customer_id, employee_id, total_sale) VALUES (:customer_id, :employee_id, :sale))

--UPDATE
--update an existing invoice

UPDATE invoices SET employee_id=:eid, customer_id=:cid, total_sale=:tsale WHERE invoice_id=:invoiceid 

--DELETE
--delete an existing invoice

DELETE FROM invoices WHERE invoice_id=:invoceid


--==============================================================
--Invoices_electronics
--==============================================================

--SELECT
-- select an existing invoice_electronic record by item id and invoice id
SELECT * FROM electronics WHERE item_id = :itemid AND invoice_id = :invoiceid

--INSERT
-- insert a new invoice_electronic record

INSERT INTO invoices_electronics (invoice_id, item_id, item_quantity) VALUES (:invoice_id, :item_id, :quantity)

--UPDATE
--update an existing invoice_electronic record

UPDATE invoices_electronics SET invoice_id=:invoiceid, item_id=:itemid, item_quantity=:qty WHERE invoice_id=:invoiceid AND item_id=:itemid AND item_quantity=:qty 

--DELETE
--delete an existing invoice_electronic record

DELETE FROM invoices_electronics WHERE invoice_id=:invoiceid AND item_id=:itemid AND item_quantity=:qty
