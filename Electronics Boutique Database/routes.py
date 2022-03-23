from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import yaml

"""
<!-- Citation for using routes, MySQL, and flash messages
    # Citation for the following function:
    # Date: 10/15/2021 - 10/25/2021
    # Copied from /OR/ Adapted from /OR/ Based on: The implementation of how use routes and apply them are in the
    the source urls. The code implemented is based off the tutorials and not a direct copy and paste.
    # Source URL:
        - https://www.youtube.com/playlist?list=PLOkVupluCIjuPtTkhO6jmA76uQR994Wvi
        - https://www.youtube.com/playlist?list=PL1FgJUcJJ03vLZXbAFESDqGKBrDNgi-LG
        - https://www.udemy.com
        - https://stackoverflow.com/
        - https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/ 
-->
"""

# creates a flask app and a secret keep for flash messages
app = Flask(__name__)
app.secret_key = 'A243CE5757B9C3C97A45B38984B66'

# import the mysql credentials from the YAML file and link app to mysql
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PORT'] = db['mysql_port']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# home page
@app.route('/', methods=['POST','GET'])
def home():
    return render_template('home.html')


# ---------------------------------------- CUSTOMERS -----------------------------------------------------------------


# customer page
@app.route('/customers/', methods=['POST','GET'])
def customers():

    # opens up a connection by a cursor and pull the the data and closes it
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    cur.close()

    # the fetched data is stored in customers to it needs to be passed customers.html to put in the table
    return render_template('customers.html', customers=customers)


# this is a route that is used to add customers
@app.route('/add_customer/', methods=['POST', 'GET'])
def add_customer():

    # if it is post method from the form then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        apt = request.form['apt']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        bday = request.form['birthday']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # pull all the phone numbers from the table and check to see if the number already exists
        # if so, send a flash message and redirect back to the customers pages by using redirect module and passed the
        # customers function
        cur.execute("SELECT phone_number FROM customers")
        phones = cur.fetchall()
        for key in phones:
            if key['phone_number'] == phone:
                cur.close()
                flash("Phone Number Already Exists",category='danger')
                return redirect(url_for('customers'))

        # pull all the emails from the table and check to see if the email already exists
        # if so, send a flash message and redirect back to the customers pages by using redirect module and passed the
        # customers function
        cur.execute("SELECT email FROM customers")
        emails = cur.fetchall()
        for key in emails:
            if key['email'] == email:
                cur.close()
                flash("Email Already Exists",category='danger')
                return redirect(url_for('customers'))

        # if the birthday does not exist, then dont insert birthday, else insert everything
        if bday:
            cur.execute("INSERT INTO customers (first_name, last_name, phone_number, email, address, apt_number, city, state, zip, birthday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname,phone,email,address,apt,city,state,zip,bday))
        else:
            cur.execute("INSERT INTO customers (first_name, last_name, phone_number, email, address, apt_number, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, phone, email, address, apt, city, state, zip))

        # commit the changes to mysql, flash a success message, and redirect back to customers
        mysql.connection.commit()
        cur.close()
        flash("Customer Data Added Successfully",category='success')
        return redirect(url_for('customers'))

# this is a route that is used to edit customers
@app.route('/update_customer/',methods=['POST','GET'])
def update_customer():

    # if post then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        cid = request.form['cid']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        apt = request.form['apt']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        bday = request.form['birthday']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # pull all the phone numbers from the table and check to see if the number already exists and is not tied to the current customer
        # if so, send a flash message and redirect back to the customers pages by using redirect module and passed the
        # customers function
        cur.execute("SELECT phone_number, customer_id FROM customers")
        phones = cur.fetchall()
        for key in phones:
            if key['phone_number'] == phone and int(key['customer_id']) != int(cid):
                cur.close()
                flash("Phone Number Already Exists", category='danger')
                return redirect(url_for('customers'))

        # pull all the emails from the table and check to see if the email already exists and is not tied to the current customer
        # if so, send a flash message and redirect back to the customers pages by using redirect module and passed the
        # customers function
        cur.execute("SELECT email, customer_id FROM customers")
        emails = cur.fetchall()
        for key in emails:
            if key['email'] == email and int(key['customer_id']) != int(cid):
                cur.close()
                flash("Email Already Exists", category='danger')
                return redirect(url_for('customers'))

        if apt == 'None':
            apt = ''

        # if the birthday does not exist, then dont update birthday, else update everything
        if bday:
            cur.execute(""" UPDATE customers SET first_name=%s, last_name=%s, phone_number=%s, email=%s, address=%s, apt_number=%s, city=%s, state=%s, zip=%s, birthday=%s WHERE customer_id=%s """, (fname, lname, phone, email, address, apt, city, state, zip, bday, cid))
        else:
            cur.execute(""" UPDATE customers SET first_name=%s, last_name=%s, phone_number=%s, email=%s, address=%s, apt_number=%s, city=%s, state=%s, zip=%s WHERE customer_id=%s """, (fname, lname, phone, email, address, apt, city, state, zip, cid))

        # commit the changes to mysql, flash a success message, and redirect back to customers with edited customer as filter
        mysql.connection.commit()
        cur.execute("SElECT * FROM customers WHERE customer_id=%s", [cid])
        customers = cur.fetchall()
        cur.close()
        flash("Customer Data Edited Successfully",category='success')

        return render_template('customers.html', customers=customers)

@app.route('/delete_customer/',methods=['POST','GET'])
def delete_customer():

    # pull the cid from the form, open a cursor and, delete from table
    cid = request.form['cid']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE customer_id=%s", [cid],)

    # commit to changes to the database and flash a message for successful removal, then redirect back to customers
    mysql.connection.commit()
    cur.close()
    flash("Customer Has Been Removed Successfully",category='success')
    return redirect(url_for('customers'))

# Search customer page
@app.route('/search_customer/', methods=['POST','GET'])
def search_customer():

    # opens up a connection by a cursor and pull the the data and closes it
    cid = request.form['customer_id']
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    apt = request.form['apt']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    bday = request.form['birthday']

    cur = mysql.connection.cursor()

    # build initial query, set AND flag and declare suffix tuple
    initial_query = """SELECT * FROM customers WHERE"""
    and_flag = False
    suffix = ()

    # based on user input build query and suffix
    if cid != "":
        cid_string = " customer_id LIKE %s"
        cid = "%" + cid + "%"
        suffix = suffix + (cid,)
        and_flag = True
        initial_query = initial_query + cid_string
    if fname != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        fname_string = " first_name LIKE %s"
        fname = "%" + fname + "%"
        suffix = suffix + (fname,)
        and_flag = True
        initial_query = initial_query + fname_string
    if lname != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        lname_string = " last_name LIKE %s"
        lname = "%" + lname + "%"
        suffix = suffix + (lname,)
        and_flag = True
        initial_query = initial_query + lname_string
    if phone != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        phone_string = " phone_number LIKE %s"
        phone = "%" + phone + "%"
        suffix = suffix + (phone,)
        and_flag = True
        initial_query = initial_query + phone_string
    if email != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        email_string = " email LIKE %s"
        email = "%" + email + "%"
        suffix = suffix + (email,)
        and_flag = True
        initial_query = initial_query + email_string
    if address != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        address_string = " address LIKE %s"
        address = "%" + address + "%"
        suffix = suffix + (address,)
        and_flag = True
        initial_query = initial_query + address_string
    if apt != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        apt_string = " apt_number LIKE %s"
        apt = "%" + apt + "%"
        suffix = suffix + (apt,)
        and_flag = True
        initial_query = initial_query + apt_string
    if city != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        city_string = " city LIKE %s"
        city = "%" + city + "%"
        suffix = suffix + (city,)
        and_flag = True
        initial_query = initial_query + city_string
    if state != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        state_string = " state LIKE %s"
        state = "%" + state + "%"
        suffix = suffix + (state,)
        and_flag = True
        initial_query = initial_query + state_string
    if zip != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        zip_string = " zip LIKE %s"
        zip = "%" + zip + "%"
        suffix = suffix + (zip,)
        and_flag = True
        initial_query = initial_query + zip_string
    if bday != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        bday_string = " birthday LIKE %s"
        bday = "%" + bday + "%"
        suffix = suffix + (bday,)
        and_flag = True
        initial_query = initial_query + bday_string

    # If user leaves everything blank, prompt to search at least one criteria and redirect
    if suffix == ():
        cur.close()
        flash("Please search at least one criteria", category='danger')
        return redirect(url_for('customers'))

    cur.execute(initial_query, tuple(suffix,))
    customers = cur.fetchall()
    cur.close()

    # the fetched data is stored in customers to it needs to be passed customers.html to put in the table
    return render_template('customers.html', customers=customers)


# ---------------------------------------- EMPLOYEES -----------------------------------------------------------------


# employee page
@app.route('/employees/', methods=['POST', 'GET'])
def employees():
    # opens up a connection by a cursor and pull the the data and closes it
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()

    # the fetched data is stored in employees to it needs to be passed employees.html to put in the table
    return render_template('employees.html', employees=employees)


# this is a route that is used to add employees
@app.route('/add_employee/', methods=['POST', 'GET'])
def add_employee():

    # if it is post method from the form then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        fname = request.form['fname']
        lname = request.form['lname']
        ssn = request.form['ssn']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        apt = request.form['apt']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        bday = request.form['birthday']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # pull all the snns from the table and check to see if the email already exists
        # if so, send a flash message and redirect back to the employees pages by using redirect module and passed the
        # employees function
        cur.execute("SELECT ssn FROM employees")
        ssns = cur.fetchall()
        for key in ssns:
            if key['ssn'] == ssn:
                cur.close()
                flash("SSN Already Exists", category='danger')
                return redirect(url_for('employees'))

        # pull all the phone numbers from the table and check to see if the number already exists
        # if so, send a flash message and redirect back to the employees pages by using redirect module and passed the
        # employees function
        cur.execute("SELECT phone_number FROM employees")
        phones = cur.fetchall()
        for key in phones:
            if key['phone_number'] == phone:
                cur.close()
                flash("Phone Number Already Exists", category='danger')
                return redirect(url_for('employees'))

        # pull all the emails from the table and check to see if the email already exists
        # if so, send a flash message and redirect back to the employees pages by using redirect module and passed the
        # employees function
        cur.execute("SELECT email FROM employees")
        emails = cur.fetchall()
        for key in emails:
            if key['email'] == email:
                cur.close()
                flash("Email Already Exists", category='danger')
                return redirect(url_for('employees'))

        # add to employees
        cur.execute(
            "INSERT INTO employees (first_name, last_name, ssn, phone_number, email, address, apt_number, city, state, zip, birthday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (fname, lname, ssn, phone, email, address, apt, city, state, zip, bday))

        # commit the changes to mysql, flash a success message, and redirect back to employees
        mysql.connection.commit()
        cur.close()
        flash("Employee Data Added Successfully", category='success')
        return redirect(url_for('employees'))


# this is a route that is used to edit employees
@app.route('/update_employee/', methods=['POST', 'GET'])
def update_employee():

    # if post then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        eid = request.form['eid']
        fname = request.form['fname']
        lname = request.form['lname']
        ssn = request.form['ssn']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        apt = request.form['apt']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        bday = request.form['birthday']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # pull all the emails from the table and check to see if the email already exists and is not tied to the current employee
        # if so, send a flash message and redirect back to the employees pages by using redirect module and passed the
        # employees function
        cur.execute("SELECT ssn, employee_id FROM employees")
        ssns = cur.fetchall()
        for key in ssns:
            if key['ssn'] == ssn and int(key['employee_id']) != int(eid):
                cur.close()
                flash("SNN Already Exists", category='danger')
                return redirect(url_for('employees'))

        # pull all the phone numbers from the table and check to see if the number already exists and is not tied to the current employee
        # if so, send a flash message and redirect back to the employees pages by using redirect module and passed the
        # employees function
        cur.execute("SELECT phone_number, employee_id FROM employees")
        phones = cur.fetchall()
        for key in phones:
            if key['phone_number'] == phone and int(key['employee_id']) != int(eid):
                cur.close()
                flash("Phone Number Already Exists", category='danger')
                return redirect(url_for('employees'))

        # pull all the emails from the table and check to see if the email already exists and is not tied to the current employee
        # if so, send a flash message and redirect back to the employees pages by using redirect module and passed the
        # employees function
        cur.execute("SELECT email, employee_id FROM employees")
        emails = cur.fetchall()
        for key in emails:
            if key['email'] == email and int(key['employee_id']) != int(eid):
                cur.close()
                flash("Email Already Exists", category='danger')
                return redirect(url_for('employees'))

        if apt == 'None':
            apt = ''

        # update employee
        cur.execute(
            """ UPDATE employees SET first_name=%s, last_name=%s, ssn=%s, phone_number=%s, email=%s, address=%s, apt_number=%s, city=%s, state=%s, zip=%s, birthday=%s WHERE employee_id=%s """,
            (fname, lname, ssn, phone, email, address, apt, city, state, zip, bday, eid))

        # commit the changes to mysql, flash a success message, and redirect back to employees
        mysql.connection.commit()
        cur.execute("SElECT * FROM employees WHERE employee_id=%s", [eid])
        employees = cur.fetchall()
        cur.close()
        flash("Employee Data Edited Successfully", category='success')

        return render_template('employees.html', employees=employees)

# deletes the employees
@app.route('/delete_employee/', methods=['POST', 'GET'])
def delete_employee():

    # pull the eid from the form, open a cursor and, delete from table
    eid = request.form['eid']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id=%s", [eid], )

    # commit to changes to the database and flash a message for successful removal, then redirect back to employees
    mysql.connection.commit()
    cur.close()
    flash("Employee Has Been Removed Successfully", category='success')
    return redirect(url_for('employees'))

# Search employee page
@app.route('/search_employee/', methods=['POST','GET'])
def search_employee():
    # opens up a connection by a cursor and pull the the data and closes it
    eid = request.form['employee_id']
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    apt = request.form['apt']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    bday = request.form['birthday']

    cur = mysql.connection.cursor()

    # build initial query, set AND flag and declare suffix tuple
    initial_query = """SELECT * FROM employees WHERE"""
    and_flag = False
    suffix = ()

    # based on user input build query and suffix
    if eid != "":
        eid_string = " employee_id LIKE %s"
        eid = "%" + eid + "%"
        suffix = suffix + (eid,)
        and_flag = True
        initial_query = initial_query + eid_string
    if fname != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        fname_string = " first_name LIKE %s"
        fname = "%" + fname + "%"
        suffix = suffix + (fname,)
        and_flag = True
        initial_query = initial_query + fname_string
    if lname != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        lname_string = " last_name Like %s"
        lname = "%" + lname + "%"
        suffix = suffix + (lname,)
        and_flag = True
        initial_query = initial_query + lname_string
    if phone != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        phone_string = " phone_number LIKE %s"
        phone = "%" + phone + "%"
        suffix = suffix + (phone,)
        and_flag = True
        initial_query = initial_query + phone_string
    if email != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        email_string = " email LIKE %s"
        email = "%" + email + "%"
        suffix = suffix + (email,)
        and_flag = True
        initial_query = initial_query + email_string
    if address != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        address_string = " address LIKE %s"
        address = "%" + address + "%"
        suffix = suffix + (address,)
        and_flag = True
        initial_query = initial_query + address_string
    if apt != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        apt_string = " apt_number LIKE %s"
        apt = "%" + apt + "%"
        suffix = suffix + (apt,)
        and_flag = True
        initial_query = initial_query + apt_string
    if city != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        city_string = " city LIKE %s"
        city = "%" + city + "%"
        suffix = suffix + (city,)
        and_flag = True
        initial_query = initial_query + city_string
    if state != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        state_string = " state LIKE %s"
        state = "%" + state + "%"
        suffix = suffix + (state,)
        and_flag = True
        initial_query = initial_query + state_string
    if zip != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        zip_string = " zip LIKE %s"
        zip = "%" + zip + "%"
        suffix = suffix + (zip,)
        and_flag = True
        initial_query = initial_query + zip_string
    if bday != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        bday_string = " birthday LIKE %s"
        bday = "%" + bday + "%"
        suffix = suffix + (bday,)
        and_flag = True
        initial_query = initial_query + bday_string

    # If user leaves everything blank, prompt to search at least one criteria and redirect
    if suffix == ():
        cur.close()
        flash("Please search at least one criteria", category='danger')
        return redirect(url_for('employees'))

    cur.execute(initial_query, tuple(suffix, ))
    employees = cur.fetchall()
    cur.close()

    # the fetched data is stored in customers to it needs to be passed customers.html to put in the table
    return render_template('employees.html', employees=employees)


# ------------------------------------ ELECTRONICS ------------------------------------------------------------------


# electronic page
@app.route('/electronics/', methods=['POST', 'GET'])
def electronics():

    # opens up a connection by a cursor and pull the the data and closes it
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM electronics")
    electronics = cur.fetchall()
    cur.close()

    # the fetched data is stored in electronics to it needs to be passed electronics.html to put in the table
    return render_template('electronics.html', electronics=electronics)


# this is a route that is used to add electronics
@app.route('/add_electronic/', methods=['POST', 'GET'])
def add_electronic():

    # if it is post method from the form then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        make = request.form['make']
        type = request.form['type']
        model = request.form['model']
        version = request.form['version']
        price = request.form['price']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # add to electronics
        cur.execute(
            "INSERT INTO electronics (make, type, model, version, price) VALUES (%s, %s, %s, %s, %s)",
            (make, type, model, version, price))

        # commit the changes to mysql, flash a success message, and redirect back to electronics
        mysql.connection.commit()
        cur.close()
        flash("Electronic Data Added Successfully", category='success')
        return redirect(url_for('electronics'))


# this is a route that is used to edit electronics
@app.route('/update_electronic/', methods=['POST', 'GET'])
def update_electronic():

    # if post then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        iid = request.form['iid']
        make = request.form['make']
        type = request.form['type']
        model = request.form['model']
        version = request.form['version']
        price = request.form['price']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        if version == "None":
            version = ''

        # update electronic
        cur.execute(
            """ UPDATE electronics SET make=%s, type=%s, model=%s, version=%s, price=%s WHERE item_id=%s """,
            (make, type, model, version, price, iid))

        # commit the changes to mysql, flash a success message, and redirect back to electronics
        mysql.connection.commit()
        cur.execute("SElECT * FROM electronics WHERE item_id=%s", [iid])
        electronics = cur.fetchall()
        cur.close()
        flash("Electronic Data Edited Successfully", category='success')
        return render_template('electronics.html', electronics=electronics)

# deletes the electronics
@app.route('/delete_electronic/', methods=['POST', 'GET'])
def delete_electronic():

    # pull the cid from the form, open a cursor and, delete from table
    iid = request.form['iid']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM electronics WHERE item_id=%s", [iid], )

    # commit to changes to the database and flash a message for successful removal, then redirect back to electronics
    mysql.connection.commit()
    cur.close()
    flash("Electronic Has Been Removed Successfully", category='success')
    return redirect(url_for('electronics'))

# Search electronic page
@app.route('/search_electronic/', methods=['POST','GET'])
def search_electronic():

    # opens up a connection by a cursor and pull the the data and closes it
    iid = request.form['item_id']
    make = request.form['make']
    type = request.form['type']
    model = request.form['model']
    version = request.form['version']
    price = request.form['price']

    cur = mysql.connection.cursor()

    # build initial query, set AND flag and declare suffix tuple
    initial_query = """SELECT * FROM electronics WHERE"""
    and_flag = False
    suffix = ()

    # based on user input build query and suffemailix
    if iid != "":
        iid_string = " item_id LIKE %s"
        iid = "%" + iid + "%"
        suffix = suffix + (iid,)
        and_flag = True
        initial_query = initial_query + iid_string
    if make != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        make_string = " make LIKE %s"
        make = "%" + make + "%"
        suffix = suffix + (make,)
        and_flag = True
        initial_query = initial_query + make_string
    if type != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        type_string = " type LIKE %s"
        type = "%" + type + "%"
        suffix = suffix + (type,)
        and_flag = True
        initial_query = initial_query + type_string
    if model != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        model_string = " model LIKE %s"
        model = "%" + model + "%"
        suffix = suffix + (model,)
        and_flag = True
        initial_query = initial_query + model_string
    if version != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        version_string = " version LIKE %s"
        version = "%" + version + "%"
        suffix = suffix + (version,)
        and_flag = True
        initial_query = initial_query + version_string
    if price != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        price_string = " price LIKE %s"
        price = "%" + price + "%"
        suffix = suffix + (price,)
        and_flag = True
        initial_query = initial_query + price_string


    # If user leaves everything blank, prompt to search at least one criteria and redirect
    if suffix == ():
        cur.close()
        flash("Please search at least one criteria", category='danger')
        return redirect(url_for('electronics'))

    cur.execute(initial_query, tuple(suffix, ))
    electronics = cur.fetchall()
    cur.close()

    # the fetched data is stored in customers to it needs to be passed customers.html to put in the table
    return render_template('electronics.html', electronics=electronics)


#---------------------------------------- INVOICES -------------------------------------------------------------------


# invoice page
@app.route('/invoices/', methods=['POST', 'GET'])
def invoices():

    # opens up a connection by a cursor and pull the the data and closes it
    cur = mysql.connection.cursor()

    # a query to display employee and customer data in the select view of the invoice table
    cur.execute("SELECT invoices.invoice_id, invoices.customer_id AS cus_id, invoices.employee_id AS emp_id, "
                "invoices.total_sale, customers.first_name AS c_fname, customers.last_name AS c_lname, "
                "employees.first_name AS e_fname, employees.last_name AS e_lname FROM invoices INNER JOIN customers ON "
                "customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = "
                "invoices.employee_id")
    invoices = cur.fetchall()

    # pull all distinct entries of employees from employees to show data in drop down menu in add invoice
    cur.execute("SELECT DISTINCT employee_id, first_name, last_name FROM employees ORDER BY last_name")
    employee_ids = cur.fetchall()

    # pull all distinct entries of customers from customer to show data in drop down menu in add invoice
    cur.execute("SELECT DISTINCT customer_id, first_name, last_name FROM customers ORDER BY last_name")
    customer_ids = cur.fetchall()

    # pull distinct customer data that exists in invoices table for the search feature
    cur.execute("SELECT DISTINCT invoices.customer_id AS cus_id, customers.first_name AS c_fname, customers.last_name AS c_lname "
                "FROM invoices INNER JOIN customers ON customers.customer_id = invoices.customer_id ORDER BY customers.last_name")
    cus_search = cur.fetchall()

    # pull distinct employee data that exists in invoices table for the search feature
    cur.execute("SELECT DISTINCT invoices.employee_id AS emp_id, employees.first_name AS e_fname, employees.last_name AS e_lname "
                "FROM invoices INNER JOIN employees ON employees.employee_id = invoices.employee_id ORDER BY employees.last_name")
    emp_search = cur.fetchall()

    # close the cursor
    cur.close()

    # the fetched data is stored in invoices to it needs to be passed invoices.html to put in the table
    return render_template('invoices.html', invoices=invoices, employee_ids=employee_ids, customer_ids=customer_ids, cus_search=cus_search, emp_search=emp_search)

# this is a route that is used to add invoices
@app.route('/add_invoice/', methods=['POST', 'GET'])
def add_invoice():

    # if post then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        customer_id = request.form['customer_id']
        employee_id = request.form['employee_id']
        sale = request.form['sale']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # if customer_id is none push flash message
        if customer_id == "None":
            cur.close()
            flash("The Customer ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices'))

        # check to see if the customer id exits
        cur.execute("SELECT customers.customer_id FROM customers")
        cus_id_match = 0
        cus_ids = cur.fetchall()
        for key in cus_ids:
            if key['customer_id'] == int(customer_id):
                cus_id_match = 1

        # if the employee id does not return a flash message saying so
        if cus_id_match == 0:
            cur.close()
            flash("The Customer ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices'))

        if employee_id == 'None':
            # add to invoices
            cur.execute(
                "INSERT INTO invoices (customer_id, total_sale) VALUES (%s, %s)",
                (customer_id, sale))

            mysql.connection.commit()
            cur.close()
            flash("Invoice Data Added Successfully", category='success')
            return redirect(url_for('invoices'))

        # double check to make sure that the employee exists
        cur.execute("SELECT employees.employee_id FROM employees")
        emp_id_match = 0
        emp_ids = cur.fetchall()
        for key in emp_ids:
            if key['employee_id'] == int(employee_id):
                emp_id_match = 1

        # if the employee id does not return a flash message saying so
        if emp_id_match == 0:
            cur.close()
            flash("The Employee ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices'))

        # add to invoices
        cur.execute(
            "INSERT INTO invoices (customer_id, employee_id, total_sale) VALUES (%s, %s, %s)",
            (customer_id, employee_id, sale))

        # commit the changes to mysql, flash a success message, and redirect back to invoices
        mysql.connection.commit()
        cur.close()
        flash("Invoice Data Added Successfully", category='success')
        return redirect(url_for('invoices'))


# this is a route that is used to edit invoices
@app.route('/update_invoice/', methods=['POST', 'GET'])
def update_invoice():

    # if post then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        invoice_id = request.form['invoice_id']
        customer_id = request.form['customer_id']
        employee_id = request.form['employee_id']
        sale = request.form['sale']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # if customer_id is none push flash message
        if customer_id == "None":
            cur.close()
            flash("The Customer ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices'))

        # check to see if the customer id exits
        cur.execute("SELECT customers.customer_id FROM customers")
        cus_id_match = 0
        cus_ids = cur.fetchall()
        for key in cus_ids:
            if key['customer_id'] == int(customer_id):
                cus_id_match = 1

        # if the employee id does not return a flash message saying so
        if cus_id_match == 0:
            cur.close()
            flash("The Customer ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices'))

        if employee_id == 'None':
            # update invoice
            cur.execute(
                """ UPDATE invoices SET customer_id=%s, total_sale=%s, employee_id=NULL WHERE invoice_id=%s """,
                (customer_id, sale, invoice_id))

            # commit the changes to mysql, flash a success message, and redirect back to invoices
            mysql.connection.commit()

            # a query to display employee and customer data in the select view of the invoice table
            cur.execute("SELECT invoices.invoice_id, invoices.customer_id AS cus_id, invoices.employee_id AS emp_id, "
                        "invoices.total_sale, customers.first_name AS c_fname, customers.last_name AS c_lname, "
                        "employees.first_name AS e_fname, employees.last_name AS e_lname FROM invoices INNER JOIN customers ON "
                        "customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = "
                        "invoices.employee_id WHERE invoice_id=%s", [invoice_id], )
            invoices = cur.fetchall()

            # pull all distinct entries of employees from employees to show data in drop down menu in add invoice
            cur.execute("SELECT DISTINCT employee_id, first_name, last_name FROM employees ORDER BY last_name")
            employee_ids = cur.fetchall()

            # pull all distinct entries of customers from customer to show data in drop down menu in add invoice
            cur.execute("SELECT DISTINCT customer_id, first_name, last_name FROM customers ORDER BY last_name")
            customer_ids = cur.fetchall()

            # pull distinct customer data that exists in invoices table for the search feature
            cur.execute(
                "SELECT DISTINCT invoices.customer_id AS cus_id, customers.first_name AS c_fname, customers.last_name AS c_lname "
                "FROM invoices INNER JOIN customers ON customers.customer_id = invoices.customer_id ORDER BY customers.last_name")
            cus_search = cur.fetchall()

            # pull distinct employee data that exists in invoices table for the search feature
            cur.execute(
                "SELECT DISTINCT invoices.employee_id AS emp_id, employees.first_name AS e_fname, employees.last_name AS e_lname "
                "FROM invoices INNER JOIN employees ON employees.employee_id = invoices.employee_id ORDER BY employees.last_name")
            emp_search = cur.fetchall()

            cur.close()
            flash("Invoice Data Edited Successfully", category='success')
            return render_template('invoices.html', invoices=invoices, employee_ids=employee_ids, customer_ids=customer_ids, cus_search=cus_search, emp_search=emp_search)

        # double check to make sure that the employee exists
        cur.execute("SELECT employees.employee_id FROM employees")
        emp_id_match = 0
        emp_ids = cur.fetchall()
        for key in emp_ids:
            if key['employee_id'] == int(employee_id):
                emp_id_match = 1

        # if the employee id does not return a flash message saying so
        if emp_id_match == 0:
            cur.close()
            flash("The Employee ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices'))

        # update invoice
        cur.execute(
            """ UPDATE invoices SET employee_id=%s, customer_id=%s, total_sale=%s WHERE invoice_id=%s """,
            (employee_id, customer_id, sale, invoice_id))

        # commit the changes to mysql, flash a success message, and redirect back to invoices
        mysql.connection.commit()

        # a query to display employee and customer data in the select view of the invoice table
        cur.execute("SELECT invoices.invoice_id, invoices.customer_id AS cus_id, invoices.employee_id AS emp_id, "
                    "invoices.total_sale, customers.first_name AS c_fname, customers.last_name AS c_lname, "
                    "employees.first_name AS e_fname, employees.last_name AS e_lname FROM invoices INNER JOIN customers ON "
                    "customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = "
                    "invoices.employee_id WHERE invoice_id=%s", [invoice_id],)
        invoices = cur.fetchall()

        # pull all distinct entries of employees from employees to show data in drop down menu in add invoice
        cur.execute("SELECT DISTINCT employee_id, first_name, last_name FROM employees ORDER BY last_name")
        employee_ids = cur.fetchall()

        # pull all distinct entries of customers from customer to show data in drop down menu in add invoice
        cur.execute("SELECT DISTINCT customer_id, first_name, last_name FROM customers ORDER BY last_name")
        customer_ids = cur.fetchall()

        # pull distinct customer data that exists in invoices table for the search feature
        cur.execute(
            "SELECT DISTINCT invoices.customer_id AS cus_id, customers.first_name AS c_fname, customers.last_name AS c_lname "
            "FROM invoices INNER JOIN customers ON customers.customer_id = invoices.customer_id ORDER BY customers.last_name")
        cus_search = cur.fetchall()

        # pull distinct employee data that exists in invoices table for the search feature
        cur.execute(
            "SELECT DISTINCT invoices.employee_id AS emp_id, employees.first_name AS e_fname, employees.last_name AS e_lname "
            "FROM invoices INNER JOIN employees ON employees.employee_id = invoices.employee_id ORDER BY employees.last_name")
        emp_search = cur.fetchall()

        cur.close()
        flash("Invoice Data Edited Successfully", category='success')
        return render_template('invoices.html', invoices=invoices, employee_ids=employee_ids, customer_ids=customer_ids, cus_search=cus_search, emp_search=emp_search)

# deletes the invoices
@app.route('/delete_invoice/', methods=['POST', 'GET'])
def delete_invoice():

    # pull the cid from the form, open a cursor and, delete from table
    invoice_id = request.form['invoice_id']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM invoices WHERE invoice_id=%s", [invoice_id], )

    # commit to changes to the database and flash a message for successful removal, then redirect back to invoices
    mysql.connection.commit()
    cur.close()
    flash("Invoice Has Been Removed Successfully", category='success')
    return redirect(url_for('invoices'))

# Search invoice page
@app.route('/search_invoice/', methods=['POST','GET'])
def search_invoice():

    # opens up a connection by a cursor and pull the the data and closes it
    invoice_id = request.form['invoice_id']
    customer_id = request.form['customer_id']
    employee_id = request.form['employee_id']
    sale = request.form['sale']

    cur = mysql.connection.cursor()

    # build initial query, set AND flag and declare suffix tuple
    initial_query = """SELECT invoices.invoice_id, invoices.customer_id AS cus_id, invoices.employee_id AS emp_id, 
                invoices.total_sale, customers.first_name AS c_fname, customers.last_name AS c_lname, 
                employees.first_name AS e_fname, employees.last_name AS e_lname FROM invoices INNER JOIN customers ON 
                customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = 
                invoices.employee_id WHERE"""

    and_flag = False
    suffix = ()
    empty_flag = 0

    # based on user input build query and suffemailix
    if invoice_id != "":
        invoice_id_string = " invoice_id LIKE %s"
        suffix = suffix + (invoice_id,)
        and_flag = True
        initial_query = initial_query + invoice_id_string
        empty_flag = 1
    if customer_id != "None":
        if and_flag == True:
            initial_query = initial_query + " AND"
        customer_id_string = " invoices.customer_id LIKE %s"
        suffix = suffix + (customer_id,)
        and_flag = True
        initial_query = initial_query + customer_id_string
        empty_flag = 1
    if employee_id != "None":
        if and_flag == True:
            initial_query = initial_query + " AND"
        if employee_id != "NULL":
            employee_id_string = " invoices.employee_id=%s"
            suffix = suffix + (employee_id,)
            and_flag = True
            initial_query = initial_query + employee_id_string
        else:
            employee_id_string = " invoices.employee_id IS NULL"
            and_flag = True
            initial_query = initial_query + employee_id_string
        empty_flag = 1
    if sale != "":
        if and_flag == True:
            initial_query = initial_query + " AND"
        sale_string = " total_sale LIKE %s"
        sale = "%" + sale +"%"
        suffix = suffix + (sale,)
        and_flag = True
        initial_query = initial_query + sale_string
        empty_flag = 1

    # If user leaves everything blank, prompt to search at least one criteria and redirect
    if empty_flag == 0:
        cur.close()
        flash("Please search at least one criteria", category='danger')
        return redirect(url_for('invoices'))

    cur.execute(initial_query, tuple(suffix, ))
    invoices = cur.fetchall()
    cur.close()

    # the fetched data is stored in customers to it needs to be passed customers.html to put in the table
    return render_template('invoices.html', invoices=invoices)


# ------------------------------------- INVOICE / ELECTRONICS -------------------------------------------------------


# invoice_electronic page
@app.route('/invoices_electronics/', methods=['POST', 'GET'])
def invoices_electronics():

    # opens up a connection by a cursor and pull the the data and closes it
    cur = mysql.connection.cursor()
    cur.execute("SELECT invoices_electronics.invoice_id, invoices_electronics.item_id, invoices_electronics.item_quantity, "
                "electronics.make, electronics.type, electronics.model, electronics.version, customers.customer_id, customers.last_name AS c_lname, customers.first_name AS c_fname, "
                "employees.employee_id, employees.last_name AS e_lname, employees.first_name AS e_fname FROM invoices_electronics INNER JOIN "
                "electronics ON electronics.item_id = invoices_electronics.item_id INNER JOIN invoices ON invoices.invoice_id = "
                "invoices_electronics.invoice_id INNER JOIN customers ON customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = invoices.employee_id")
    invoices_electronics = cur.fetchall()
    cur.execute("SELECT DISTINCT invoices.invoice_id, invoices.customer_id, invoices.employee_id, customers.last_name AS c_lname, "
                "customers.first_name AS c_fname, employees.last_name AS e_lname, employees.first_name AS e_fname FROM invoices INNER JOIN "
                "customers ON customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = invoices.employee_id "
                "ORDER BY invoice_id")
    invoice_ids = cur.fetchall()
    cur.execute("SELECT DISTINCT item_id, make, type, model, version FROM electronics ORDER BY item_id")
    electronic_ids = cur.fetchall()
    cur.close()

    # the fetched data is stored in invoices to it needs to be passed invoices.html to put in the table
    return render_template('invoices_electronics.html', invoices_electronics=invoices_electronics, invoice_ids=invoice_ids, electronic_ids=electronic_ids)


# this is a route that is used to add invoices
@app.route('/add_invoice_electronic/', methods=['POST', 'GET'])
def add_invoice_electronic():

    # if it is post method from the form then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables
        invoice_id = request.form['invoice_id']
        item_id = request.form['item_id']
        quantity = request.form['quantity']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # if invoice_id or item_id is None then do nothing and flash message
        if invoice_id == "None":
            cur.close()
            flash("The Invoice ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))

        if item_id == "None":
            cur.close()
            flash("The Item ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))

        # double check to make sure that the invoice exists
        cur.execute("SELECT invoices.invoice_id FROM invoices")
        inv_id_match = 0
        inv_ids = cur.fetchall()
        for key in inv_ids:
            if key['invoice_id'] == int(invoice_id):
                inv_id_match = 1

        # if the invoice id does not, return a flash message saying so
        if inv_id_match == 0:
            cur.close()
            flash("The Invoice ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))

        # check to see if the item id exits
        cur.execute("SELECT electronics.item_id FROM electronics")
        ele_id_match = 0
        ele_ids = cur.fetchall()
        for key in ele_ids:
            if key['item_id'] == int(item_id):
                ele_id_match = 1

        # if the item id does not, return a flash message saying so
        if ele_id_match == 0:
            cur.close()
            flash("The Item ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))

        # check to see if the item_id, invoice_id, and qty combin1ation already exists
        cur.execute("SELECT invoice_id, item_id FROM invoices_electronics")
        ies = cur.fetchall()
        for key in ies:
            if key['invoice_id'] == int(invoice_id) and key['item_id'] == int(item_id):
                cur.close()
                flash("The Unique Combination of Item ID and Invoice ID Already Exists", category='danger')
                return redirect(url_for('invoices_electronics'))

        # add to invoices_electronics
        cur.execute(
            "INSERT INTO invoices_electronics (invoice_id, item_id, item_quantity) VALUES (%s, %s, %s)",
            (invoice_id, item_id, quantity))

        # commit the changes to mysql, flash a success message, and redirect back to invoices
        mysql.connection.commit()
        cur.close()
        flash("Invoice/Electronic Data Added Successfully", category='success')
        return redirect(url_for('invoices_electronics'))


# this is a route that is used to edit invoices
@app.route('/update_invoice_electronic/', methods=['POST', 'GET'])
def update_invoice_electronic():

    # if post then proceed
    if request.method == 'POST':

        # the module 'request' is needed to store the saved form variables into variables and pull the current values
        # because there is no pk for traditional updates
        iid = request.form['iid']
        eid = request.form['eid']
        qty = request.form['qty']
        invoice_id = request.form['invoice_id']
        item_id = request.form['item_id']
        quantity = request.form['quantity']

        # open up a connect to mysql
        cur = mysql.connection.cursor()

        # if invoice_id or item_id is None then do nothing and flash message
        if invoice_id == "None":
            cur.close()
            flash("The Invoice ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))

        if item_id == "None":
            cur.close()
            flash("The Item ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))

        # double check to make sure that the invoice exists
        cur.execute("SELECT invoices.invoice_id FROM invoices")
        inv_id_match = 0
        inv_ids = cur.fetchall()
        for key in inv_ids:
            if key['invoice_id'] == int(invoice_id):
                inv_id_match = 1

        # if the invoice id does not, return a flash message saying so
        if inv_id_match == 0:
            cur.close()
            flash("The Invoice ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))

        # check to see if the item id exits
        cur.execute("SELECT electronics.item_id FROM electronics")
        ele_id_match = 0
        ele_ids = cur.fetchall()
        for key in ele_ids:
            if key['item_id'] == int(item_id):
                ele_id_match = 1

        # if the item id does not, return a flash message saying so
        if ele_id_match == 0:
            cur.close()
            flash("The Item ID Entered Does Not Exist", category='danger')
            return redirect(url_for('invoices_electronics'))


        # check to see if the item_id if invoice_id and item_id already exists if it the update changes the combination
        if iid != invoice_id or eid != item_id:
            cur.execute("SELECT * FROM invoices_electronics")
            ies = cur.fetchall()
            for key in ies:
                if key['invoice_id'] == int(invoice_id) and key['item_id'] == int(item_id):
                    cur.close()
                    flash("The Unique Combination of Item ID and Invoice ID Already Exists",
                          category='danger')
                    return redirect(url_for('invoices_electronics'))

        # update invoice
        cur.execute(
            """ UPDATE invoices_electronics SET invoice_id=%s, item_id=%s, item_quantity=%s WHERE invoice_id=%s AND item_id=%s AND item_quantity=%s """,
            (invoice_id, item_id, quantity, iid, eid, qty))

        # commit the changes to mysql, flash a success message, and redirect back to invoices
        mysql.connection.commit()

        # gather filters for release
        cur.execute(
            "SELECT invoices_electronics.invoice_id, invoices_electronics.item_id, invoices_electronics.item_quantity, "
            "electronics.make, electronics.type, electronics.model, electronics.version, customers.customer_id, customers.last_name AS c_lname, customers.first_name AS c_fname, "
            "employees.employee_id, employees.last_name AS e_lname, employees.first_name AS e_fname FROM invoices_electronics INNER JOIN "
            "electronics ON electronics.item_id = invoices_electronics.item_id INNER JOIN invoices ON invoices.invoice_id = "
            "invoices_electronics.invoice_id INNER JOIN customers ON customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = invoices.employee_id "
            "WHERE invoices_electronics.invoice_id=%s AND invoices_electronics.item_id=%s", [invoice_id, item_id], )
        invoices_electronics = cur.fetchall()
        cur.execute(
            "SELECT DISTINCT invoices.invoice_id, invoices.customer_id, invoices.employee_id, customers.last_name AS c_lname, "
            "customers.first_name AS c_fname, employees.last_name AS e_lname, employees.first_name AS e_fname FROM invoices INNER JOIN "
            "customers ON customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = invoices.employee_id "
            "ORDER BY invoice_id")
        invoice_ids = cur.fetchall()
        cur.execute("SELECT DISTINCT item_id, make, type, model, version FROM electronics ORDER BY item_id")
        electronic_ids = cur.fetchall()

        cur.close()
        flash("Invoice/Electronic Data Edited Successfully", category='success')
        return render_template('invoices_electronics.html', invoices_electronics=invoices_electronics,
                               invoice_ids=invoice_ids, electronic_ids=electronic_ids)

# deletes the invoices
@app.route('/delete_invoice_electronic/', methods=['POST', 'GET'])
def delete_invoice_electronic():

    # pull the invoice id, item id and qty from the form so it can be used as a super key and deleted
    iid = request.form['iid']
    eid = request.form['eid']
    qty = request.form['qty']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM invoices_electronics WHERE invoice_id=%s AND item_id=%s AND item_quantity=%s", [iid, eid, qty], )

    # commit to changes to the database and flash a message for successful removal, then redirect back to invoices
    mysql.connection.commit()
    flash("Invoice/Electronic Has Been Removed Successfully", category='success')
    return redirect(url_for('invoices_electronics'))

# Search invoice/electronic page
@app.route('/search_invoice_electronic//', methods=['POST','GET'])
def search_invoice_electronic():

    # the module 'request' is needed to store the saved form variables into variables
    iid = request.form['invoice_id']
    eid = request.form['item_id']

    cur = mysql.connection.cursor()

    # build initial query, set AND flag and declare suffix tuple
    initial_query = """SELECT invoices_electronics.invoice_id, invoices_electronics.item_id, invoices_electronics.item_quantity, 
        electronics.make, electronics.type, electronics.model, electronics.version, customers.customer_id, customers.last_name AS c_lname, customers.first_name AS c_fname, 
        employees.employee_id, employees.last_name AS e_lname, employees.first_name AS e_fname FROM invoices_electronics INNER JOIN 
        electronics ON electronics.item_id = invoices_electronics.item_id INNER JOIN invoices ON invoices.invoice_id = 
        invoices_electronics.invoice_id INNER JOIN customers ON customers.customer_id = invoices.customer_id LEFT JOIN employees ON employees.employee_id = invoices.employee_id WHERE"""
    and_flag = False
    suffix = ()

    # based on user input build query and suffemailix
    if iid != "None":
        invoice_id_string = " invoices_electronics.invoice_id=%s"
        suffix = suffix + (iid,)
        and_flag = True
        initial_query = initial_query + invoice_id_string
    if eid != "None":
        if and_flag == True:
            initial_query = initial_query + " AND"
        item_id_string = " invoices_electronics.item_id=%s"
        suffix = suffix + (eid,)
        and_flag = True
        initial_query = initial_query + item_id_string

    cur.execute(initial_query, tuple(suffix, ))
    invoices_electronics = cur.fetchall()
    cur.close()

    # the fetched data is stored in customers to it needs to be passed customers.html to put in the table
    return render_template('invoices_electronics.html', invoices_electronics=invoices_electronics)


# --------------------------------------------------- ERROR HANDLING --------------------------------------------------


# Catch bad routes
@app.errorhandler(404)
def not_found(bad_url):
    """Page not found, render error and redirect"""
    return render_template('not-found.html')