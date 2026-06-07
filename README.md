# Bammpy ByteBeam Forge

A Flask portfolio website for showcasing services and accepting client inquiries.

## Files Included

- `app.py` — Flask application
- `templates/` — HTML templates
- `static/` — CSS, JavaScript, images
- `requirements.txt` — Python dependencies
- `Procfile` — Render deployment command
- `.env.example` — example environment variables
- `.gitignore` — files to ignore in Git

## Local Setup

1. Create a virtual environment:
   ```powershell
   python -m venv bbbf
   .\bbbf\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your credentials.

4. Run locally:
   ```powershell
   python app.py
   ```

## Deploying to Render

1. Push this project to a GitHub repository.
2. Create a new Web Service on Render.
3. Select "Connect a repository" and choose your GitHub repo.
4. For the build command, use:
   ```bash
   pip install -r requirements.txt
   ```
5. For the start command, use:
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```
6. Add environment variables in Render:
   - `SECRET_KEY`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
   - `MAIL_SENDER`

## Notes

- Keep `.env` secret and do not commit it.
- The app is public on Render by default, which is appropriate for a portfolio site.
- You can optionally add a custom domain through Render later.

## Deployment (Production)

Recommended production checklist and commands for hosting (Render, Heroku, or similar):

- Ensure required environment variables are set in your hosting platform:
   - `SECRET_KEY` — strong random secret for session signing
   - `MAIL_USERNAME` — Brevo SMTP login/email
   - `MAIL_PASSWORD` — Brevo SMTP password or API key
   - `MAIL_SENDER` — verified sender email (e.g. noreply@yourdomain.com)
   - Optional: `DEBUG` — set to `False` (or unset) in production

- Include `runtime.txt` to pin Python version (already included: `python-3.13.0`).

- Health check endpoint:
   - The app exposes `/health` which returns `{ "status": "ok" }` for load balancers.

- Start command (example for Render or Heroku):
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```

- Build/install dependencies (CI or build step):
   ```bash
   pip install -r requirements.txt
   ```

- Local production testing (bind to all interfaces):
   ```bash
   # set env vars in PowerShell example
   $env:SECRET_KEY = 'your_secret'; $env:MAIL_USERNAME = 'you@example.com'; $env:MAIL_PASSWORD = 'pwd';
   python app.py
   ```

- Logging & error handling:
   - The app configures basic logging and writes exceptions to the app logger. For advanced logging, connect to a stdout collector or logging service.

- Recommended security hardening (future):
   - Add CSRF protection (Flask-WTF or similar)
   - Add rate limiting for contact form to prevent abuse
   - Serve static assets via CDN or object storage for performance

If you want, I can add a `Procfile` example for other platforms or add automated deploy steps (GitHub Actions).

## GitHub Actions (optional CI & Deploy)

You can add CI and an automated Render deploy using GitHub Actions. Two example workflows are included in `.github/workflows/`:

- `ci.yml` — Installs dependencies, runs a syntax check, and performs a basic `/health` smoke test by importing the app.
- `deploy-render.yml` — Triggers a Render deploy by calling the Render API. It runs on push to `main`.

To enable the deploy workflow, add two repository secrets in GitHub:

- `RENDER_API_KEY` — A Render service API key (create in Render dashboard → Account → API Keys).
- `RENDER_SERVICE_ID` — The Render service id for your Web Service (e.g. `srv-xxxxx`).

Once those secrets are set, pushes to `main` will trigger the `Deploy to Render` workflow.
