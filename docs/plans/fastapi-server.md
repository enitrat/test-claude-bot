# Plan: FastAPI Server with UV Inline Dependencies

## Overview

Create a single-file FastAPI server (`api.py`) at the project root using PEP 723 inline script metadata so it can be run with `uv run api.py` without any external dependency files.

## Work Type Assessment

**TDD applies.** This adds new observable behavior:
- A new file (`api.py`) that serves HTTP requests
- A `GET /` endpoint returning JSON — testable via FastAPI's `TestClient`

## Approach

1. Write a test that validates the API contract (GET / returns 200 + JSON with status)
2. Implement `api.py` with PEP 723 metadata block and health endpoint
3. Verify with `uv run api.py` and manual curl, plus automated test

---

## Step-by-Step Implementation

### Step 1: Write test (test_api.py)

Create `test_api.py` at project root using FastAPI's `TestClient`:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "httpx",
#   "pytest",
# ]
# ///
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_check_returns_200():
    response = client.get("/")
    assert response.status_code == 200

def test_health_check_returns_json():
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
```

**Tests cover:**
- AC3: GET / returns 200 JSON response
- Response body structure validation

### Step 2: Implement api.py

Create `api.py` at project root:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn[standard]",
# ]
# ///
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Key details:**
- `# /// script` block at top, before imports (required by PEP 723)
- `uvicorn[standard]` for full feature set
- `requires-python = ">=3.11"` for clarity
- Dict return auto-serialized to JSON by FastAPI
- `__main__` guard for `uv run api.py` execution

### Step 3: Verify

1. **Run tests:** `uv run pytest test_api.py -v`
2. **Start server:** `uv run api.py` (background), then `curl http://localhost:8000/`
3. **Check no extra files needed:** Confirm no `requirements.txt` or `pyproject.toml` exists

---

## Files

### To Create
| File | Purpose |
|------|---------|
| `api.py` | FastAPI server with PEP 723 inline dependencies |
| `test_api.py` | Tests for health check endpoint |

### To Modify
None.

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `uv` not installed on target machine | Server won't start | Document `uv` as prerequisite; it's already used in this project |
| Port 8000 already in use | Server fails to bind | Use a configurable port or document the default |
| PEP 723 block malformed | `uv` ignores dependencies | Follow exact format from PEP 723 spec; validate with `uv run --dry-run` if available |

---

## Acceptance Criteria Verification

| AC | Verification |
|----|-------------|
| 1. `api.py` exists with `# /// script` block | File inspection |
| 2. `uv run api.py` starts without errors | Manual run + test |
| 3. GET / returns 200 JSON | `test_api.py` assertions + curl |
| 4. No separate requirements.txt/pyproject.toml | `ls` confirms absence |
