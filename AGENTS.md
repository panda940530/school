# Repository Guidelines

## Project Structure & Module Organization
- `school.py` is the Flask entrypoint exposing `/` for uploads and `/download_csv` for exports; it forwards queries to the n8n webhook and formats table/chart data.
- `templates/` holds the UI: `school_upload.html` (input form) and `school_result.html` (results table + chart and CSV download).
- `docker-compose.yml` defines the `school-backend` service (built from `Dockerfile`) and the companion `n8n` service; shared settings live in environment variables.
- `requirements.txt` lists Python runtime deps (Flask, requests). Add new deps here and rebuild images.

## Setup, Build, and Run
- Local venv: `python -m venv .venv && .\.venv\Scripts\activate` (Windows) then `pip install -r requirements.txt`.
- Dev server: `python school.py` (binds to `0.0.0.0:5000`). Set `N8N_BASE` to point at your n8n host; switch `USE_TEST` to `0` when targeting the production webhook path.
- Docker: `docker compose up --build` builds the backend image and brings up both services; reach the UI at `http://127.0.0.1:5000` and n8n at `http://127.0.0.1:5679`.
- Template changes: use `flask --app school run --debug` for auto-reload while editing HTML/CSS.

## Coding Style & Naming Conventions
- Python 3.11, follow PEP 8 with 4-space indents and snake_case for functions/variables; keep module-level constants uppercase.
- Prefer small helpers for formatting/validation (see the percent/money formatters in `school.py`); keep request handlers thin.
- HTML/CSS: keep inline styles consistent with existing palette; name form fields descriptively to match n8n payload keys.

## Testing Guidelines
- No automated tests yet; add `pytest` with files named `tests/test_*.py`. Target helpers that transform percentages, money, and table columns.
- Manual smoke: run the server, submit sample queries, verify n8n responses render rows, confirm chart spec passes through, and download CSV to ensure column order matches `col_map`.

## Commit & Pull Request Guidelines
- Git history is sparse; use clear, imperative messages (e.g., `Add CSV download route`, `Harden n8n request handling`).
- PRs should include: summary of behavior change, linked issue (if any), screenshots of the upload/result pages for UI tweaks, manual test notes, and any env var/config changes (e.g., `N8N_BASE`, webhook paths).

## Security & Configuration Tips
- Do not hardcode secrets or production endpoints; inject via env vars and `docker-compose.yml`.
- Keep request timeouts reasonable (`requests.post` already uses 90s); validate user input length before forwarding to n8n if expanding functionality.
- When switching environments, confirm `USE_TEST` flag and `PATH` match the intended webhook (`/webhook-test/school` vs `/webhook/school`).
