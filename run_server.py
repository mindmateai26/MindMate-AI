import os
import sys
import uvicorn

# Ensure project root is in python path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.main import app

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    print(f"Starting MindMate AI server on http://{host}:{port} ...", flush=True)
    uvicorn.run("backend.main:app", host=host, port=port, log_level="info")
