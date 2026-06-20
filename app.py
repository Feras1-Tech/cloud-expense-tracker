from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, amount FROM expenses")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

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

            <form action="/add" method="post">
                <input name="name" placeholder="Expense Name" required>
                <input name="amount" type="number" step="0.01" placeholder="Amount" required>
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

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (name, amount) VALUES (?, ?)",
        (name, amount)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)