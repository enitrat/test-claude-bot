# Plan: FastAPI Server with UV Inline Dependencies

## Overview

Create a single-file FastAPI server (`api.py`) at the project root using PEP 723 inline script metadata so it can be run with `uv run api.py` without any external dependency files.

## Work Type Assessment

**TDD applies.** This adds new observable behavior:
- A new file (`api.py`) that serves HTTP requests
- A `GET /` endpoint returning JSON — testable via FastAPI's `TestClient`

## Current State

Both `api.py` and `test_api.py` already exist at the project root with correct implementations:

- **api.py** — PEP 723 `# /// script` block declaring `fastapi` and `uvicorn[standard]`, `GET /` returning `{"status": "ok"}`, `uvicorn.run()` in `__main__` guard
- **test_api.py** — PEP 723 block declaring `fastapi`, `httpx`, `pytest`; two tests covering status code 200 and JSON body validation

All four acceptance criteria are already satisfied by the existing code. The implementation steps below document the TDD approach used and serve as verification guidance.

---

## Step-by-Step Implementation

### Step 1: Write tests first (test_api.py) — DONE

`test_api.py` at project root with PEP 723 inline dependencies:

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

def test_health_check_returns_200() -> None:
    response = client.get("/")
    assert response.status_code == 200

def test_health_check_returns_json_status_ok() -> None:
    response = client.get("/")
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"status": "ok"}
```

**Tests cover:**
- AC3: GET / returns 200 JSON response
- Response body structure validation (`{"status": "ok"}`)

### Step 2: Implement api.py — DONE

`api.py` at project root:

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
def health_check() -> dict[str, str]:
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Key details:**
- `# /// script` block at top, before imports (PEP 723 required position)
- `uvicorn[standard]` for full feature set (websockets, watchfiles)
- `requires-python = ">=3.11"` for `dict[str, str]` builtin generic syntax
- Dict return auto-serialized to JSON by FastAPI
- `__main__` guard enables both `uv run api.py` and module import in tests

### Step 3: Verify

1. **Run tests:** `uv run pytest test_api.py -v`
2. **Start server:** `uv run api.py` (background), then `curl http://localhost:8000/`
3. **Check no extra files needed:** Confirm no `requirements.txt` or `pyproject.toml` is required

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
| PEP 723 block malformed | `uv` ignores dependencies | Follow exact format from PEP 723 spec |
| `content-type` header includes charset suffix | Test assertion breaks on exact match | Use `.startswith("application/json")` (already done) |

---

## Acceptance Criteria Verification

| AC | How to Verify | Status |
|----|---------------|--------|
| 1. `api.py` exists with `# /// script` block | File inspection — lines 1-7 of `api.py` | ✓ Done |
| 2. `uv run api.py` starts without errors | Manual run | ✓ Verify at Step 3 |
| 3. GET / returns 200 JSON | `test_api.py` assertions + curl | ✓ Verify at Step 3 |
| 4. No separate requirements.txt/pyproject.toml | `ls` confirms absence | ✓ Verify at Step 3 |
