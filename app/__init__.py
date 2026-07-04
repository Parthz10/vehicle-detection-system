from pathlib import Path

# Expose backend/app as the top-level `app` package so existing imports work
# both locally and in Vercel's build environment.
__path__ = [str(Path(__file__).resolve().parent.parent / "backend" / "app")]
