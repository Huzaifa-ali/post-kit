"""PostKitBridge — the single boundary between the app and post-kit files."""

from pathlib import Path

import yaml


class PostKitBridge:
    """Reads and writes post-kit file structure. Only class allowed to touch these files."""

    def __init__(self, postkit_root: Path):
        self._root = postkit_root
        self._niche_dir = postkit_root / "my-niche"
        self._engine_dir = postkit_root / "engine"

    @property
    def root(self) -> Path:
        return self._root

    @property
    def niche_dir(self) -> Path:
        return self._niche_dir

    def is_onboarded(self) -> bool:
        """Check if niche.yaml exists (setup complete)."""
        return (self._niche_dir / "niche.yaml").exists()

    def load_niche_config(self) -> dict | None:
        """Load and parse niche.yaml. Returns None if not found."""
        niche_file = self._niche_dir / "niche.yaml"
        if not niche_file.exists():
            return None
        return yaml.safe_load(niche_file.read_text(encoding="utf-8"))

    def get_posts_path(self) -> Path:
        """Resolve the posts output directory from niche config."""
        config = self.load_niche_config()
        if config and "output" in config and "path" in config["output"]:
            return (self._root / config["output"]["path"]).resolve()
        for candidate in [self._root / "posts", self._root.parent / "posts"]:
            if candidate.exists():
                return candidate
        return self._root.parent / "posts"

    def get_active_modules(self) -> list[str]:
        """Get list of active module names from niche.yaml."""
        config = self.load_niche_config()
        if not config:
            return []
        return config.get("modules_active", [])

    def get_platforms(self) -> list[str]:
        """Get configured platforms."""
        config = self.load_niche_config()
        if not config:
            return []
        return config.get("platforms", [])

    def get_content_pillars(self) -> list[dict]:
        """Get content pillars (name + percentage)."""
        config = self.load_niche_config()
        if not config:
            return []
        return config.get("content_pillars", [])

    def get_cadence(self) -> dict | None:
        """Get cadence config (posts_per_day, best_days, etc.)."""
        config = self.load_niche_config()
        if not config:
            return None
        return config.get("cadence", None)

    def list_niche_files(self) -> list[str]:
        """List all files in my-niche/ directory."""
        if not self._niche_dir.exists():
            return []
        return [f.name for f in self._niche_dir.iterdir() if f.is_file()]

    def read_niche_file(self, filename: str) -> str | None:
        """Read a file from my-niche/ by name."""
        filepath = self._niche_dir / filename
        if not filepath.exists():
            return None
        return filepath.read_text(encoding="utf-8")

    def write_niche_file(self, filename: str, content: str) -> None:
        """Write content to a file in my-niche/."""
        self._niche_dir.mkdir(parents=True, exist_ok=True)
        (self._niche_dir / filename).write_text(content, encoding="utf-8")

    def get_version(self) -> str | None:
        """Read VERSION file from post-kit root."""
        version_file = self._root / "VERSION"
        if not version_file.exists():
            return None
        return version_file.read_text(encoding="utf-8").strip()

    def get_niche_version(self) -> str | None:
        """Get postkit_version from niche.yaml."""
        config = self.load_niche_config()
        if not config:
            return None
        return config.get("postkit_version", None)
