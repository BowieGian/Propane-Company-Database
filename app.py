import pandas as pd
import sqlite3

from flask import Flask, render_template, url_for, request, redirect
from our_sql import *
from sqlite3 import Error

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()

    employees = cursor.execute('SELECT first_name FROM employee').fetchall();

    if request.method == 'POST':
        first_name = request.form['first_name']
        id = request.form['id']

        # find if login exists
        if cursor.execute('SELECT id FROM employee WHERE first_name = ? AND id = ?', (first_name, id,)).fetchone():
            return redirect(url_for('home'))
        else:
            return render_template('login.html', employees=employees, loginFailed=True)
    else:
        return render_template('login.html', employees=employees, loginFailed=False)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/inventory/add', methods=['GET', 'POST'])
def inventoryAdd():
    database = 'propane354.db'
    connection = create_connection(database)
    cursor = connection.cursor()

    retail_employees = cursor.execute('SELECT id FROM employee WHERE position = "Retail";').fetchall();
    customer_emails = cursor.execute('SELECT email FROM customer;').fetchall();
    
    if request.method == 'POST':
        form = {}
        attributes = [
            'serial_number', 'manufacturer', 'expiration_date', 'quick_fill', 'form_factor',
            'tare_weight', 'water_capacity', 'liquid_vapor', 'rust_level', 'production_date',
            'last_visual_check_date', 'type_of_tank', 'sold_by_employee_id',
            'sold_to_customer_email', 'sell_date'
        ]

        for attribute in attributes:
            user_input = request.form[attribute]
            if (user_input != ''):
                form[attribute] = user_input
            else:
                form[attribute] = None

        return_value = 'success'
        new_propane_tank_values = tuple(form.values())
        return_value = insert_propane_tank(connection, new_propane_tank_values)
        if (return_value != 'success'):
            return render_template('inventory-add.html', retail_employees=retail_employees, customer_emails=customer_emails, error=return_value)
        else:
            return render_template('inventory-add.html', retail_employees=retail_employees, customer_emails=customer_emails, error='')
    else:
        return render_template('inventory-add.html', retail_employees=retail_employees, customer_emails=customer_emails, error='')

@app.route('/inventory/list', methods=['GET', 'POST'])
def inventoryList():
    database = 'propane354.db'
    connection = create_connection(database)

    group_by_attribute = request.form['group-by']
    select_propane_tank_results = select_propane_tank(connection, group_by_attribute)    

    return render_template(
        'inventory-list.html',
        tables=[select_propane_tank_results.to_html(classes='data', index=False)],
        titles=select_propane_tank_results.columns.values
    )

@app.route('/work-order', methods=['GET', 'POST'])
def workOrder():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('work-order.html')

@app.route('/work-order/create', methods=['GET', 'POST'])
def workOrderCreate():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('work-order-create.html')

@app.route('/work-order/list', methods=['GET', 'POST'])
def workOrderList():
    database = 'propane354.db'
    connection = create_connection(database)
    
    if (connection):
        cursor = connection.cursor()
    else:
        return "Failed to create database connection."

    test_sql = f'''
        SELECT *
        FROM work_order
    '''

    df = pd.read_sql(test_sql, connection)

    if request.method == 'POST':
        return render_template('work-order-list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
    else:
        return render_template('work-order-list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

    '''
    if request.method == 'POST':
        return 'Post'
    else:
        workOrders = cursor.execute('SELECT * FROM WorkOrder').fetchall()
        return render_template('work-order-list.html', workOrders=workOrders)
    '''

@app.route('/employee-list', methods=['GET', 'POST'])
def employeeList():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('employee-list.html')

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('customers.html')

@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('vehicles.html')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        return 'Post'
    else:
        return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
