import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_all_assets_and_pages():
    endpoints = [
        ("/", "text/html"),
        ("/companion.html", "text/html"),
        ("/assessment.html", "text/html"),
        ("/dashboard.html", "text/html"),
        ("/result.html", "text/html"),
        ("/about.html", "text/html"),
        ("/css/style.css", "text/css"),
        ("/js/app.js", "application/javascript"),
        ("/js/companion.js", "application/javascript"),
        ("/js/assessment.js", "application/javascript"),
        ("/js/dashboard.js", "application/javascript"),
        ("/static/css/style.css", "text/css"),
    ]

    for ep, expected_mime in endpoints:
        res = client.get(ep)
        assert res.status_code == 200, f"Failed for {ep}: got {res.status_code}"
        ct = res.headers.get("content-type", "")
        assert expected_mime in ct, f"Failed mime for {ep}: expected {expected_mime}, got {ct}"
        print(f"[PASS] {ep:<25} -> 200 OK ({len(res.content)} bytes, {ct})")

    # Check companion.html links
    companion_html = client.get("/companion.html").text
    assert "/css/style.css" in companion_html, "companion.html must link /css/style.css"
    assert "/js/companion.js" in companion_html, "companion.html must link /js/companion.js"
    print("[PASS] companion.html correctly links /css/style.css and /js/companion.js")

    # Test sending one chat message to chat endpoint
    chat_res = client.post("/api/chat", json={"message": "Hello, I am testing the companion styling!"})
    assert chat_res.status_code == 200, "Chat request failed"
    chat_data = chat_res.json()
    assert "text" in chat_data
    assert "moodTag" in chat_data
    print(f"[PASS] Chat test message verified successfully:")
    print(f"       Mood: {chat_data['moodTag']}")
    print(f"       Reply: {chat_data['text']}")

if __name__ == "__main__":
    test_all_assets_and_pages()
    print("\nAll Frontend Assets & Companion Verification PASSED!")
