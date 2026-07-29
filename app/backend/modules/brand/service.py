"""Brand service — niche file listing and editing via bridge."""

from backend.core.bridge import PostKitBridge


def list_niche_files(bridge: PostKitBridge) -> list[dict]:
    """List all files in my-niche/ with summary info."""
    files = bridge.list_niche_files()
    result = []
    for filename in sorted(files):
        content = bridge.read_niche_file(filename)
        first_line = ""
        if content:
            for line in content.split("\n"):
                stripped = line.strip().lstrip("#").strip()
                if stripped:
                    first_line = stripped[:80]
                    break
        result.append({
            "filename": filename,
            "summary": first_line,
            "size": len(content) if content else 0,
        })
    return result


def get_file_content(bridge: PostKitBridge, filename: str) -> str | None:
    """Get the content of a niche file."""
    return bridge.read_niche_file(filename)


def save_file_content(bridge: PostKitBridge, filename: str, content: str) -> None:
    """Save edited content to a niche file."""
    bridge.write_niche_file(filename, content)
