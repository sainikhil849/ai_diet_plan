# How to Start the AI-NutriCare Server

## Quick Start

### Option 1: Using the Run Script (Recommended)

From the `backend` directory:

```bash
python run_server.py
```

This will:
- Start the server on http://localhost:8000
- Show you the API documentation URL
- Handle errors gracefully

### Option 2: Using Python Module

From the `backend` directory:

```bash
python -m app.main
```

### Option 3: Using Uvicorn Directly

From the `backend` directory:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload on code changes (useful for development).

---

## Access the API

Once the server is running:

- **API Root:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:** Make sure you're in the `backend` directory when running the server.

```bash
cd backend
python run_server.py
```

### Issue: "Port 8000 already in use"

**Solution:** Use a different port:

```bash
uvicorn app.main:app --port 8001
```

Or stop the process using port 8000:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill
```

### Issue: "kagglehub is missing"

**Solution:** kagglehub is **optional** and not needed for the main application. It's only required if you want to download datasets. The app will run fine without it.

If you see this error, it's been fixed in the latest version. Make sure you have the updated code.

---

## Requirements

**Required packages:**
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Python-multipart (for file uploads)

**Install all requirements:**
```bash
cd backend
pip install -r requirements.txt
```

**Note:** Some packages in requirements.txt are optional:
- `kagglehub` - Only needed for dataset downloading (optional)
- `easyocr` - Only needed for OCR features (optional, Tesseract can be used)
- ML/NLP libraries - Only needed for Weeks 3-8 features

---

## Running Tests

Before starting the server, you can test the system:

```bash
# From project root
python test_complete_system.py
```

This will verify all components are working correctly.

---

**Happy coding!** 🚀
