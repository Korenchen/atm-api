import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields


# Dictionary to store account information with account numbers as keys
accounts = {
    "1001": {"balance": 500.0},
    "1002": {"balance": 1000.0},
    "1003": {"balance": 750.0}
}
# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configure Swagger UI
api = Api(
    app,
    version='1.0',
    title='ATM Banking API',
    description='A comprehensive ATM banking system API with account management and transaction processing capabilities',
    doc='/docs',
    mask=None,
)
app.config["SWAGGER_UI_DOC_EXPANSION"] = "list"
app.config['ERROR_404_HELP'] = False
app.config['SERVER_NAME'] = 'atm-api-435429241525.us-central1.run.app'
app.config['PREFERRED_URL_SCHEME'] = 'https'
# Create namespace for account-related operations
accounts_ns = api.namespace('accounts', description='Account management operations')
# Model for account balance response
balance_model = api.model('Balance', {
    'account_number': fields.String(required=True, description='Account number', example='1001'),
    'balance': fields.Float(required=True, description='Current account balance', example=500.0)
})
# Model for transaction request payload
transaction_request = api.model('TransactionRequest', {
    'amount': fields.Float(required=True, description='Transaction amount', example=100.0, min=0.01)
})
# Models for deposit responses
deposit_response = api.model('DepositResponse', {
    'message': fields.String(required=True, description='Transaction status message',
                           example='Deposit successful. $100.0 added to account 1001'),
    'balance': fields.Float(required=True, description='Updated account balance', example=600.0)
})
#Model for withdrawal responses
withdraw_response = api.model('WithdrawResponse', {
    'message': fields.String(required=True, description='Transaction status message',
                           example='Withdrawal successful. $100.0 withdrawn from account 1001'),
    'balance': fields.Float(required=True, description='Updated account balance', example=400.0)
})
# Model for 404 error response
not_found_error_model = api.model('NotFoundError', {
    'error': fields.String(required=True, description='Error message', example='Account not found')
})
# Model for 400 error responses (bad request)
bad_request_error_model = api.model('BadRequestError', {
    'error': fields.String(required=True, description='Error message', example='Deposit amount must be a positive number')
})
# Model for 400 insufficient funds error
insufficient_funds_error_model = api.model('InsufficientFundsError', {
    'error': fields.String(required=True, description='Error message', example='Insufficient funds. Current balance: $500.0, Requested: $600.0')
})
@accounts_ns.route('/<string:account_number>/balance')
@accounts_ns.param('account_number', 'The account number (1001, 1002, or 1003)')
class AccountBalance(Resource):
    @accounts_ns.doc('get_balance')
    @accounts_ns.response(200, 'Success', balance_model)
    @accounts_ns.response(404, 'Account not found', not_found_error_model)
    def get(self, account_number):
        """Get account balance

        Retrieve the current balance for the specified account number.
        Available accounts: 1001, 1002, 1003
        """
        if account_number not in accounts:
            return {"error": "Account not found"}, 404

        return {
            'account_number': account_number,
            'balance': accounts[account_number]['balance']
        }
@accounts_ns.route('/<string:account_number>/deposit')
@accounts_ns.param('account_number', 'The account number (1001, 1002, or 1003)')
class AccountDeposit(Resource):
    @accounts_ns.doc('deposit_money')
    @accounts_ns.expect(transaction_request, validate=False)
    @accounts_ns.response(200, 'Success', deposit_response)
    @accounts_ns.response(400, 'Bad request - Invalid amount', bad_request_error_model)
    @accounts_ns.response(404, 'Account not found', not_found_error_model)
    def post(self, account_number):
        """Deposit money to account

        Add money to the specified account. The amount must be positive.
        The response includes a success message and the updated balance.
        """
        if account_number not in accounts:
            return {"error": "Account not found"}, 404
        data = request.get_json()
        if not data or 'amount' not in data:
            return {"error": "Amount is required"}, 400
        amount = data.get('amount', 0)
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"error": "Deposit amount must be a positive number"}, 400
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
    @accounts_ns.expect(transaction_request, validate=False)
    @accounts_ns.response(200, 'Success', withdraw_response)
    @accounts_ns.response(400, 'Bad request - Invalid amount or insufficient funds', insufficient_funds_error_model)
    @accounts_ns.response(404, 'Account not found', not_found_error_model)
    def post(self, account_number):
        """Withdraw money from account

        Remove money from the specified account. The amount must be positive
        and not exceed the current account balance.
        """
        if account_number not in accounts:
            return {"error": "Account not found"}, 404
        data = request.get_json()
        if not data or 'amount' not in data:
            return {"error": "Amount is required"}, 400
        amount = data.get('amount', 0)
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {"error": "Withdrawal amount must be a positive number"}, 400
        # Round to 2 decimal places for currency
        amount = round(float(amount), 2)
        current_balance = accounts[account_number]['balance']
        if current_balance < amount:
            return {"error": f"Insufficient funds. Current balance: ${current_balance}, Requested: ${amount}"}, 400
        accounts[account_number]['balance'] = round(current_balance - amount, 2)
        return {
            'message': f'Withdrawal successful. ${amount} withdrawn from account {account_number}',
            'balance': accounts[account_number]['balance']
        }
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)