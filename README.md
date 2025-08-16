# 🏦 ATM System (Server-Side)

This project is a **server-side ATM system** built with **Python (Flask)** and deployed to **Heroku Cloud**.  
It provides REST API endpoints to perform basic banking operations:

- **Get Balance**
- **Deposit Money**
- **Withdraw Money**

All account data is stored **in-memory** (no database required).

---

## 🌍 Live Deployment

The server is hosted on **Heroku** at:

👉 [https://atm-system-demo.herokuapp.com](https://atm-system-demo.herokuapp.com)


---

## 📌 API Endpoints

### 1. Get Balance
**Request**
```bash
GET /accounts/<account_number>/balance



