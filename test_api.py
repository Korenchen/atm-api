import requests

# Base URL for your Flask app
base_url = "https://atm-api-435429241525.us-central1.run.app"


def test_get_balance(account_number):
    """Test getting account balance"""
    response = requests.get(f"{base_url}/accounts/{account_number}/balance")
    print(f"GET Balance - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 40)


def test_deposit(account_number, amount):
    """Test depositing money"""
    response = requests.post(f"{base_url}/accounts/{account_number}/deposit",
                             json={"amount": amount})
    print(f"POST Deposit - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 40)


def test_withdraw(account_number, amount):
    """Test withdrawing money"""
    response = requests.post(f"{base_url}/accounts/{account_number}/withdraw",
                             json={"amount": amount})
    print(f"POST Withdraw - Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 40)


if __name__ == "__main__":
    # Test account 1001
    account = "1001"

    # Test sequence
    print("=== Testing ATM API ===\n")

    # Check initial balance
    test_get_balance(account)

    # Deposit money
    test_deposit(account, 100)

    # Check balance after deposit
    test_get_balance(account)

    # Withdraw money
    test_withdraw(account, 50)

    # Check final balance
    test_get_balance(account)

    # Test error cases
    print("=== Testing Error Cases ===\n")

    # Test invalid account
    test_get_balance("9999")

    # Test insufficient funds
    test_withdraw(account, 10000)

    # Test negative deposit
    test_deposit(account, -50)