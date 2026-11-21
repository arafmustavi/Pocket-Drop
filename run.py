import os
import threading
import webbrowser
from waitress import serve
from app import app, local_ip, PAIRING_PIN, UPLOAD_DIR

port = int(os.environ.get("PORT", "5000"))
ip = local_ip()
print(f"Pocket Drop\nPhone URL: http://{ip}:{port}\nPairing PIN: {PAIRING_PIN}\nStorage: {UPLOAD_DIR}")
if os.environ.get("NO_BROWSER") != "1":
    threading.Timer(1.0, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
serve(app, host="0.0.0.0", port=port, threads=8)
