# 🌾 Kenya Weather Farmer Dashboard

A responsive Flask application built to demonstrate Weather-AI API integration for Kenyan farmers.

This project consumes Weather-AI's developer API to deliver:
- current weather conditions
- 7-day forecast
- AI-powered farming advisory
- Kenyan city support with default Nairobi fallback

## 🚀 Key Features

- **Weather-AI API integration** for live forecast and AI insights
- **Clean UI** with responsive dashboard design
- **Search Kenyan cities** like Nairobi, Kisumu, Eldoret, Nakuru, Mombasa, and more
- **Deployment-ready** configuration for Render, Railway, or similar platforms

## 🧰 Tech Stack

- Python 3.13
- Flask
- Tailwind CSS
- Requests
- Python Dotenv

## 📦 Requirements

- `requirements.txt`
- `gunicorn` for production deployment

## 🔧 Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/The_kenya_weather-farmer-dashboard.git
   cd The_kenya_weather-farmer-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following values:
   ```env
   API_KEY=wai_your_weather_ai_key_here
   ```

5. Run the app locally:
   ```bash
   python app.py
   ```

6. Open the app in your browser:
   ```text
   http://127.0.0.1:5000
   ```

## 🌐 Deployment

This project is ready for deployment on platforms such as Render or Railway.

### Render deployment

1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. Add the environment variable:
   - `API_KEY` = `wai_your_weather_ai_key_here`
4. Set the start command with `Procfile` support, or use:
   ```text
   gunicorn app:app
   ```

### Railway deployment

1. Connect the repository in Railway.
2. Set `API_KEY` in the environment variables.
3. Use `gunicorn app:app` as the start command.

## 📝 Notes

- Do not commit your `.env` file to the repository.
- The default city is Nairobi when an unknown city is entered.
- The app uses environment variables for secure API key management.

## 📌 Project Structure

- `app.py` — Flask backend and Weather-AI API integration
- `templates/` — HTML templates for the dashboard
- `static/css/style.css` — custom styles
- `requirements.txt` — Python dependencies
- `Procfile` — deployment entrypoint
- `.gitignore` — local ignore rules

## 💡 Next steps for submission

- Publish the repository publicly on GitHub.
- Deploy the app and confirm the live URL works.
- Reply to the hiring email with:
  1. GitHub repository link
  2. Live deployment URL
