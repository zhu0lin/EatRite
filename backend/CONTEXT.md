# EatRite Backend - Development Context

## Project Overview

EatRite is a nutrition tracking application with an Expo (React Native) frontend and FastAPI backend. This document provides context on the backend implementation completed so far.

## What Was Built

### Initial Goal
Create a FastAPI backend service folder structure with:
- Basic API setup with health check endpoint
- JWT-based authentication
- Minimal boilerplate code
- Integration-ready for Expo frontend

### Created Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Settings and environment configuration
│   ├── dependencies.py      # Shared JWT authentication dependencies
│   └── routers/
│       ├── __init__.py
│       ├── health.py        # Health check endpoint
│       └── auth.py          # Authentication endpoints (login, get current user)
├── requirements.txt         # Python dependencies
├── README.md               # Setup and usage documentation
└── CONTEXT.md              # This file
```

### Implemented Features

1. **FastAPI Application (`main.py`)**
   - Application initialization
   - CORS middleware configured for Expo (ports 8081, 19000, 19006)
   - Router inclusion for health and auth endpoints
   - Root endpoint with welcome message

2. **Configuration Management (`config.py`)**
   - Pydantic Settings for type-safe configuration
   - Environment variable support via `.env` file
   - JWT settings (secret key, algorithm, token expiration)
   - CORS origins configuration

3. **Health Check Endpoint (`routers/health.py`)**
   - `GET /api/v1/health` - Returns service status and timestamp
   - Useful for monitoring and confirming server is running

4. **Authentication System (`routers/auth.py`)**
   - `POST /api/v1/auth/login` - Login endpoint with OAuth2 password flow
   - `GET /api/v1/auth/me` - Get current authenticated user
   - JWT token generation and validation
   - Password hashing with bcrypt
   - Dummy user database (for development/testing)

5. **Shared Dependencies (`dependencies.py`)**
   - JWT token validation
   - Current user extraction from tokens
   - Reusable authentication dependencies

6. **Test User**
   - Username: `testuser`
   - Password: `secret`
   - Pre-hashed password in fake database

## Technical Challenges & Solutions

### 1. Python 3.13 Compatibility Issues

**Problem:** Initial package versions were not compatible with Python 3.13.

**Solution:**
- Updated `pydantic` from 2.5.0 to 2.10.3
- Updated `pydantic-core` to 2.27.1 (auto-installed with pydantic)
- Updated `fastapi` to 0.115.0
- Updated `uvicorn` to 0.32.1

### 2. Deprecated `datetime.utcnow()`

**Problem:** Python 3.13 shows warnings for `datetime.utcnow()` as it's deprecated.

**Solution:**
- Replaced all instances with `datetime.now(timezone.utc)`
- Updated imports to include `timezone` from datetime module
- Applied to both `auth.py` and `health.py`

### 3. bcrypt/passlib Compatibility

**Problem:** The latest bcrypt 5.0.0 has breaking changes incompatible with passlib 1.7.4, causing:
```
ValueError: password cannot be longer than 72 bytes
AttributeError: module 'bcrypt' has no attribute '__about__'
```

**Solution:**
- Downgraded bcrypt from 5.0.0 to 4.0.1
- Explicitly specified bcrypt version in requirements.txt
- Kept passlib at 1.7.4

### 4. SSL Certificate Issues on macOS

**Problem:** pip couldn't verify SSL certificates when installing packages.

**Solution:**
- Used `--trusted-host pypi.org --trusted-host files.pythonhosted.org` flags
- This is a common issue with Python installations on macOS

### 5. Type Hints for Python 3.13

**Problem:** Union type syntax (`X | None`) caused issues in some contexts.

**Solution:**
- Imported `Optional` and `Union` from typing module
- Used explicit `Optional[Type]` instead of `Type | None`
- Used `Union[Type1, Type2]` for complex unions

## Current State

### Server Status
✅ **Running successfully** on `http://localhost:8000`

### Working Endpoints

1. **Root Endpoint**
   ```bash
   GET /
   Response: {"message":"Welcome to EatRite API","version":"1.0.0","docs":"/docs"}
   ```

2. **Health Check**
   ```bash
   GET /api/v1/health
   Response: {"status":"healthy","timestamp":"2025-11-08T05:33:15.258187+00:00","service":"EatRite API"}
   ```

3. **Login**
   ```bash
   POST /api/v1/auth/login
   Content-Type: application/x-www-form-urlencoded
   Body: username=testuser&password=secret
   Response: {"access_token":"eyJ...", "token_type":"bearer"}
   ```

4. **Get Current User**
   ```bash
   GET /api/v1/auth/me
   Authorization: Bearer <token>
   Response: {"username":"testuser","email":"test@example.com","full_name":"Test User","disabled":false}
   ```

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies (requirements.txt)

```
fastapi==0.115.0              # Web framework
uvicorn[standard]==0.32.1     # ASGI server
python-jose[cryptography]==3.3.0  # JWT handling
passlib==1.7.4                # Password hashing
bcrypt==4.0.1                 # Bcrypt backend for passlib
python-multipart==0.0.12      # Form data parsing
python-dotenv==1.0.1          # Environment variable loading
pydantic==2.10.3              # Data validation
pydantic-settings==2.6.1      # Settings management
```

## Setup Instructions

### First Time Setup

1. **Navigate to backend directory:**
   ```bash
   cd /Users/zhuolin/Desktop/EatRite/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   # If SSL issues on macOS:
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   
   # Otherwise:
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Subsequent Runs

```bash
cd /Users/zhuolin/Desktop/EatRite/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Configuration

The application uses default values but can be configured via `.env` file:

```env
# Security - IMPORTANT: Change in production!
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
APP_NAME=EatRite API
VERSION=1.0.0
API_PREFIX=/api/v1

# CORS - Add your Expo URLs
CORS_ORIGINS=["http://localhost:8081", "http://localhost:19000", "http://localhost:19006"]
```

## Next Steps / Future Enhancements

### Immediate Priorities
- [ ] Add database integration (PostgreSQL/MongoDB)
- [ ] Implement user registration endpoint
- [ ] Replace fake_users_db with real database
- [ ] Add proper user model and database table

### Feature Development
- [ ] Create nutrition data models (foods, meals, logs)
- [ ] Implement meal tracking endpoints
- [ ] Add food database integration (e.g., USDA FoodData Central)
- [ ] Create user profile management endpoints
- [ ] Add nutritional goals and tracking
- [ ] Implement search functionality for foods

### Security Enhancements
- [ ] Generate secure SECRET_KEY (use `openssl rand -hex 32`)
- [ ] Implement password strength validation
- [ ] Add rate limiting
- [ ] Implement refresh tokens
- [ ] Add email verification for registration
- [ ] Implement password reset functionality

### DevOps & Quality
- [ ] Add comprehensive error handling
- [ ] Implement logging (structured logging with context)
- [ ] Create automated tests (pytest)
- [ ] Set up CI/CD pipeline
- [ ] Add API request/response validation
- [ ] Implement database migrations (Alembic)
- [ ] Add monitoring and alerting

### Documentation
- [ ] Expand API documentation with examples
- [ ] Create architecture diagram
- [ ] Document database schema
- [ ] Add contribution guidelines

## Integration with Expo Frontend

The backend is configured to accept requests from Expo development servers:
- `http://localhost:8081` - Expo default
- `http://localhost:19000` - Expo Metro bundler
- `http://localhost:19006` - Expo web

### Example Frontend Integration

```typescript
// Example login request from Expo app
const login = async (username: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });
  
  const data = await response.json();
  return data.access_token;
};
```

## Git Branch

Currently on branch: `backend/v1`

## Notes

- The current implementation uses an in-memory fake database for testing
- All passwords should be hashed before storage (handled by passlib/bcrypt)
- JWT tokens expire after 30 minutes (configurable)
- The server runs with hot-reload enabled for development (`--reload` flag)
- CORS is configured permissively for development; restrict in production

## Development Philosophy

This backend was built with:
1. **Minimal but complete** - Only essential features, fully functional
2. **Production patterns** - Following best practices (JWT, password hashing, etc.)
3. **Extensibility** - Easy to add new endpoints and features
4. **Type safety** - Using Pydantic for validation and type checking
5. **Developer experience** - Auto-generated docs, hot reload, clear structure

---

**Last Updated:** 2025-11-08  
**Python Version:** 3.13  
**FastAPI Version:** 0.115.0

