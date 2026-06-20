from flask import Flask, request

app = Flask(__name__)

expenses = []

@app.route("/")
def home():
    html = """
    <h1>Expense Tracker</h1>

    <form action="/add" method="post">
        <input name="name" placeholder="Expense Name">
        <input name="amount" placeholder="Amount">
        <button type="submit">Add Expense</button>
    </form>

    <h2>Expenses</h2>
    """

    for e in expenses:
        html += f"<p>{e['name']} - ${e['amount']}</p>"

    return html

@app.route("/add", methods=["POST"])
def add():
    expenses.append({
        "name": request.form["name"],
        "amount": request.form["amount"]
    })
    return home()