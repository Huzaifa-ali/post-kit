"""Run the post-kit web UI."""

import uvicorn


def main():
    uvicorn.run(
        "web.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_excludes=[".venv"],
    )


if __name__ == "__main__":
    main()
