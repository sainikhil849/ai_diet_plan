# How to Run the AI-NutriCare Server

## Quick Start (Windows)

### Method 1: Double-click the batch file (Easiest)
1. Navigate to the `backend` folder
2. Double-click `start.bat`
3. The server will start automatically

### Method 2: Command Line

Open Command Prompt or PowerShell in the `backend` directory:

```bash
cd backend
python run_server.py
```

If port 8000 is busy, it will automatically find an available port (8001, 8002, etc.)

Or specify a custom port:
```bash
python run_server.py 8001
```

### Method 3: Using Python Module

```bash
cd backend
python -m app.main
```

---

## What the Server Does

Once running, you'll see:
```
============================================================
AI-NutriCare API Server
============================================================

Starting server on port 8000...
API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health

Press Ctrl+C to stop the server
============================================================

INFO:     Started server process [...]
[OK] Database initialized
[OK] Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Access the API

Once the server is running:

- **API Root:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

---

## Troubleshooting

### Issue: Port Already in Use

**Error:** `error 10048: only one usage of each socket address is normally permitted`

**Solution 1 (Automatic):** The updated script automatically finds an available port!

**Solution 2 (Manual):** Use a different port:
```bash
python run_server.py 8001
```

**Solution 3:** Stop the process using port 8000:
```powershell
# Find the process
netstat -ano | findstr :8000

# Kill the process (replace <PID> with the actual process ID)
taskkill /PID <PID> /F
```

### Issue: Module Not Found

**Solution:** Make sure you're in the `backend` directory:
```bash
cd backend
python run_server.py
```

### Issue: Python Not Found

**Solution:** Make sure Python is installed and in your PATH:
```bash
python --version
```

If that doesn't work, try:
```bash
python3 --version
# or
py --version
```

---

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## Testing the Server

### Quick Test:
Open your browser and go to:
- http://localhost:8000/health

You should see:
```json
{"status": "healthy", "service": "AI-NutriCare"}
```

### Test API Documentation:
Go to:
- http://localhost:8000/docs

You'll see the interactive API documentation (Swagger UI) where you can test all endpoints.

---

## Server Features

✅ Automatic port detection if 8000 is busy  
✅ Clear error messages  
✅ Database auto-initialization  
✅ Directory auto-creation  
✅ CORS enabled for React frontend  
✅ Interactive API documentation  

---

**The server will keep running until you press Ctrl+C!** 🚀
