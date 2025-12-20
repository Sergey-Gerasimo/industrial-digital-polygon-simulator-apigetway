"""Pytest configuration for smoke tests."""

import sys
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient


# Ensure the application package is importable when tests run from repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
for path in (PROJECT_ROOT, PROJECT_ROOT / "application"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from application.main import app


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    """Shared FastAPI test client for smoke tests."""
    with TestClient(app, base_url="http://testserver") as test_client:
        yield test_client
