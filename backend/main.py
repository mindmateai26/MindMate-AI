import os
import sys

# Ensure project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

try:
    from backend.routes import assessment, chat, emotion
except ImportError:
    from .routes import assessment, chat, emotion

app = FastAPI(
    title="MindMate AI API",
    description="AI-Powered Mental Wellness Screening, Prediction & Companion API",
    version="2.0.0"
)

# Enable CORS for local development and diverse ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(assessment.router)
app.include_router(chat.router)
app.include_router(emotion.router)

@app.get("/api/health", tags=["System"])
def health_check():
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    return {
        "status": "healthy",
        "app": "MindMate AI",
        "version": "2.0.0",
        "geminiConfigured": bool(gemini_key),
        "message": "MindMate AI Backend is operational."
    }

# Mount Frontend static files
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.abspath(os.path.join(current_dir, "..", "frontend"))

if os.path.exists(frontend_dir):
    css_dir = os.path.join(frontend_dir, "css")
    js_dir = os.path.join(frontend_dir, "js")
    
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_home():
        index_file = os.path.join(frontend_dir, "index.html")
        return FileResponse(index_file)

    @app.get("/{page_name}.html")
    def serve_html_page(page_name: str):
        target_file = os.path.join(frontend_dir, f"{page_name}.html")
        if os.path.exists(target_file):
            return FileResponse(target_file)
        return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"Starting MindMate AI on http://{host}:{port}...")
    uvicorn.run(app, host=host, port=port)
