# ATM Banking API  

A cloud-hosted **ATM Banking System API** built with **Flask + Flask-RESTX**, providing account management and transaction operations such as balance inquiries, deposits, and withdrawals. The project is deployed on **Google Cloud Run** and exposes a RESTful API with interactive Swagger documentation.  

---

## 🌍 Live Deployment  

- **API Base URL**: [https://atm-api-435429241525.us-central1.run.app](https://atm-api-435429241525.us-central1.run.app)  
- **Swagger UI**: [https://atm-api-435429241525.us-central1.run.app/docs](https://atm-api-435429241525.us-central1.run.app/docs)  

---

## 🚀 Features  

- Check account balance  
- Deposit money  
- Withdraw money (with insufficient funds check)  
- RESTful design with clear resource endpoints  
- Swagger/OpenAPI documentation auto-generated with Flask-RESTX  

---

## 🏗️ Design Decisions & Approach  

### 1. **Framework Choice**  
I selected **Flask** for simplicity and **Flask-RESTX** for structured API design and automatic Swagger documentation. This provides a balance between lightweight implementation and professional API standards.  

### 2. **In-Memory Data Store**  
For simplicity, account data is stored in a Python dictionary. This avoids external database dependencies and keeps the project easy to deploy.  
In a production system, this would be replaced with a persistent database (e.g., PostgreSQL, MySQL, or MongoDB).  

### 3. **Error Handling**  
I included explicit error responses for:  
- Invalid account numbers  
- Negative or zero deposits  
- Insufficient funds  
This ensures API consumers receive clear, predictable messages.  

### 4. **Cloud Deployment**  
I chose **Google Cloud Run** because it allows containerized apps to be deployed with minimal setup, free tier usage, and no need for manual server management.  
The API is packaged into a Docker container and deployed directly via `gcloud run deploy`.  

---

## ⚡ Challenges Faced  

1. **Swagger UI “X-Fields” Issue**  
Flask-RESTX automatically adds an `X-Fields` query parameter, which wasn’t necessary for this project. The solution was to configure the API with `mask=None` to hide this parameter.  

2. **Redirect on Root Path**  
Cloud Run health checks expect `/` to return a valid response. I solved this by adding a root route (`/`) that redirects to `/docs`.  

3. **Stateful Data in Stateless Environment**  
Since Cloud Run is stateless, the in-memory dictionary resets when a new container instance spins up. This was acceptable for demo purposes but would need a persistent DB in production.  

---

## 📖 API Endpoints  

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

## 🧪 Testing  

You can test the API with the included script:  

```bash
python test_api.py
```

Example output:  
```
=== Testing ATM API ===

GET Balance - Status: 200
Response: {"account_number": "1001", "balance": 500}
POST Deposit - Status: 200
Response: {"account_number": "1001", "balance": 600}
...
```

---

## ☁️ Deployment (Google Cloud Run)  

### 1. Build container image  
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/atm-api
```

### 2. Deploy to Cloud Run  
```bash
gcloud run deploy atm-api \
  --image gcr.io/YOUR_PROJECT_ID/atm-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 3. Get service URL  
```bash
gcloud run services describe atm-api --platform managed --region us-central1 --format "value(status.url)"
```

---

## 🔮 Future Improvements  

- Replace in-memory storage with PostgreSQL  
- Add authentication (JWT)  
- Add transaction history tracking  
- Container health checks for better resilience  

---

👨‍💻 **Author**: Koren Chen 
