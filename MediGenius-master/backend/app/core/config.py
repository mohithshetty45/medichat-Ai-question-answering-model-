"""
MEDICHAT AI — core/config.py
Environment variables and path constants.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────────
# backend/app/core/config.py -> backend/
_BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Ensure logs and storage are inside backend directory
LOG_DIR = os.getenv("LOG_DIR", os.path.join(_BACKEND_DIR, "logs"))
CHAT_DB_PATH = os.getenv("CHAT_DB_PATH", os.path.join(_BACKEND_DIR, "storage", "chat_db", "medichat_ai.db"))
VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", os.path.join(_BACKEND_DIR, "storage", "vector_store"))
PDF_PATH = os.getenv("PDF_PATH", os.path.join(_BACKEND_DIR, "data", "medical_book.pdf"))

# ── API Keys ───────────────────────────────────────────────────────────────────
def _read_secret(name: str) -> str | None:
    """Return a configured secret, ignoring the placeholders from .env.example."""
    value = os.getenv(name, "").strip()
    if not value or value.lower() in {
        "replace_with_your_groq_api_key",
        "your_groq_api_key",
        "your_key_here",
    }:
        return None
    return value


GROQ_API_KEY = _read_secret("GROQ_API_KEY")
TAVILY_API_KEY = _read_secret("TAVILY_API_KEY")

# ── Rate Limiting ──────────────────────────────────────────────────────────────
# protects Groq/Tavily quota and avoids tripping DuckDuckGo's IP-block threshold
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "1") == "1"
RATE_LIMIT = os.getenv("RATE_LIMIT", "20/minute")

# ── Memory ─────────────────────────────────────────────────────────────────────
# caps how many recalled exchanges get injected into a prompt — unbounded recall quietly inflates every prompt
MAX_RECALLED_MEMORIES = int(os.getenv("MAX_RECALLED_MEMORIES", "3"))

# ── Model Gateway ──────────────────────────────────────────────────────────────
# Using currently available valid Groq models.
SYNTHESIS_MODEL = os.getenv("SYNTHESIS_MODEL", "groq/openai/gpt-oss-120b")
REASONING_MODEL = os.getenv("REASONING_MODEL", "groq/openai/gpt-oss-120b")
CLASSIFICATION_MODEL = os.getenv("CLASSIFICATION_MODEL", "groq/openai/gpt-oss-20b")
