set -e
cat > 'pyproject.toml' <<'FIXTURE_EOF'
[project]
name = "slugkit"
version = "1.2.0"
description = "Turn titles into URL slugs"
requires-python = ">=3.10"
license = "Apache-2.0"
dependencies = []

[dependency-groups]
dev = ["pytest>=8"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
FIXTURE_EOF
cat > 'uv.lock' <<'FIXTURE_EOF'
version = 1
requires-python = ">=3.10"
FIXTURE_EOF
cat > 'LICENSE' <<'FIXTURE_EOF'
Apache License
Version 2.0, January 2004
FIXTURE_EOF
mkdir -p 'src/slugkit'
cat > 'src/slugkit/__init__.py' <<'FIXTURE_EOF'
"""Turn titles into URL slugs."""
import re
import unicodedata

__all__ = ["slugify"]


def slugify(text: str, sep: str = "-", max_length: int | None = None) -> str:
    """Lowercase, strip accents, and join words with sep. Truncates at a word boundary when max_length is set."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", ascii_text.lower())
    slug = sep.join(words)
    if max_length is not None and len(slug) > max_length:
        cut = slug[:max_length]
        slug = cut.rsplit(sep, 1)[0] if sep in cut else cut
    return slug
FIXTURE_EOF
mkdir -p 'tests'
cat > 'tests/test_slugify.py' <<'FIXTURE_EOF'
from slugkit import slugify


def test_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_accents():
    assert slugify("Crème brûlée") == "creme-brulee"


def test_max_length():
    assert slugify("one two three", max_length=8) == "one-two"
FIXTURE_EOF
mkdir -p '.github/workflows'
cat > '.github/workflows/ci.yml' <<'FIXTURE_EOF'
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv run --python ${{ matrix.python }} pytest
FIXTURE_EOF
