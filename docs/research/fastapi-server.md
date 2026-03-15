# Research: FastAPI Server with UV Inline Dependencies

## Unit Summary

**ID:** `fastapi-server`
**Category:** large
**RFC Sections:** §1

Create a single-file FastAPI server (`api.py`) at the project root using uv's inline script
dependencies (PEP 723). The file must include a `# /// script` metadata block declaring
`fastapi` and `uvicorn` as dependencies so it can be run with `uv run api.py`. Must include
at minimum a health check endpoint (`GET /`) returning a JSON response.

---

## Acceptance Criteria

1. `api.py` exists at the project root with a `# /// script` inline dependency block declaring `fastapi` and `uvicorn`
2. `uv run api.py` starts the server without errors
3. `GET /` returns a `200` JSON response
4. No separate `requirements.txt` or `pyproject.toml` is needed to run the server

---

## Key Implementation Patterns

### PEP 723 Inline Script Metadata Block

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn[standard]",
# ]
# ///
```

- The `# /// script` block **must appear at the top of the file**, before imports
- Each dependency line uses the `#   "package"` format (two-space indent inside TOML)
- `uvicorn[standard]` includes websocket support; plain `uvicorn` also works
- `requires-python` is optional but recommended for clarity

### Minimal FastAPI App

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

- `FastAPI` automatically serializes `dict` return values as JSON (`Content-Type: application/json`)
- `GET /` returning `{"status": "ok"}` satisfies the health check requirement
- The `if __name__ == "__main__"` guard enables both `uv run api.py` and module import

### Running the Server

```bash
uv run api.py
```

UV will:
1. Parse the `# /// script` block
2. Create an ephemeral virtual environment
3. Install `fastapi` and `uvicorn[standard]`
4. Execute `api.py` — which calls `uvicorn.run(app, ...)`

---

## Implementation Checklist

- [ ] `# /// script` block at top of file (before imports)
- [ ] `fastapi` listed as dependency
- [ ] `uvicorn` (or `uvicorn[standard]`) listed as dependency
- [ ] `FastAPI()` app instantiated
- [ ] `GET /` endpoint returning JSON dict
- [ ] `uvicorn.run(app, ...)` in `if __name__ == "__main__"` guard
- [ ] No `requirements.txt` or `pyproject.toml` needed

---

## Open Questions

1. Should the server port be configurable via an environment variable (e.g. `PORT`)? Not specified in the RFC.
2. Should additional endpoints beyond `GET /` be included? RFC says "at minimum" a health check.
3. Should the health check response include additional metadata (version, timestamp)? Not specified.

---

## References

- [PEP 723 – Inline Script Metadata](https://peps.python.org/pep-0723/)
- [uv scripts documentation](https://docs.astral.sh/uv/guides/scripts/)
- [FastAPI quickstart](https://fastapi.tiangolo.com/)
- Work plan: `/Users/msaug/zama/temp-repo-test-claude/.ralphinho/work-plan.json`
