# ATM Banking API  

A cloud-hosted **ATM Banking System API** built with **Flask + Flask-RESTX**, providing account management and transaction operations such as balance inquiries, deposits, and withdrawals. The project is deployed on **Google Cloud Run** and exposes a RESTful API with interactive Swagger documentation.  

---

## Live Deployment  

- **API Base URL**: [https://atm-api-435429241525.us-central1.run.app](https://atm-api-435429241525.us-central1.run.app)  
- **Swagger**: [https://atm-api-435429241525.us-central1.run.app/docs](https://atm-api-435429241525.us-central1.run.app/docs)  

---

## Features  

- Check account balance  
- Deposit money  
- Withdraw money


---

## Design Decisions & Approach  

### 1. **Framework Choice**  
I selected **Flask** for simplicity and **Flask-RESTX** for structured API design and automatic Swagger documentation. This provides a balance between lightweight implementation and professional API standards.  

### 2. **In-Memory Data Store**  
As been told in the assignment, I chose that account data is stored in a Python dictionary. This avoids external database dependencies and keeps the project easy to deploy.  

### 3. **Error Handling**  
I included explicit error responses for:  
- Invalid account numbers  
- Negative or zero deposits  
- Insufficient funds  
This ensures API consumers receive clear, predictable messages.  

### 4. **Cloud Deployment**  
As been told in the assignment, I chose **Google Cloud Run** because it allows containerized apps to be deployed with minimal setup.  
The API is packaged into a Docker container and deployed directly via `gcloud run deploy`.  

---

## Challenges Faced  

1. **Deployment Configuration**  
One of the biggest challenges was deploying the API to a cloud service instead of running it locally. This was a completely new area for me, and I had to learn the deployment process from scratch. Although it was challenging, it gave me valuable hands-on experience with cloud platforms and modern deployment practices.
2. **Swagger (API Documentation) Setup**  
Another challenge was setting up clear and user-friendly API documentation. I wanted the endpoints, parameters, and responses to be easy to explore and test. To achieve this, I used Flask-RESTX, which automatically generates Swagger documentation.
---

## API Endpoints  

### Get Balance  
`GET /accounts/<account_number>/balance`  

### Deposit  
`POST /accounts/<account_number>/deposit`  
```json
{
  "amount": 100
}
```  

### Withdraw  
`POST /accounts/<account_number>/withdraw`  
```json
{
  "amount": 50
}
``` 


---

## API Testing and Execution

You can test the API with different options:  
### Option 1: Using Swagger

[https://atm-api-435429241525.us-central1.run.app/docs](https://atm-api-435429241525.us-central1.run.app/docs)

### Option 2: Using the provided Unittest
```bash
python test_api.py
```

### Option 3: cURL
```bash
# Get balance
curl https://atm-api-435429241525.us-central1.run.app/accounts/1001/balance
# Deposit money
curl -X POST https://atm-api-435429241525.us-central1.run.app/accounts/1001/deposit -H "Content-Type: application/json" -d "{\"amount\": 100}"

# Withdraw money
curl -X POST https://atm-api-435429241525.us-central1.run.app/accounts/1001/withdraw -H "Content-Type: application/json" -d "{\"amount\": 50}"

# List all accounts
curl https://atm-api-435429241525.us-central1.run.app/accounts
```
### Option 4: PowerShell
```powershell
# Get balance
Invoke-WebRequest -Uri "https://atm-api-435429241525.us-central1.run.app/accounts/1001/balance" -Method GET

# Deposit money
Invoke-WebRequest -Uri "https://atm-api-435429241525.us-central1.run.app/accounts/1001/deposit" -Method POST -ContentType "application/json" -Body '{"amount": 100}'

# Withdraw money
Invoke-WebRequest -Uri "https://atm-api-435429241525.us-central1.run.app/accounts/1001/withdraw" -Method POST -ContentType "application/json" -Body '{"amount": 50}'
# List all accounts
Invoke-WebRequest -Uri "https://atm-api-435429241525.us-central1.run.app/accounts" -Method GET
```

---

##  Future Improvements  

- Replace in-memory storage
- Add authentication
- Add transaction history tracking  


---

 **Author**: Koren Chen 
