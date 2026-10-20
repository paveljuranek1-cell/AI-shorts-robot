# Subscription Management REST API

A comprehensive, production-ready RESTful API for managing user subscription plans and lifecycle, built with **FastAPI**, **Pydantic v2**, and **pytest**.

## Features

- **Plan Management**: View available subscription tiers (Free, Pro, Enterprise) and their features.
- **Subscription Lifecycle**: Create subscriptions, fetch subscription status, change plans/billing cycles (monthly vs. yearly), toggle auto-renewal, and cancel subscriptions.
- **Data Validation & Error Handling**: Strict email format and request body validation powered by Pydantic v2 with custom exception handlers.
- **Security & Authentication**: Protected write endpoints requiring API Key authentication via `X-API-Key` header.
- **Layered Architecture**: Decoupled routes, service layer, and repository pattern for easy extension to persistent databases (e.g. PostgreSQL, SQLite).
- **Automated Testing**: 100% test coverage for API endpoints and business logic with `pytest` and `httpx`.

---

## Directory Structure

```
subscription-api/
├── app/
│   ├── __init__.py
│   ├── auth.py          # API Key security dependency
│   ├── main.py          # FastAPI application initialization & exception handlers
│   ├── repository.py    # Abstract base repository & in-memory store
│   ├── router.py        # REST API route handlers
│   ├── schemas.py       # Pydantic v2 models and enums
│   └── service.py       # Business logic and domain validations
├── tests/
│   └── test_api.py      # Integration and unit tests
└── requirements.txt     # Dependency definitions
```

---

## Quick Start

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Installation
Install the dependencies:
```bash
pip install -r subscription-api/requirements.txt
```

### 3. Running the Server
To start the FastAPI server with auto-reload:
```bash
PYTHONPATH=subscription-api uvicorn app.main:app --reload --port 8000
```
The API interactive documentation will be available at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Configuration & Security

Authentication is enforced on subscription endpoints using the `X-API-Key` HTTP header.

- **Default API Key**: `secret-api-key`
- You can override the expected key by setting the `API_KEY` environment variable:
  ```bash
  export API_KEY="your-custom-api-key"
  ```

---

## Running Tests

Run the full test suite using `pytest`:
```bash
PYTHONPATH=subscription-api pytest subscription-api/tests
```

---

## API Documentation

### Public Endpoints

#### `GET /health`
Returns system health status.
- **Response**: `200 OK`
  ```json
  { "status": "healthy" }
  ```

#### `GET /api/v1/plans`
Retrieves all available subscription plans.
- **Response**: `200 OK`
  ```json
  [
    {
      "id": "pro",
      "name": "Pro Tier",
      "description": "Advanced tools for professionals",
      "price_monthly": 19.99,
      "price_yearly": 199.99,
      "features": ["Unlimited Projects", "Priority Support", "Advanced Analytics", "API Access"]
    }
  ]
  ```

#### `GET /api/v1/plans/{plan_id}`
Retrieves details for a specific plan (`free`, `pro`, `enterprise`).

---

### Protected Endpoints (Requires `X-API-Key` Header)

#### `POST /api/v1/subscriptions`
Creates a new active subscription for a user.
- **Headers**: `X-API-Key: secret-api-key`
- **Request Body**:
  ```json
  {
    "user_email": "user@example.com",
    "plan_id": "pro",
    "billing_cycle": "monthly"
  }
  ```
- **Response**: `201 Created`

#### `GET /api/v1/subscriptions/{subscription_id}`
Retrieves subscription details by UUID.
- **Headers**: `X-API-Key: secret-api-key`
- **Response**: `200 OK`

#### `PATCH /api/v1/subscriptions/{subscription_id}`
Updates an active subscription's plan, billing cycle, or auto-renew option.
- **Headers**: `X-API-Key: secret-api-key`
- **Request Body**:
  ```json
  {
    "plan_id": "enterprise",
    "billing_cycle": "yearly",
    "auto_renew": true
  }
  ```
- **Response**: `200 OK`

#### `DELETE /api/v1/subscriptions/{subscription_id}`
Cancels an active subscription.
- **Headers**: `X-API-Key: secret-api-key`
- **Response**: `200 OK`
