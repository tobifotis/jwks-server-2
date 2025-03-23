# 📌 Extending the JWKS Server 
![Python Version](https://img.shields.io/badge/python-blue) 

This is a simple implementation of a **JWKS (JSON Web Key Set) server** that provides public keys for verifying **JWTs (JSON Web Tokens).** 

---

## 📌 Requirements

Before running the server, make sure you have the following installed:
- ✅ Flask
- ✅ Cryptography
- ✅ PyJWT
- ✅ Pytest

--- 

## ⚙️ Setup 
To get started, follow these steps: 

1️⃣ **Clone the repository:** 
```bash
git clone https://github.com/tobifotis/jwks-server-2.git
```
2️⃣ **Navigate into the project directory:** 
```bash 
cd path/jwks-server-2
```
3️⃣ **Run the server:** 
```bash 
python .\main.py 
```

---

## 📌 Example Response 
### **Request:** 
To retrieve the JSON Web Key Set (JWKS), run: 
```bash 
curl "http://127.0.0.1:8080/.well-known/jwks.json"
```

### **Response:**
```json
{
  "StatusCode": 200,
  "StatusDescription": "OK",
  "Content": {
    "keys": [
      {
        "alg": "RS256",
        "e": "AQAB",
        "kid": "1",
        "kty": "RSA",
        "n": "tM5LSP2cgZ6sR6lNgvSXdF_0xmBDns7LOgHVObk4GyCrf3uJeWbS8wiv_ediTqs6lBXWog4VMGWkOcp6rJXIKdOXd..."
      }
    ]
  },
  "RawContent": "HTTP/1.1 200 OK\nConnection: close\nContent-Length: 4235\nContent-Type: application/json\nDate: Sun, 23 Mar 2025 03:26:36 GMT\nServer: Werkzeug/3.0.3 Python/3.12.7"
}

```

--- 



## ⭐ Contributing 
Contributions are welcome! If you find any issues or improvements, feel free to open an issue or submit a pull request.
