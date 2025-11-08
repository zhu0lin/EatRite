# EatRite Backend API

FastAPI backend for the EatRite nutrition tracking application with food scanning, safety analysis, and Supabase integration.

## Features

- ✅ FastAPI framework
- ✅ Supabase Auth integration with fallback authentication
- ✅ JWT-based authentication
- ✅ User preferences management (allergies, dietary restrictions, health goals)
- ✅ Image scanning endpoint (MVP with mock data)
- ✅ Food safety analysis endpoint (MVP with mock data)
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

6. Configure your environment variables in `.env`:
   - Generate a secure secret key: `openssl rand -hex 32`
   - Add your Supabase project credentials (URL, anon key, service role key)
   - See `.env.example` for all available options

7. Set up Supabase (if using Supabase integration):
   - Create a Supabase project at https://supabase.com
   - Run the SQL schema from `.env.example` to create the `user_preferences` table
   - Copy your project URL and API keys to `.env`

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

#### Register

```
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

Creates a new user account.

#### Login (Form)

```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=test@example.com&password=secret
```

Returns a JWT access token. Use email as username for OAuth2 compatibility.

**Fallback Test Credentials:**
- Username (email): `test@example.com`
- Password: `secret`

#### Login (JSON)

```
POST /api/v1/auth/login-json
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "secret"
}
```

Alternative login endpoint that accepts JSON.

#### Get Current User

```
GET /api/v1/auth/me
Authorization: Bearer <your-jwt-token>
```

Returns the currently authenticated user's information.

### User Preferences

#### Get Preferences

```
GET /api/v1/preferences
Authorization: Bearer <your-jwt-token>
```

Returns user's dietary preferences, allergies, and health goals.

#### Create Preferences

```
POST /api/v1/preferences
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "allergies": ["peanuts", "shellfish"],
  "dietary_restrictions": ["vegan", "gluten-free"],
  "health_goals": "Weight loss and muscle gain"
}
```

Creates initial user preferences.

#### Update Preferences

```
PUT /api/v1/preferences
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "allergies": ["peanuts"],
  "dietary_restrictions": ["vegan"],
  "health_goals": "Maintain current weight"
}
```

Updates existing user preferences.

#### Delete Preferences

```
DELETE /api/v1/preferences
Authorization: Bearer <your-jwt-token>
```

Deletes all user preferences.

### Food Scanning & Analysis

#### Scan Image

```
POST /api/v1/scan-image
Authorization: Bearer <your-jwt-token> (optional)
Content-Type: multipart/form-data

file: <image-file>
```

Scans an image for food items and barcodes. Returns detected items with confidence scores.

**Phase 1 Note:** Currently returns mock data. Phase 2 will implement OpenCV, Pyzbar, and MediaPipe for real detection.

#### Analyze Food

```
POST /api/v1/analyze
Authorization: Bearer <your-jwt-token> (optional)
Content-Type: application/json

{
  "barcode": "012345678905",
  "product_name": "Sample Product"
}
```

Analyzes a food product for safety based on user preferences. Returns allergen warnings, dietary conflicts, and nutritional information.

**Phase 1 Note:** Currently returns mock data. Phase 3 will implement OpenFoodFacts API integration.

#### Get Scan History

```
GET /api/v1/scan-history?limit=10&offset=0
Authorization: Bearer <your-jwt-token>
```

Returns user's scan and analysis history (placeholder for Phase 6).

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings & Supabase client
│   ├── models.py            # Pydantic models for validation
│   ├── dependencies.py      # Shared dependencies (auth, etc.)
│   └── routers/
│       ├── __init__.py
│       ├── health.py        # Health check endpoint
│       ├── auth.py          # Authentication endpoints (Supabase + fallback)
│       ├── preferences.py   # User preferences CRUD
│       └── scan.py          # Image scanning & food analysis
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

**Register:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"secret","full_name":"Test User"}'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=secret"
```

**Get Current User:**
```bash
# Replace <TOKEN> with the access_token from login response
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <TOKEN>"
```

**Create Preferences:**
```bash
curl -X POST "http://localhost:8000/api/v1/preferences" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"allergies":["peanuts"],"dietary_restrictions":["vegan"],"health_goals":"Weight loss"}'
```

**Scan Image:**
```bash
curl -X POST "http://localhost:8000/api/v1/scan-image" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/path/to/image.jpg"
```

**Analyze Food:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"barcode":"012345678905","product_name":"Sample Product"}'
```

### Using the Interactive Docs

Visit http://localhost:8000/docs to test all endpoints interactively.

## Connecting to Expo Frontend

The API is configured to accept requests from:
- http://localhost:8081 (Expo default)
- http://localhost:19000 (Expo alternative)
- http://localhost:19006 (Expo web)

Update `CORS_ORIGINS` in `.env` if you need to add additional origins.

## Development Roadmap

### ✅ Phase 1 - Backend Setup (COMPLETED)
- ✅ Initialize FastAPI project
- ✅ Connect to Supabase (users + preferences)
- ✅ Create `/scan-image` and `/analyze` endpoints (MVP stubs)
- ✅ User authentication with Supabase Auth
- ✅ User preferences management

### 🚧 Phase 2 - Vision System (Next)
- [ ] Add OpenCV for image preprocessing
- [ ] Add Pyzbar for barcode detection
- [ ] Integrate MediaPipe for food classification
- [ ] Return structured detection results

### 🔜 Phase 3 - Food Data & Safety Logic
- [ ] Query OpenFoodFacts API for ingredients
- [ ] Implement allergen/diet conflict detection
- [ ] Personalized safety scoring

### 🔜 Phase 4 - Accessibility Features
- [ ] Add ElevenLabs voice output
- [ ] Support haptic feedback
- [ ] Color-coded safety responses

### 🔜 Phase 5 - Real-Time Scanning
- [ ] Enable continuous camera stream
- [ ] Real-time food/barcode recognition
- [ ] Instant feedback

### 🔜 Phase 6 - Enhancements
- [ ] Chatbot integration (Gemini API)
- [ ] Scan history storage & retrieval
- [ ] Performance optimizations
- [ ] On-device ML via TensorFlow Lite

## Supabase Setup

### Database Schema

Run this SQL in your Supabase SQL Editor to create the required tables:

```sql
-- Create user_preferences table
CREATE TABLE user_preferences (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  allergies TEXT[] DEFAULT '{}',
  dietary_restrictions TEXT[] DEFAULT '{}',
  health_goals TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id)
);

-- Enable Row Level Security
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Create policies for user access
CREATE POLICY "Users can view their own preferences"
  ON user_preferences FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own preferences"
  ON user_preferences FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own preferences"
  ON user_preferences FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own preferences"
  ON user_preferences FOR DELETE
  USING (auth.uid() = user_id);
```

### Fallback Mode

The API can run without Supabase configuration. If `SUPABASE_URL` and keys are not set:
- Authentication falls back to in-memory user storage
- Preferences are stored in memory (not persisted)
- Useful for development and testing

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in your `.env` file (use `openssl rand -hex 32`)
2. Configure Supabase with proper Row Level Security policies
3. Never commit `.env` file to version control
4. Keep `SUPABASE_SERVICE_ROLE_KEY` secret (server-side only)
5. Enable HTTPS in production
6. Add rate limiting
7. Implement proper error handling
8. Add request logging and monitoring
9. Validate and sanitize all user inputs
10. Set up automated backups for Supabase database

## License

See the main project LICENSE file.


