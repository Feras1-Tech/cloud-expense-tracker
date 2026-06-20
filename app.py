from flask import Flask, request
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

    cursor.execute("SELECT name, amount FROM expenses")
    expenses = cursor.fetchall()

    conn.close()

    html = """
    <h1>Expense Tracker</h1>

    <form action="/add" method="post">
        <input name="name" placeholder="Expense Name">
        <input name="amount" placeholder="Amount">
        <button type="submit">Add Expense</button>
    </form>

    <h2>Expenses</h2>
    """

    for expense in expenses:
        html += f"<p>{expense[0]} - ${expense[1]}</p>"

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

    return home()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)