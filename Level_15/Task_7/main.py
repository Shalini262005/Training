from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
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
    
    cursor.execute('Select * from customer_shopping_data')
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('report.html',rows=rows)

if __name__ == '__main__':
    app.run(debug=True)