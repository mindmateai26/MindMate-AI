import os
import sys
import uvicorn

# Ensure project root is in python path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.main import app

if __name__ == "__main__":
    print("Starting MindMate AI server on http://127.0.0.1:8000 ...", flush=True)
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, log_level="info")
