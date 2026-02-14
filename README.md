# Test API Project

Simple API with a bug for testing Claude bot.

## Bug Description

The API endpoint `/` is supposed to return `{"message": "hello_world"}` but instead returns `{"message": "THIS IS A BUG"}`.

## Running the API

```bash
# Make executable
chmod +x api.py

# Run with uv (will auto-install dependencies)
./api.py

# Or explicitly with uv
uv run api.py
```

## Testing

```bash
curl http://localhost:8000/
# Expected: {"message": "hello_world"}
# Actual: {"message": "THIS IS A BUG"}
```
