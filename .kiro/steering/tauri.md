---
inclusion: fileMatch
fileMatchPattern: "app/tauri/**"
---

# Tauri v2 — Thin Shell, Maximum Delegation

Tauri's job: bundle, launch, and manage the Python backend. That's it. Keep Rust minimal.

## Single Responsibility

- `main.rs` — ONE job: spawn sidecar, wait for ready, open webview, handle shutdown.
- No application logic in Rust. If it can be done in Python → do it in Python.
- No Tauri commands (invoke) unless the feature requires OS-level access that Python can't do.

## Sidecar Pattern (2026 Standard for Tauri + Python)

Tauri v2 has first-class sidecar support. Use it:

```
Build Pipeline:
1. PyInstaller bundles FastAPI app → single binary
2. Binary placed in src-tauri/binaries/ with platform triple suffix
3. `cargo tauri build` bundles everything into installer
```

### `main.rs` — The Entire Rust File (keep it this small)

```rust
use tauri::Manager;
use std::io::{BufRead, BufReader};

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Spawn Python backend sidecar
            let sidecar = app.shell().sidecar("backend").unwrap();
            let (mut rx, child) = sidecar.spawn().unwrap();
            
            // Read port from sidecar stdout
            // Open webview to http://localhost:{port}
            // Store child handle for cleanup
            
            Ok(())
        })
        .on_window_event(|window, event| {
            // On close: kill sidecar gracefully
        })
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

That's the target. Under 50 lines of meaningful Rust.

## Process Coordination Protocol

```
Sidecar (Python) startup:
1. Finds available port
2. Starts uvicorn
3. Prints to stdout: {"port": 54321, "status": "ready"}
4. Serves requests

Tauri reads stdout:
1. Parses JSON line
2. Extracts port
3. Sets webview URL to http://localhost:{port}

Shutdown:
1. Tauri sends kill signal to sidecar
2. Python catches signal, runs cleanup (close DB, etc.)
3. Process exits
```

## Configuration

```json
{
  "productName": "post-kit",
  "identifier": "com.postkit.app",
  "app": {
    "windows": [{
      "title": "post-kit",
      "width": 1280,
      "height": 800,
      "minWidth": 1024,
      "minHeight": 600
    }],
    "security": {
      "csp": "default-src 'self'; connect-src http://localhost:*; style-src 'self' 'unsafe-inline'; script-src 'self'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "externalBin": ["backend"]
  }
}
```

## Rules

- `main.rs` under 100 lines. If it's longer, you're doing too much in Rust.
- Use `anyhow` for error handling (it's a shell, not a library).
- Log with `log` crate. No `println!` in production.
- CSP: localhost only. No external connections from webview.
- Single instance: prevent multiple app windows.
- Dev mode: point `devUrl` to `http://localhost:8000` (where uvicorn runs directly).
- Prod mode: sidecar is the bundled PyInstaller binary.

## Dev vs Prod

| Concern | Development | Production |
|---------|-------------|-----------|
| Backend | `uvicorn app.backend.main:app --reload` | Bundled sidecar binary |
| Frontend | Served by FastAPI (same as prod) | Same |
| Tauri | `cargo tauri dev` with `devUrl` | `cargo tauri build` |
| Port | Fixed 8000 | Random (sidecar reports via stdout) |

## Anti-Patterns

- ❌ Business logic in Rust
- ❌ Tauri commands for things Python can do
- ❌ Complex Rust error handling (it's a 50-line shell, use `anyhow`)
- ❌ Multiple Rust files/modules (one `main.rs` is enough)
- ❌ Custom Tauri plugins (unless genuinely needed for OS access)
- ❌ External network access from webview
