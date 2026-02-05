                                                HestaBit Training Development
                                                      Week 4 - Day 4
# Project – Security Report

## 1. Objective

This document summarizes the **security measures implemented**, **vulnerabilities tested**, and **results** for the Week4 Product Management API.  

**Learning Outcomes:**

- Secure and sanitize APIs  
- Implement robust request validation  
- Apply rate limiting and payload size limits  
- Prevent common web vulnerabilities such as NoSQL Injection, XSS, and Parameter Pollution  

---

## 2. Security Measures Implemented

### 2.1 Input Validation

- **Library Used:** JOI / Zod  
- **File:** `/middlewares/validate.js`  
- **Description:**  
  - Validates all incoming requests for User and Product endpoints  
  - Ensures required fields, types, and formats are strictly enforced  
  - Prevents malformed or malicious data from reaching the database  

**Example:**

- `POST /products` requires:
  - `name` (string, required)  
  - `price` (number, min: 0)  
  - `tags` (array of strings)  

---

### 2.2 Security Headers & Middleware

- **Libraries Used:** Helmet, CORS, express-rate-limit  
- **File:** `/middlewares/security.js`  
- **Description:**  
  - **Helmet:** Adds HTTP headers for XSS protection, HSTS, content sniffing prevention, etc.  
  - **CORS:** Restricts allowed origins to prevent unauthorized cross-origin requests  
  - **Rate Limiting:** Protects against brute-force attacks and request flooding  
  - **Payload Limits:** Restricts JSON body size to avoid denial-of-service attacks  

**Configuration Example:**

```
app.use(helmet());
app.use(cors({ origin: 'http://localhost:3000' }));
app.use(express.json({ limit: '10kb' }));

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per window
});
app.use(limiter);
```

---

### 2.3 NoSQL Injection Prevention

* **Description:**

  * Sanitized MongoDB query inputs
  * Prevented `$` operators and dot notation injection in user input

* **Test:** Attempted injection payloads in query parameters (`{"$gt": ""}`)

* **Result:** API correctly rejected invalid queries


![NoSQL Injection Test](screenshots/NoSQL_Injection.png)

---

### 2.4 XSS (Cross-Site Scripting) Prevention

* **Description:**

  * Input sanitization prevents scripts from being saved in database fields
  * Output encoding ensures no executable scripts are returned to clients

* **Test:** Submitted payloads like `<script>alert(1)</script>` in `description` and `name` fields

* **Result:** Payloads sanitized; no scripts executed in response


![XSS Prevention Test](screenshots/XSS_Attack.png)

---

### 2.5 Parameter Pollution Prevention

* **Description:**

  * Prevented duplicate query parameters that could override filters
  * Used Express middleware to normalize query parameters

* **Test:** Attempted requests like `/products?sort=price&sort=name`

* **Result:** Only the first valid parameter was processed; no unintended behavior

![Parameter Pollution Test](screenshots/hpp_attack.png)

---

### 2.6 Rate Limiting & Payload Size Enforcement

* **Description:**

  * Requests limited to 100 per 15 minutes per IP
  * Maximum payload size restricted to 10kb to prevent denial-of-service attacks

* **Test:**

  * Sent more than 100 requests in 15 minutes
  * Sent payload exceeding 10kb

* **Result:**

  * Exceeded requests returned 429 Too Many Requests
  * Oversized payloads returned 413 Payload Too Large

**Screenshot Placeholder:**
![Rate Limit & Payload Test](screenshots/Rate_limiting.png)

---

## 3. Security Test Cases

| Test Case              | Endpoint                                 | Expected Result       | Actual Result         | Status   |
| ---------------------- | ---------------------------------------- | --------------------- | --------------------- | -------- |
| Invalid price type     | POST /products                           | 400 error             | 400 error             | Passed |
| Missing required field | POST /products                           | 400 error             | 400 error             | Passed |
| NoSQL Injection        | GET /products?price[$gt]=0               | Request rejected      | Request rejected      | Passed |
| XSS attack             | POST /products {description: "<script>"} | Payload sanitized     | Payload sanitized     | Passed |
| Parameter pollution    | GET /products?sort=price&sort=name       | First param processed | First param processed | Passed |
| Exceed payload limit   | POST /products (20kb JSON)               | 413 Payload Too Large | 413 Payload Too Large | Passed |
| Rate limiting          | >100 requests/15min                      | 429 Too Many Requests | 429 Too Many Requests | Passed |
| Unauthorized CORS      | Request from unknown origin              | Blocked               | Blocked               | Passed |

---
