from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "abcd" 

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sh@lini262005',
        database='shopping'
    )
    return connection

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/report")
def report():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM customer_shopping_data')
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('report.html', rows=rows)

@app.route("/input", methods=['GET', 'POST'])
def input_form():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        gender = request.form['gender']
        age = request.form['age']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        payment_method = request.form['payment_method']
        shopping_mall = request.form['shopping_mall']
        invoice_date = datetime.now().strftime('%d/%m/%Y')
        invoice_no = 'I' + str(uuid.uuid4().int)[:6]

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            query = '''
            INSERT INTO customer_shopping_data 
            (invoice_no, customer_id, gender, age, category, quantity, price, payment_method, invoice_date, shopping_mall)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            values = (invoice_no, customer_id, gender, age, category, quantity, price, payment_method, invoice_date, shopping_mall)

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            flash('Order added successfully!', 'success')
            return redirect(url_for('report'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('input_form'))

    # GET request renders the form
    return render_template("input.html")


@app.route("/monthly-sales")
def monthly_sales():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
        WITH parsed_data AS (
        SELECT
        YEAR(STR_TO_DATE(invoice_date, '%d/%m/%Y')) AS Year,
        LPAD(MONTH(STR_TO_DATE(invoice_date, '%d/%m/%Y')), 2, '0') AS `Month(num)`,
        MONTHNAME(STR_TO_DATE(invoice_date, '%d/%m/%Y')) AS `Month name`,
        quantity * price AS `Total sales`
        FROM customer_shopping_data)

        SELECT Year, `Month(num)`, `Month name`,
        SUM(`Total sales`) AS `Monthly sales`,
        SUM(SUM(`Total sales`)) OVER (PARTITION BY Year ORDER BY `Month(num)`) AS `Monthly Cumulative Sales`
        FROM parsed_data
        GROUP BY Year, `Month(num)`, `Month name`
        ORDER BY Year, `Month(num)`
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('monthly_sales.html', rows=rows)

@app.route("/top-5-cust")
def top_5_cust():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT customer_id, category, `Amount Spent`
    FROM (
    SELECT 
        customer_id, 
        category, 
        SUM(quantity * price) AS `Amount Spent`,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(quantity * price) DESC) AS `row_num`
    FROM customer_shopping_data
    GROUP BY customer_id, category) 
    AS RankedCustomers
    WHERE `row_num` <= 5
    ORDER BY category, `row_num`;
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('top_5_cust.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
