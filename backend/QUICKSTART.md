# EatRite Backend - Quick Start Guide

## Phase 1 Implementation Complete! 🎉

All Phase 1 features have been successfully implemented. You now have a fully functional backend with:
- Supabase Auth integration
- User preferences management
- Image scanning endpoint (MVP)
- Food analysis endpoint (MVP)

## Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd /Users/zhuolin/Desktop/EatRite/backend
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Environment (Optional for Testing)

For quick testing, you can skip this step and use fallback mode:

```bash
# Optional: Copy and configure .env for Supabase
cp .env.example .env
# Edit .env with your Supabase credentials
```

### Step 3: Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at **http://localhost:8000**

## Test Your API

### Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs in your browser
2. You'll see an interactive API documentation
3. Try the endpoints directly from the browser!

### Quick Test with cURL

```bash
# 1. Health Check
curl http://localhost:8000/api/v1/health

# 2. Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123","full_name":"Demo User"}'

# 3. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=demo123"
  
# Save the access_token from the response

# 4. Create preferences (replace YOUR_TOKEN with actual token)
curl -X POST "http://localhost:8000/api/v1/preferences" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"allergies":["peanuts","shellfish"],"dietary_restrictions":["vegan"],"health_goals":"Weight loss"}'

# 5. Test food analysis
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"barcode":"012345678905","product_name":"Test Product"}'
```

## What's Working Now?

### ✅ Authentication
- User registration and login
- JWT token-based authentication
- Works with or without Supabase

### ✅ User Preferences
- Create, read, update, delete preferences
- Store allergies, dietary restrictions, health goals
- Persists to Supabase or in-memory fallback

### ✅ Image Scanning (MVP)
- Upload image endpoint ready
- Returns mock detection data
- Ready for Phase 2 computer vision integration

### ✅ Food Analysis (MVP)
- Analyzes products by barcode or name
- Returns mock allergen warnings and nutrition info
- Ready for Phase 3 OpenFoodFacts integration

## Fallback Mode vs Supabase Mode

### Fallback Mode (No Configuration Needed)
- Uses in-memory storage
- Great for testing and development
- Data doesn't persist between server restarts
- Default test user: `test@example.com` / `secret`

### Supabase Mode (Recommended for Production)
1. Create a Supabase project at https://supabase.com
2. Run the SQL schema from `.env.example`
3. Add your Supabase credentials to `.env`
4. Restart the server

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
uvicorn app.main:app --reload

# Start on different port
uvicorn app.main:app --reload --port 8001

# View logs with more detail
uvicorn app.main:app --reload --log-level debug

# Run without reload (production)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Supabase Connection Issues
The API will automatically fall back to in-memory storage if Supabase is unavailable. Check:
- `.env` file exists and has correct credentials
- Supabase project is active
- Network connection is working

## Next Steps

### Ready for Phase 2?
When you're ready to implement real computer vision:
1. Add OpenCV, Pyzbar, MediaPipe to requirements.txt
2. Update `app/routers/scan.py` with actual detection logic
3. Test with real food images

### Want to Use Supabase?
1. Create project at https://supabase.com
2. Copy `.env.example` to `.env`
3. Run the SQL schema (in `.env.example` comments)
4. Add your credentials to `.env`
5. Restart the server

### Test with Expo Frontend?
The backend is configured to accept requests from:
- http://localhost:8081
- http://localhost:19000
- http://localhost:19006

Just point your Expo app to `http://localhost:8000/api/v1`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Full README**: `README.md`
- **Implementation Details**: `PHASE_1_SUMMARY.md`

## Need Help?

Check these files:
- `README.md` - Complete documentation
- `PHASE_1_SUMMARY.md` - Implementation details
- `.env.example` - Configuration options
- `CONTEXT.md` - Development history

---

**Status**: ✅ Phase 1 Complete  
**Ready for**: Phase 2 (Vision System)

