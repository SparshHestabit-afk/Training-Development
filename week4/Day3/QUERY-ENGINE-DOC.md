                                            HestaBit Training Development
                                                    Week 4 - Day 3

# Project – Query Engine & API Architecture Documentation

## 1. Objective

This document provides a **comprehensive overview of the Product API’s query engine, architecture, and error-handling strategies**. It demonstrates how the API was designed to:

- Handle complex, production-grade queries  
- Implement dynamic filtering, sorting, and pagination  
- Manage soft deletes safely  
- Ensure robust error boundaries and consistent error reporting  

**Learning Outcomes Achieved:**

- Design modular Controller → Service → Repository architecture  
- Build dynamic search engines with regex, OR/AND conditions  
- Implement soft deletes and restoration logic  
- Apply centralized, typed error handling for production readiness  

---

## 2. System Architecture

### 2.1 Controller → Service → Repository Flow

The API follows a **layered architecture**, ensuring clear separation of concerns:

```

Client Request → Controller → Service → Repository → Database → Response

```

- **Controller:** Handles HTTP requests, validates inputs, formats responses  
- **Service:** Implements business logic, filtering, and orchestration of repository methods  
- **Repository:** Performs database operations, including queries, soft delete, and restoration  

**Conceptual Note:** This flow ensures that the API is maintainable, testable, and scalable. Business logic is isolated from request/response handling and data persistence.

---

## 3. Dynamic Filters & Sorting

The API supports **advanced query capabilities** to fetch products efficiently.

### 3.1 Query Parameters

| Parameter | Description |
|-----------|-------------|
| `search` | Case-insensitive regex search on `name` and `description` |
| `minPrice` / `maxPrice` | Filter products within a price range |
| `tags` | Comma-separated list; returns products matching any tag (`$in`) |
| `sort` | Format: `field:order` (asc/desc). Default: `createdAt:desc` |
| `includeDeleted` | Boolean; include soft-deleted products if `true` |

**Example Request:**

```

GET /products?search=phone&minPrice=100&maxPrice=500&sort=price:desc&tags=apple,samsung

```
## Dynamic Filter (Example Request)
![Dynamic Filter Example](screenshots/Main_Query.png)  

## Search Filter

![Search Filter Example](screenshots/Main_Query.png)  
---

### 3.2 Implementation Details

- Query parameters are **parsed and sanitized** in the service layer  
- Strings are converted to appropriate types (`Number`, `Array`)  
- **MongoDB dynamic queries** are built using `$or` and `$and` conditions  
- Pagination is implemented with `limit` and `skip`  
- Response structure:

```
{
  "data": [...],
  "pagination": {
    "total": 120,
    "page": 1,
    "limit": 10,
    "pages": 12
  }
}
```
* **Command Line Interface look**

![An Image of implementation (cli)](screenshots/Product_list_cli.png)

* **Browser Look**
![An Image of implementation](screenshots/Product_List.png)

**Conceptual Note:** This approach ensures **flexible querying** without modifying backend code for every filter combination.

---
## 4. Product Functionallities

### 4.1 Soft Delete Functionality

Soft deletes allow products to be marked as deleted without removing them permanently from the database.

* **Deleted Flag:** `deletedAt` timestamp
* **Endpoints:**

| Endpoint                            | Action                                             |
| ----------------------------------- | -------------------------------------------------- |
| `DELETE /products/:id`              | Marks product as deleted (`deletedAt = timestamp`) |
| `GET /products?includeDeleted=true` | Returns all products, including soft-deleted ones  |

**Implementation Highlights:**

* Repository methods handle soft delete and restore logic
* Default queries **exclude deleted products** unless `includeDeleted=true`
* Ensures **data safety and auditability**

![Soft Delete Example](screenshots/Delete_Product.png)

**Conceptual Note:** Soft delete allows recovery of deleted items and provides an audit trail for administrative purposes.

### 4.2 Restore Product Functionality

Restore product allows to revoke the action performed during soft delete, making the product visible again, and removing it from soft_delete mark, from the database.

* **Deleted Flag:** `deletedAt` timestamp -> null
* **Endpoints:**

| Endpoint                            | Action                                             |
| ----------------------------------- | -------------------------------------------------- |
| `PATCH /products/:id/restore`       | Marks product as deleted (`deletedAt = null` again)|
| `GET /products?includeDeleted=false`| Returns all products, including soft-deleted ones  |

**Implementation Highlights:**

* Repository methods handle restore product and restore logic.
* Default queries **include deleted products** ir-respective of  `includeDeleted=true`
* Ensures **data safety and auditability**

* **Command Line Interface look**
![Restore Product](screenshots/Restore_Product_cli.png)

* **Browser look**
![Restore Product](screenshots/Product_after_Restore.png)

---

## 5. Advanced Error Handling

### 5.1 Global Error Format

All API errors follow a **consistent, structured format**:

```
{
  "success": false,
  "message": "Product not found",
  "code": "PRODUCT_NOT_FOUND",
  "timestamp": "2026-02-05T10:48:24.713Z",
  "path": "/products/12345"
}

```

### 5.2 Implementation

* **Typed Errors:** Custom error classes with `statusCode` and `code`
* **Centralized Middleware:** `/middlewares/error.middleware.js` captures all errors and formats responses uniformly
* **Benefits:** Simplifies debugging, provides consistency across the API, and improves client-side error handling

**Conceptual Note:** Centralized error handling is critical for production APIs, ensuring that all errors are logged, categorized, and returned in a predictable format.

---

## 6. Test Cases & Examples

| Feature            | Endpoint                                | Test Description                                     | Expected Result                 | Actual Result                   | Status   |
| ------------------ | --------------------------------------- | ---------------------------------------------------- | ------------------------------- | ------------------------------- | -------- |
| Search by name     | GET /products?search=phone              | Returns products with "phone" in name or description | Matches expected items        | Matches expected items        | Passed |
| Price filter       | GET /products?minPrice=100&maxPrice=500 | Products within price range                          | Filtered correctly            | Filtered correctly            | Passed |
| Tag filter         | GET /products?tags=apple,samsung        | Products with specified tags                         | Filtered correctly            | Filtered correctly            | Passed |
| Sort by price desc | GET /products?sort=price:desc           | Products sorted descending by price                  | Correct order                 | Correct order                 | Passed |
| Soft delete        | DELETE /products/:id                    | Marks product as deleted                             | deletedAt timestamp populated | deletedAt timestamp populated | Passed |
| Include deleted    | GET /products?includeDeleted=true       | Returns soft-deleted products                        | Returned                      | Returned                      | Passed |
| Invalid ID         | GET /products/invalidId                 | Returns structured error                             | 400 Bad Request               | 400 Bad Request               | Passed |
