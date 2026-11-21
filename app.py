import os
import socket
import secrets
import threading
import webbrowser
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

APP_NAME = "Pocket Drop"
BASE_DIR = Path(os.environ.get("POCKET_DROP_HOME", Path.home() / "PocketDrop"))
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024 * 1024  # 4 GB per request
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
PAIRING_PIN = os.environ.get("PPV_PIN") or f"{secrets.randbelow(1000000):06d}"

ALLOWED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".heif",
    ".dng", ".tif", ".tiff", ".bmp", ".mp4", ".mov", ".m4v", ".avi", ".mkv"
}

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

def unique_path(folder: Path, filename: str) -> Path:
    safe = secure_filename(filename) or "upload"
    candidate = folder / safe
    stem, suffix = candidate.stem, candidate.suffix
    n = 1
    while candidate.exists():
        candidate = folder / f"{stem}_{n}{suffix}"
        n += 1
    return candidate

def valid_pin(value):
    return secrets.compare_digest(str(value or ""), PAIRING_PIN)

@app.get("/")
def index():
    return render_template("index.html", app_name=APP_NAME)

@app.get("/api/info")
def info():
    return jsonify({"app": APP_NAME, "storage": str(UPLOAD_DIR), "requiresPin": True})

@app.post("/api/upload")
def upload():
    if not valid_pin(request.form.get("pin")):
        return jsonify({"ok": False, "error": "Incorrect pairing PIN."}), 401
    items = request.files.getlist("files")
    if not items:
        return jsonify({"ok": False, "error": "No files received."}), 400
    day_dir = UPLOAD_DIR / datetime.now().strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    saved, rejected = [], []
    for item in items:
        ext = Path(item.filename or "").suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            rejected.append({"name": item.filename, "reason": "Unsupported file type"})
            continue
        target = unique_path(day_dir, item.filename)
        item.save(target)
        saved.append({"name": target.name, "bytes": target.stat().st_size})
    return jsonify({"ok": bool(saved), "saved": saved, "rejected": rejected})

@app.get("/api/files")
def list_files():
    if not valid_pin(request.args.get("pin")):
        return jsonify({"ok": False, "error": "Incorrect pairing PIN."}), 401
    out=[]
    for p in sorted(UPLOAD_DIR.rglob("*"), key=lambda x: x.stat().st_mtime if x.is_file() else 0, reverse=True):
        if p.is_file(): out.append({"name": p.name, "path": str(p.relative_to(UPLOAD_DIR)), "bytes": p.stat().st_size})
        if len(out) >= 50: break
    return jsonify({"ok": True, "files": out})

@app.errorhandler(413)
def too_large(_):
    return jsonify({"ok": False, "error": "Upload is too large. Select fewer files and retry."}), 413

def run(host="0.0.0.0", port=5000, open_browser=True):
    ip = local_ip()
    print("\n" + "="*58)
    print(f"{APP_NAME} is ready")
    print(f"Laptop: http://127.0.0.1:{port}")
    print(f"Phone:  http://{ip}:{port}")
    print(f"Pairing PIN: {PAIRING_PIN}")
    print(f"Saving to: {UPLOAD_DIR}")
    print("Keep both devices on the same Wi-Fi network.")
    print("="*58 + "\n")
    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
    app.run(host=host, port=port, debug=False, threaded=True)

if __name__ == "__main__":
    run(port=int(os.environ.get("PORT", "5000")), open_browser=os.environ.get("NO_BROWSER") != "1")
