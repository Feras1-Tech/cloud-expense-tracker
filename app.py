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
    <h1>Expense Tracker</h1>

    <h2>Total Expenses: ${total}</h2>

    <form action="/add" method="post">
        <input name="name" placeholder="Expense Name" required>
        <input name="amount" type="number" step="0.01" placeholder="Amount" required>
        <button type="submit">Add Expense</button>
    </form>

    <h2>Expenses</h2>
    """

    for expense in expenses:
        html += f"""
        <p>
            {expense[1]} - ${expense[2]}
            <a href="/delete/{expense[0]}">❌ Delete</a>
        </p>
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