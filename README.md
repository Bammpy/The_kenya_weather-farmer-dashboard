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
