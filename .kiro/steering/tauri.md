---
inclusion: fileMatch
fileMatchPattern: "app/tauri/**"
---

# Tauri v2 Desktop Shell Standards (2026)

## Version & Setup

- Tauri v2 (stable 2026). Use v2 APIs exclusively — not v1.
- Rust edition 2024.
- Use Tauri's official sidecar feature for bundling the Python backend.

## Architecture Principle

Tauri is a **thin shell**. Its only jobs:
1. Bundle and spawn the FastAPI Python process as a sidecar
2. Open a webview pointing to the local FastAPI server
3. Handle app lifecycle (startup, shutdown, crash recovery)
4. Provide OS-level features if needed (file dialogs, system tray, notifications)

All application logic lives in FastAPI/Python. Minimal Rust code.

## Sidecar Pattern (Python Backend)

Tauri's sidecar feature bundles external binaries with the app:

- Bundle the Python backend as a PyInstaller executable (single file)
- Configure in `tauri.conf.json` under `bundle.externalBin`
- Name follows Tauri convention: `backend-x86_64-pc-windows-msvc` (platform-specific suffix)
- On startup: spawn sidecar, read stdout for port number, open webview to that URL
- On shutdown: send graceful shutdown signal to sidecar, wait 3s, force-kill if needed

## Process Coordination

```
Startup:
1. Tauri main() starts
2. Spawn sidecar (FastAPI binary) with a random port argument
3. Sidecar prints JSON to stdout: {"port": 54321, "status": "ready"}
4. Tauri reads stdout, extracts port
5. Open webview to http://localhost:{port}

Shutdown:
1. User closes window OR app quit event
2. Send SIGTERM (or equivalent) to sidecar process
3. Wait up to 3 seconds for graceful exit
4. Force-kill if still running
5. Tauri process exits

Crash Recovery:
1. Monitor sidecar process handle
2. If process exits unexpectedly:
   - Show error overlay in webview ("Backend crashed, restarting...")
   - Attempt to respawn sidecar (max 3 retries)
   - If retries exhausted: show permanent error with "Quit" button
```

## Configuration (`tauri.conf.json`)

```json
{
  "productName": "post-kit",
  "identifier": "com.postkit.app",
  "build": {
    "devUrl": "http://localhost:8000",
    "frontendDist": "http://localhost:8000"
  },
  "app": {
    "windows": [
      {
        "title": "post-kit",
        "width": 1280,
        "height": 800,
        "minWidth": 1024,
        "minHeight": 600,
        "decorations": true,
        "resizable": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; connect-src http://localhost:*; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "externalBin": ["backend"]
  }
}
```

## Security

- CSP: only allow connections to localhost.
- No remote URLs in webview — everything served from local FastAPI.
- Disable navigation to external origins.
- No `tauri://` protocol usage unless specifically needed.
- Disable devtools in production builds.

## Rust Code Style

- Keep `main.rs` under 100 lines.
- Use Tauri's plugin system for any OS-level features (don't implement manually).
- Error handling: use `anyhow` for the thin shell code. Log errors, don't panic.
- No complex Rust logic — if it can be done in Python/FastAPI, do it there.

## Build & Distribution

- `cargo tauri build` for production binaries.
- Target all platforms: Windows (.msi/.exe), macOS (.dmg), Linux (.deb/.AppImage).
- The sidecar binary must be built separately (PyInstaller) before Tauri build.
- Build pipeline:
  1. `pyinstaller --onefile app/backend/main.py` → produces backend executable
  2. Place in `app/tauri/src-tauri/binaries/` with platform suffix
  3. `cargo tauri build` → bundles everything into installer

## Development Mode

- Dev: run FastAPI directly with `uvicorn` on port 8000, Tauri webview points to it
- No need to build sidecar during development — just `cargo tauri dev` with `devUrl` set
- Hot reload: uvicorn `--reload` for backend, Tauri auto-reloads webview on page changes
