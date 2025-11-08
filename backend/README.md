# EatRite Backend API

FastAPI backend for the EatRite nutrition tracking application.

## Features

- ✅ FastAPI framework
- ✅ JWT-based authentication
- ✅ CORS configuration for Expo frontend
- ✅ Health check endpoint
- ✅ Password hashing with bcrypt
- ✅ Environment variable configuration

## Setup

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file:
```bash
cp .env.example .env
```

6. (Optional) Generate a secure secret key:
```bash
openssl rand -hex 32
```
Update the `SECRET_KEY` in your `.env` file with this value.

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Health Check

```
GET /api/v1/health
```

Returns the API status and current timestamp.

### Authentication

#### Login

```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=testuser&password=secret
```

Returns a JWT access token.

**Test Credentials:**
- Username: `testuser`
- Password: `secret`

#### Get Current User

```
GET /api/v1/auth/me
Authorization: Bearer <your-jwt-token>
```

Returns the currently authenticated user's information.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── dependencies.py      # Shared dependencies
│   └── routers/
│       ├── __init__.py
│       ├── health.py        # Health check endpoint
│       └── auth.py          # Authentication endpoints
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Testing the API

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/api/v1/health
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=secret"
```

**Get Current User:**
```bash
# Replace <TOKEN> with the access_token from login response
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <TOKEN>"
```

### Using the Interactive Docs

Visit http://localhost:8000/docs to test all endpoints interactively.

## Connecting to Expo Frontend

The API is configured to accept requests from:
- http://localhost:8081 (Expo default)
- http://localhost:19000 (Expo alternative)
- http://localhost:19006 (Expo web)

Update `CORS_ORIGINS` in `.env` if you need to add additional origins.

## Next Steps

- [ ] Add database integration (PostgreSQL/MongoDB)
- [ ] Implement user registration endpoint
- [ ] Add nutrition data models and endpoints
- [ ] Implement meal tracking functionality
- [ ] Add food database integration
- [ ] Set up proper user management
- [ ] Add input validation and error handling
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Set up automated tests

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in your `.env` file
2. Use a proper database instead of the in-memory fake database
3. Implement proper user registration and management
4. Enable HTTPS
5. Add rate limiting
6. Implement proper error handling
7. Add input validation
8. Set up logging and monitoring

## License

See the main project LICENSE file.


