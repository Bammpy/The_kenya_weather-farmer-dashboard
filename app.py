from dotenv import load_dotenv
load_dotenv()

import os

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bammpy_super_secret_key_2025')  # Use env for production if available

# === EMAIL CONFIGURATION (Brevo SMTP) ===
app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Use env vars for credentials (secure & correct)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')          # Your Brevo SMTP login email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')          # Your Brevo SMTP key

# Sender: (display name, actual email) - use your new business email
# Make sure this email is verified in Brevo (Senders & IP → Senders → Add/verify)
app.config['MAIL_DEFAULT_SENDER'] = ("Bammpy ByteBeam Forge", os.environ.get('MAIL_SENDER', 'whatbethebusiness@gmail.com'))

mail = Mail(app)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/fiber-tech')
def fiber_tech():
    return render_template('fiber_tech.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        service = request.form.get('service', 'other')
        message = request.form.get('message', '').strip()

        # Make service name look nice in email
        service_display = {
            'software': 'Software Development',
            'ml': 'Machine Learning / Data',
            'fiber': 'Fiber & Networking',
            'project': 'Buy a Project',
            'other': 'Other'
        }.get(service, service.capitalize())

        msg = Message(
            subject=f"New Inquiry: {service_display} from {name}",
            recipients=['whatbethebusiness@gmail.com'],
            reply_to=email,
            body=f"""
New message from Bammpy ByteBeam Forge!

Name: {name}
Email: {email}
Service: {service_display}

Message:
{message}

---
Sent from your portfolio site
            """.strip()
        )

        try:
            mail.send(msg)
            flash(f"Thanks {name}! Your message was sent successfully. I'll reply soon 🚀", "success")
        except Exception as e:
            print(f"Mail send failed: {e}")
            flash("Sorry, something went wrong. Please email me directly at whatbethebusiness@gmail.com or try again later.", "danger")

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)