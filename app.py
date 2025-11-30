from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import os
from extract_text import extract_text
from generate_mcqs import generate_mcqs
from create_html import create_html
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flashing messages

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_EMAIL = "razakhanahmad68@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "razakhanahmad68@gmail.com"  # replace with your Gmail for sending
SMTP_PASSWORD = "ppgd iblk ezxu pfzo"  # replace with your app password


# -------------------- ROUTES --------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields are required.", "error")
            return redirect(url_for("contact"))

        try:
            # Create Email
            msg = MIMEMultipart()
            msg["From"] = email
            msg["To"] = ADMIN_EMAIL
            msg["Subject"] = f"Quiz Agent contact form Message from {name}"
            msg.attach(MIMEText(message, "plain"))

            # Send Email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()

            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            print("Error sending email:", e)
            flash("Failed to send your message. Try again later.", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/generate", methods=["POST"])
def generate():
    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]
    num = int(request.form.get("num_questions", 5))

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    ext = os.path.splitext(file_path)[1].lower()
    ext_map = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".jpg": "image",
        ".jpeg": "image",
        ".png": "image",
        ".txt": "txt",
    }

    if ext not in ext_map:
        return f"Unsupported file format: {ext}"

    file_type = ext_map[ext]

    # Extract text
    text = extract_text(file_path, file_type)

    # Generate MCQs
    mcqs = generate_mcqs(text, num)

    # Create HTML
    create_html(
        mcqs, output_file="templates/quiz.html"
    )  # place in templates for easier rendering

    return render_template("quiz.html")  # render the quiz page in browser


if __name__ == "__main__":
    app.run(debug=True)
