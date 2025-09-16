from __future__ import annotations
from pathlib import Path
from typing import Optional

__all__ = ["detect_language", "is_probably_text"]

# Mapping of extensions to canonical language identifiers used across the system
_EXT_MAP = {
    # Python
    ".py": "python",
    ".pyi": "python-stub",
    # JavaScript / TypeScript
    ".js": "javascript",
    ".jsx": "javascript-react",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript-react",
    # Other common backend
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".kt": "kotlin",
    ".scala": "scala",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "csharp",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "cpp-header",
    ".hpp": "cpp-header",
    ".hh": "cpp-header",
    ".hxx": "cpp-header",
    # Config / scripts
    ".sh": "bash",
    ".ps1": "powershell",
    ".bash": "bash",
    ".zsh": "bash",
    ".fish": "fish",
    # Markup / docs
    ".md": "markdown",
    ".rst": "restructuredtext",
    ".adoc": "asciidoc",
    ".txt": "text",
    # Data / schema
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".toml": "toml",
    ".ini": "ini",
    ".cfg": "ini",
    ".env": "dotenv",
}

# Shebang hints
_SHEBANG_HINTS = {
    "python": "python",
    "python3": "python",
    "node": "javascript",
    "bash": "bash",
    "sh": "bash",
    "zsh": "bash",
    "fish": "fish",
}

_BINARY_SNIFF_BYTES = 4096

_TEXT_CHAR_RATIO_THRESHOLD = 0.90

def is_probably_text(path: Path) -> bool:
    """Heuristic binary detection by proportion of printable chars in first chunk."""
    try:
        raw = path.read_bytes()[:_BINARY_SNIFF_BYTES]
    except Exception:
        return False
    if not raw:
        return True
    printable = sum(32 <= b < 127 or b in (9, 10, 13) for b in raw)
    ratio = printable / len(raw)
    return ratio >= _TEXT_CHAR_RATIO_THRESHOLD

def _shebang_language(first_line: str) -> Optional[str]:
    if not first_line.startswith("#!"):
        return None
    # Extract last token (e.g. /usr/bin/env python3)
    parts = first_line[2:].strip().split()
    if not parts:
        return None
    last = parts[-1].split('/')[-1]
    return _SHEBANG_HINTS.get(last)

def detect_language(path: Path, content_first_1k: Optional[str] = None) -> Optional[str]:
    ext = path.suffix.lower()
    if ext in _EXT_MAP:
        return _EXT_MAP[ext]
    # Shebang fallback (scripts without extension)
    if content_first_1k is None:
        try:
            content_first_1k = path.read_text(encoding="utf-8", errors="ignore")[:1000]
        except Exception:
            content_first_1k = ""
    first_line = content_first_1k.splitlines()[0] if content_first_1k else ""
    she = _shebang_language(first_line)
    if she:
        return she
    return None
