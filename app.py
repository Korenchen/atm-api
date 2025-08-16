import os
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from werkzeug.exceptions import BadRequest, NotFound

# accounts data
accounts = {
    "1001": {"balance": 500.0},
    "1002": {"balance": 1000.0},
    "1003": {"balance": 750.0}
}

app = Flask(__name__)
CORS(app)

# Configure Swagger UI
api = Api(
    app,
    version='1.0',
    title='ATM Banking API',
    description='A comprehensive ATM banking system API with account management and transaction processing capabilities',
    doc='/docs',  # Swagger UI will be available at /docs
    contact_email="your.email@example.com",
    contact_url="https://github.com/yourusername/atm-api",
    mask=None,
)
app.config["SWAGGER_UI_DOC_EXPANSION"] = "list"

# Create namespaces for better organization
accounts_ns = api.namespace('accounts', description='Account management operations')

# Define data models for Swagger documentation
balance_model = api.model('Balance', {
    'account_number': fields.String(required=True, description='Account number', example='1001'),
    'balance': fields.Float(required=True, description='Current account balance', example=500.0)
})

transaction_request = api.model('TransactionRequest', {
    'amount': fields.Float(required=True, description='Transaction amount', example=100.0, min=0.01)
})

transaction_response = api.model('TransactionResponse', {
    'message': fields.String(required=True, description='Transaction status message', example='Deposit successful'),
    'balance': fields.Float(required=True, description='Updated account balance', example=600.0)
})

error_model = api.model('Error', {
    'error': fields.String(required=True, description='Error message', example='Account not found')
})


@accounts_ns.route('/<string:account_number>/balance')
@accounts_ns.param('account_number', 'The account number (1001, 1002, or 1003)')
class AccountBalance(Resource):
    @accounts_ns.doc('get_balance')
    @accounts_ns.marshal_with(balance_model,mask=None)
    @accounts_ns.response(404, 'Account not found', error_model)
    def get(self, account_number):
        """Get account balance

        Retrieve the current balance for the specified account number.
        Available accounts: 1001, 1002, 1003
        """
        if account_number not in accounts:
            api.abort(404, error="Account not found")

        return {
            'account_number': account_number,
            'balance': accounts[account_number]['balance']
        }


@accounts_ns.route('/<string:account_number>/deposit')
@accounts_ns.param('account_number', 'The account number (1001, 1002, or 1003)')
class AccountDeposit(Resource):
    @accounts_ns.doc('deposit_money')
    @accounts_ns.expect(transaction_request, validate=True)
    @accounts_ns.marshal_with(transaction_response,mask=None)
    @accounts_ns.response(400, 'Bad request - Invalid amount', error_model)
    @accounts_ns.response(404, 'Account not found', error_model)
    def post(self, account_number):
        """Deposit money to account

        Add money to the specified account. The amount must be positive.
        The response includes a success message and the updated balance.
        """
        if account_number not in accounts:
            api.abort(404, error="Account not found")

        data = request.get_json()
        if not data or 'amount' not in data:
            api.abort(400, error="Amount is required")

        amount = data.get('amount', 0)

        if not isinstance(amount, (int, float)) or amount <= 0:
            api.abort(400, error="Deposit amount must be a positive number")

        # Round to 2 decimal places for currency
        amount = round(float(amount), 2)
        accounts[account_number]['balance'] = round(accounts[account_number]['balance'] + amount, 2)

        return {
            'message': f'Deposit successful. ${amount} added to account {account_number}',
            'balance': accounts[account_number]['balance']
        }


@accounts_ns.route('/<string:account_number>/withdraw')
@accounts_ns.param('account_number', 'The account number (1001, 1002, or 1003)')
class AccountWithdraw(Resource):
    @accounts_ns.doc('withdraw_money')
    @accounts_ns.expect(transaction_request, validate=True)
    @accounts_ns.marshal_with(transaction_response,mask=None)
    @accounts_ns.response(400, 'Bad request - Invalid amount or insufficient funds', error_model)
    @accounts_ns.response(404, 'Account not found', error_model)
    def post(self, account_number):
        """Withdraw money from account

        Remove money from the specified account. The amount must be positive
        and not exceed the current account balance.
        """
        if account_number not in accounts:
            api.abort(404, error="Account not found")

        data = request.get_json()
        if not data or 'amount' not in data:
            api.abort(400, error="Amount is required")

        amount = data.get('amount', 0)

        if not isinstance(amount, (int, float)) or amount <= 0:
            api.abort(400, error="Withdrawal amount must be a positive number")

        # Round to 2 decimal places for currency
        amount = round(float(amount), 2)
        current_balance = accounts[account_number]['balance']

        if current_balance < amount:
            api.abort(400, error=f"Insufficient funds. Current balance: ${current_balance}, Requested: ${amount}")

        accounts[account_number]['balance'] = round(current_balance - amount, 2)

        return {
            'message': f'Withdrawal successful. ${amount} withdrawn from account {account_number}',
            'balance': accounts[account_number]['balance']
        }


@accounts_ns.route('')
class AccountsList(Resource):
    @accounts_ns.doc('list_accounts')
    def get(self):
        """List all available accounts

        Returns a list of all available accounts with their current balances.
        This is useful for getting an overview of all accounts in the system.
        """
        account_list = []
        for account_num, account_data in accounts.items():
            account_list.append({
                'account_number': account_num,
                'balance': account_data['balance']
            })

        return {
            'accounts': account_list,
            'total_accounts': len(account_list)
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)