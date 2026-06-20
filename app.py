from flask import Flask, request, redirect
from google.cloud import storage
import psycopg2

app = Flask(__name__)

def init_db():
    conn = psycopg2.connect(
        host="34.52.251.175",
        database="expenses",
        user="postgres",
        password="Expense@2026"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        amount DECIMAL
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():

    conn = psycopg2.connect(
        host="34.52.251.175",
        database="expenses",
        user="postgres",
        password="Expense@2026"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT id, name, amount FROM expenses")
    expenses = cursor.fetchall()

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    total = cursor.fetchone()[0]

    conn.close()
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expense Tracker</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f6f9;
                margin: 0;
                padding: 40px;
            }}

            .container {{
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}

            h1 {{
                text-align: center;
                color: #333;
            }}

            .total {{
                text-align: center;
                font-size: 24px;
                color: green;
                margin-bottom: 25px;
            }}

            form {{
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }}

            input {{
                flex: 1;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }}

            button {{
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
            }}

            button:hover {{
                background: #0056b3;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th {{
                background: #007bff;
                color: white;
                padding: 12px;
            }}

            td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}

            .delete {{
                color: red;
                text-decoration: none;
                font-weight: bold;
            }}

            .delete:hover {{
                color: darkred;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h1>💰 Expense Tracker</h1>

            <div class="total">
                Total Expenses: ${total:.2f}
            </div>

            <form action="/add" method="post" enctype="multipart/form-data">
                <input name="name" placeholder="Expense Name" required>
                <input name="amount" type="number" step="0.01" placeholder="Amount" required>
                <input type="file" name="receipt">
                <button type="submit">Add Expense</button>
            </form>

            <table>
                <tr>
                    <th>Expense</th>
                    <th>Amount</th>
                    <th>Action</th>
                </tr>
    """

    for expense in expenses:
        html += f"""
        <tr>
            <td>{expense[1]}</td>
            <td>${expense[2]:.2f}</td>
            <td>
                <a class="delete" href="/delete/{expense[0]}">
                    Delete
                </a>
            </td>
        </tr>
        """

    html += """
            </table>

        </div>

    </body>
    </html>
    """

    return html


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    amount = request.form["amount"]
    receipt = request.files["receipt"]

    client = storage.Client()
    bucket = client.bucket("expense-receipts-feras")

    blob = bucket.blob(receipt.filename)
    blob.upload_from_file(receipt)

    receipt_url = blob.public_url

    conn = psycopg2.connect(
        host="34.52.251.175",
        database="expenses",
        user="postgres",
        password="Expense@2026"
    )

    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO expenses (name, amount, receipt_url) VALUES (%s, %s, %s)",
    (name, amount, receipt_url)
)

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:expense_id>")
def delete(expense_id):

    conn = psycopg2.connect(
        host="34.52.251.175",
        database="expenses",
        user="postgres",
        password="Expense@2026"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = %s",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")