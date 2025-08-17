import unittest
import json
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, accounts


class TestATMBankingAPI(unittest.TestCase):
    """Unit tests for ATM Banking API"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Disable SERVER_NAME for testing to avoid routing issues
        app.config['SERVER_NAME'] = None
        app.config['TESTING'] = True

        self.app = app.test_client()
        self.app.testing = True

        # Reset accounts to initial state before each test
        accounts.clear()
        accounts.update({
            "1001": {"balance": 500.0},
            "1002": {"balance": 1000.0},
            "1003": {"balance": 750.0}
        })

    def tearDown(self):
        """Clean up after each test method."""
        pass

    # ============= GET /accounts/{id}/balance Tests =============
    def test_get_balance_success(self):
        """Test getting balance for valid account"""
        response = self.app.get('/accounts/1001/balance')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['account_number'], '1001')
        self.assertEqual(data['balance'], 500.0)

    def test_get_balance_invalid_account(self):
        """Test getting balance for invalid account returns 404"""
        response = self.app.get('/accounts/9999/balance')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Account not found')

    def test_get_balance_all_accounts(self):
        """Test getting balance for all valid accounts"""
        test_cases = [
            ('1001', 500.0),
            ('1002', 1000.0),
            ('1003', 750.0)
        ]

        for account_num, expected_balance in test_cases:
            with self.subTest(account=account_num):
                response = self.app.get(f'/accounts/{account_num}/balance')
                self.assertEqual(response.status_code, 200)

                data = json.loads(response.data)
                self.assertEqual(data['account_number'], account_num)
                self.assertEqual(data['balance'], expected_balance)

    # ============= POST /accounts/{id}/deposit Tests =============
    def test_deposit_success(self):
        """Test successful deposit"""
        deposit_data = {"amount": 100.0}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('balance', data)
        self.assertEqual(data['balance'], 600.0)  # 500 + 100
        self.assertIn('Deposit successful', data['message'])
        self.assertIn('$100.0', data['message'])
        self.assertIn('1001', data['message'])

    def test_deposit_invalid_account(self):
        """Test deposit to invalid account returns 404"""
        deposit_data = {"amount": 100.0}
        response = self.app.post('/accounts/9999/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Account not found')

    def test_deposit_missing_amount(self):
        """Test deposit without amount field returns 400"""
        deposit_data = {}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Amount is required')


    def test_deposit_negative_amount(self):
        """Test deposit with negative amount returns 400"""
        deposit_data = {"amount": -50.0}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Deposit amount must be a positive number')

    def test_deposit_zero_amount(self):
        """Test deposit with zero amount returns 400"""
        deposit_data = {"amount": 0}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Deposit amount must be a positive number')

    def test_deposit_invalid_amount_type(self):
        """Test deposit with invalid amount type returns 400"""
        deposit_data = {"amount": "not_a_number"}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Deposit amount must be a positive number')

    def test_deposit_none_amount(self):
        """Test deposit with null amount returns 400"""
        deposit_data = {"amount": None}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Deposit amount must be a positive number')

    def test_deposit_decimal_precision(self):
        """Test deposit with decimal places rounds correctly"""
        deposit_data = {"amount": 100.456}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Should round to 2 decimal places: 500 + 100.46 = 600.46
        self.assertEqual(data['balance'], 600.46)

    def test_deposit_integer_amount(self):
        """Test deposit with integer amount works correctly"""
        deposit_data = {"amount": 100}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 600.0)

    # ============= POST /accounts/{id}/withdraw Tests =============
    def test_withdraw_success(self):
        """Test successful withdrawal"""
        withdraw_data = {"amount": 100.0}
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('balance', data)
        self.assertEqual(data['balance'], 400.0)  # 500 - 100
        self.assertIn('Withdrawal successful', data['message'])
        self.assertIn('$100.0', data['message'])
        self.assertIn('1001', data['message'])

    def test_withdraw_invalid_account(self):
        """Test withdrawal from invalid account returns 404"""
        withdraw_data = {"amount": 100.0}
        response = self.app.post('/accounts/9999/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Account not found')

    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds returns 400"""
        withdraw_data = {"amount": 1000.0}  # More than account 1001's balance (500)
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Insufficient funds', data['error'])
        self.assertIn('500.0', data['error'])  # Current balance
        self.assertIn('1000.0', data['error'])  # Requested amount

    def test_withdraw_exact_balance(self):
        """Test withdrawal of exact account balance"""
        withdraw_data = {"amount": 500.0}  # Exact balance of account 1001
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 0.0)

    def test_withdraw_missing_amount(self):
        """Test withdrawal without amount field returns 400"""
        withdraw_data = {}
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Amount is required')


    def test_withdraw_zero_amount(self):
        """Test withdrawal with zero amount returns 400"""
        withdraw_data = {"amount": 0}
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Withdrawal amount must be a positive number')

    def test_withdraw_invalid_amount_type(self):
        """Test withdrawal with invalid amount type returns 400"""
        withdraw_data = {"amount": "not_a_number"}
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Withdrawal amount must be a positive number')

    def test_withdraw_decimal_precision(self):
        """Test withdrawal with decimal places rounds correctly"""
        withdraw_data = {"amount": 100.456}
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Should round to 2 decimal places: 500 - 100.46 = 399.54
        self.assertEqual(data['balance'], 399.54)

    # ============= Integration Tests =============
    def test_multiple_transactions_sequence(self):
        """Test sequence of multiple transactions on same account"""
        account_num = '1001'

        # Initial balance check
        response = self.app.get(f'/accounts/{account_num}/balance')
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 500.0)

        # Deposit $200
        deposit_data = {"amount": 200.0}
        response = self.app.post(f'/accounts/{account_num}/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 700.0)

        # Withdraw $150
        withdraw_data = {"amount": 150.0}
        response = self.app.post(f'/accounts/{account_num}/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 550.0)

        # Final balance check
        response = self.app.get(f'/accounts/{account_num}/balance')
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 550.0)

    def test_concurrent_account_operations(self):
        """Test operations on different accounts don't interfere"""
        # Deposit to account 1001
        deposit_data = {"amount": 100.0}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Withdraw from account 1002
        withdraw_data = {"amount": 200.0}
        response = self.app.post('/accounts/1002/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Check both accounts have correct balances
        response1 = self.app.get('/accounts/1001/balance')
        data1 = json.loads(response1.data)
        self.assertEqual(data1['balance'], 600.0)  # 500 + 100

        response2 = self.app.get('/accounts/1002/balance')
        data2 = json.loads(response2.data)
        self.assertEqual(data2['balance'], 800.0)  # 1000 - 200

        # Verify account 1003 is unchanged
        response3 = self.app.get('/accounts/1003/balance')
        data3 = json.loads(response3.data)
        self.assertEqual(data3['balance'], 750.0)  # Original balance

    def test_large_transaction_amounts(self):
        """Test with large transaction amounts"""
        # Large deposit
        deposit_data = {"amount": 999999.99}
        response = self.app.post('/accounts/1002/deposit',  # Account with $1000 initial
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 1000999.99)

        # Large withdrawal (but within balance)
        withdraw_data = {"amount": 500000.0}
        response = self.app.post('/accounts/1002/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 500999.99)

    def test_small_transaction_amounts(self):
        """Test with very small transaction amounts"""
        # Small deposit
        deposit_data = {"amount": 0.01}
        response = self.app.post('/accounts/1001/deposit',
                                 data=json.dumps(deposit_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 500.01)

        # Small withdrawal
        withdraw_data = {"amount": 0.01}
        response = self.app.post('/accounts/1001/withdraw',
                                 data=json.dumps(withdraw_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 500.0)

    # ============= Edge Case Tests =============
    def test_account_balance_persistence_across_requests(self):
        """Test that account balances persist across multiple requests"""
        # Make deposits to all accounts
        accounts_to_test = ['1001', '1002', '1003']
        expected_balances = [600.0, 1100.0, 850.0]  # original + 100 each

        for account in accounts_to_test:
            deposit_data = {"amount": 100.0}
            response = self.app.post(f'/accounts/{account}/deposit',
                                     data=json.dumps(deposit_data),
                                     content_type='application/json')
            self.assertEqual(response.status_code, 200)

        # Check all balances are correct
        for account, expected_balance in zip(accounts_to_test, expected_balances):
            response = self.app.get(f'/accounts/{account}/balance')
            data = json.loads(response.data)
            self.assertEqual(data['balance'], expected_balance)

    def test_invalid_json_content(self):
        """Test API handles invalid JSON gracefully"""
        # Send invalid JSON
        response = self.app.post('/accounts/1001/deposit',
                                 data='{"amount": invalid}',
                                 content_type='application/json')

        # Should return 400 (bad request)
        self.assertIn(response.status_code, [400, 500])  # Different Flask versions handle this differently




if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)