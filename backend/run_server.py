"""
Simple script to run the AI-NutriCare API server
Run this from the backend directory: python run_server.py
"""
import sys
import os
import socket
from pathlib import Path

# Add current directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def is_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except OSError:
            return False


def find_available_port(start_port=8000, max_port=8100):
    """Find an available port starting from start_port"""
    for port in range(start_port, max_port):
        if is_port_available(port):
            return port
    return None


if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    # Check for port argument
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"[WARN] Invalid port number: {sys.argv[1]}. Using default port 8000")
    
    # Check if port is available
    if not is_port_available(port):
        print(f"[WARN] Port {port} is already in use. Finding an available port...")
        available_port = find_available_port(port + 1)
        if available_port:
            port = available_port
            print(f"[OK] Using port {port} instead")
        else:
            print("[ERROR] No available ports found in range 8000-8100")
            print("Please stop the process using port 8000 or specify a different port:")
            print("  python run_server.py 8001")
            sys.exit(1)
    
    print("="*60)
    print("AI-NutriCare API Server")
    print("="*60)
    print(f"\nStarting server on port {port}...")
    print(f"\n✅ Server URLs (USE THESE IN YOUR BROWSER):")
    print(f"   API Root:         http://localhost:{port}")
    print(f"   Health Check:     http://localhost:{port}/health")
    print(f"   API Docs (Swagger): http://localhost:{port}/docs")
    print(f"   API Docs (ReDoc):   http://localhost:{port}/redoc")
    print(f"\n⚠️  IMPORTANT: Use 'localhost' or '127.0.0.1', NOT '0.0.0.0'")
    print(f"\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port, reload=False, log_level="info")
    except KeyboardInterrupt:
        print("\n\n[OK] Server stopped by user")
    except OSError as e:
        if "10048" in str(e) or "already in use" in str(e).lower():
            print(f"\n[ERROR] Port {port} is already in use!")
            print("Try running with a different port:")
            print(f"  python run_server.py {port + 1}")
            print("\nOr stop the process using port 8000:")
            print("  netstat -ano | findstr :8000")
            print("  taskkill /PID <PID> /F")
        else:
            print(f"\n[ERROR] Failed to start server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
