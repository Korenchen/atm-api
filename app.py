from flask import Flask, jsonify, request
from accounts import accounts

app = Flask(__name__)

# Get balance
@app.route('/accounts/<account_number>/balance', methods=['GET'])
def get_balance(account_number):
    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "account_number": account_number,
        "balance": accounts[account_number]["balance"]
    })

# Deposit money
@app.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    amount = data.get("amount", 0)
    if amount <= 0:
        return jsonify({"error": "Deposit amount must be positive"}), 400

    accounts[account_number]["balance"] += amount
    return jsonify({
        "message": "Deposit successful",
        "balance": accounts[account_number]["balance"]
    })

# Withdraw money
@app.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    amount = data.get("amount", 0)
    if amount <= 0:
        return jsonify({"error": "Withdraw amount must be positive"}), 400
    if accounts[account_number]["balance"] < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    accounts[account_number]["balance"] -= amount
    return jsonify({
        "message": "Withdrawal successful",
        "balance": accounts[account_number]["balance"]
    })

if __name__ == "__main__":
    app.run(debug=True)
