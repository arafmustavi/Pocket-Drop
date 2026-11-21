# Pocket Drop

Pocket Drop is a local-first Flask web app that lets you copy photos and videos from an iPhone or Android phone directly to a laptop over the same Wi-Fi network. Files do not pass through a cloud service.

## What you need
- A Windows, macOS, or Linux laptop with Python 3.10+ if running from source.
- An iPhone or Android phone with a modern browser.
- Both devices connected to the **same trusted Wi-Fi network**.
- For the Windows portable build, Windows 10/11 and Python are required only when building the EXE. The generated EXE can then run without a separate Python installation.

## Fast setup: run from source

### Windows
1. Extract the project ZIP to a normal folder such as `C:\PocketDrop`.
2. Open Command Prompt or PowerShell in that folder.
3. Create a virtual environment:
   `py -m venv .venv`
4. Activate it:
   `.venv\Scripts\activate`
5. Install dependencies:
   `pip install -r requirements.txt`
6. Start Pocket Drop:
   `python run.py`
7. The terminal prints a **Phone URL**, a **6-digit pairing PIN**, and the storage folder.
8. On the phone, while connected to the same Wi-Fi, open the Phone URL in Safari or Chrome.
9. Enter the PIN, choose photos/videos, and tap **Copy to laptop**.

### macOS / Linux
Run:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
Then open the printed Phone URL on the phone.

## First transfer test
Before selecting hundreds of files, test with **2 or 3 photos**. Confirm they appear under:
- Windows default: `C:\Users\<you>\PocketDrop\uploads\YYYY-MM-DD\`
- macOS/Linux default: `~/PocketDrop/uploads/YYYY-MM-DD/`

Pocket Drop preserves the uploaded originals and supports common formats including JPG, JPEG, PNG, HEIC, HEIF, DNG, MOV, MP4, M4V, TIFF, WebP, AVI and MKV. Duplicate filenames are retained with a numeric suffix instead of overwriting an existing file.

## Build the portable Windows EXE
1. Install Python 3.10+ on a Windows PC and ensure the Python launcher is available.
2. Extract the repository.
3. Double-click `scripts\build_windows.bat`, or run it from Command Prompt.
4. The script creates `.venv`, installs Flask, Waitress, PyInstaller and test dependencies, then packages the app.
5. The result is: `dist\PocketDrop.exe`.
6. Copy `PocketDrop.exe` wherever you want and run it.

**Important:** PyInstaller builds for the operating system on which it runs. Build the Windows EXE on Windows.

## Windows Firewall prompt
The first time Pocket Drop listens on the network, Windows Defender Firewall may display a prompt. Allow access on **Private networks** only. Do not enable Public networks unless you understand the exposure.

If no prompt appears and the phone cannot connect:
1. Open **Windows Security > Firewall & network protection > Allow an app through firewall**.
2. Allow Python or PocketDrop on the current **Private** network.
3. Alternatively, allow inbound TCP port `5000` for Private networks only.

## Configuration
Pocket Drop supports environment variables:
- `PORT=5000` changes the listening port.
- `PPV_PIN=123456` sets a fixed pairing PIN. If omitted, a random PIN is generated at startup.
- `POCKET_DROP_HOME=D:\PhoneBackup` changes the local storage root.
- `NO_BROWSER=1` prevents the laptop browser from opening automatically.

## Troubleshooting

### Phone says the site cannot be reached
- Confirm the laptop and phone are on the **same Wi-Fi SSID**.
- Use the exact **Phone URL** printed by Pocket Drop, not `127.0.0.1`. `127.0.0.1` on the phone means the phone itself.
- Keep Pocket Drop running while connecting.
- Temporarily disconnect a VPN on either device. VPN clients can prevent LAN access.
- Check Windows Firewall and allow PocketDrop/Python on **Private networks**.
- Guest Wi-Fi, hotel Wi-Fi, corporate Wi-Fi and some routers enable **AP/client isolation**, which prevents devices from talking to one another. Use a trusted home network or another network where local-device communication is allowed.

### PIN rejected
- Use the 6-digit PIN printed in the current Pocket Drop terminal window.
- Restarting Pocket Drop generates a new PIN unless `PPV_PIN` is configured.

### Upload stops or fails
- Keep the phone browser open and the screen awake during large transfers.
- Start again with fewer files. For reliability, use batches such as **50-200 items** rather than an entire multi-thousand-photo library at once.
- Confirm the laptop has enough free disk space.
- Very large individual requests are capped at **4 GB** by the Flask configuration.
- If Wi-Fi disconnects, already completed files remain on the laptop; retry the failed items.

### iPhone cannot find all photos
The browser file picker is controlled by iOS. Tap **Choose Files/Photo Library**, grant access when requested, and select the originals you want to copy. Photos stored only in iCloud may need to download to the iPhone before the browser can upload them.

### HEIC files copied successfully but Windows cannot preview them
Pocket Drop copies HEIC/HEIF originals without converting them. Preview support depends on the laptop's installed codecs. The copied file itself is still preserved.

### Android selection behaves differently
Android file pickers vary by manufacturer and browser. Chrome generally exposes Photos/Gallery or the system Files picker. Select photos/videos and return to Pocket Drop; the web page then shows the transfer queue.

### EXE does not start
- Build `PocketDrop.exe` on Windows rather than Linux/macOS.
- Re-run `scripts\build_windows.bat` and inspect any error before the window closes.
- If security software quarantines a self-built unsigned executable, build directly from the repository yourself and review the source. Production distribution should use Windows code signing.

### Port 5000 is already in use
In Command Prompt:
`set PORT=5050 && python run.py`
Then use the new Phone URL printed by Pocket Drop.

### Wrong IP address is shown
If the laptop has VPNs, virtual adapters, Docker, Hyper-V, or multiple network connections, automatic IP detection can select an unusable interface. Find the laptop's Wi-Fi IPv4 address with `ipconfig` on Windows, then open `http://<WIFI-IP>:5000` on the phone.

## Security and privacy
Pocket Drop is designed for a **trusted private LAN**. The pairing PIN prevents casual uploads, but the current version uses HTTP rather than HTTPS. Do not port-forward it, publish port 5000 to the internet, or use it as an internet-facing service.

For a future production-grade release, consider HTTPS/TLS, resumable/chunked transfers, cryptographic checksums, device sessions, QR-code pairing, storage-space checks, EXIF-based organization and signed Windows releases.

## GitHub setup
```bash
git init
git add .
git commit -m "Initial Pocket Drop release"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

## Project structure
- `app.py` - Flask application and upload API
- `run.py` - Waitress production-style local server launcher
- `templates/` - mobile web interface
- `static/` - CSS and JavaScript
- `scripts/build_windows.bat` - Windows EXE builder
- `pocket_drop.spec` - PyInstaller configuration
- `tests/` - basic Flask tests

## License
MIT License. See `LICENSE`.
