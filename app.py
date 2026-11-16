from flask import Flask, render_template, request
from database import initialize_database, get_db_connection
from werkzeug.security import generate_password_hash
import sqlite3

# Create the Flask application
app = Flask(__name__)
#Initialize the CampusCare Connect Database
initialize_database()

# Display homepage
@app.route("/")
def home():
    return render_template("index.html")
# Wellness Resources page
@app.route("/resources")
def resources():
    return render_template("resources.html")
# Self-Care page
@app.route("/self-care")
def self_care():
    return render_template("self_care.html")
# Student Login page
@app.route("/login")
def login():
    return render_template("login.html")
# Student Registration page
# Student Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Get information from the registration form
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check that passwords match
        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        # Check password length
        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters."
            )

        # Hash the password
        password_hash = generate_password_hash(password)

        # Save student information
        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO students (full_name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (full_name, email, password_hash)
            )

            connection.commit()
            message = "Your account was created successfully!"

        except sqlite3.IntegrityError:
            message = "An account with this email already exists."

        finally:
            connection.close()

        return render_template("register.html", message=message)

    return render_template("register.html")

# Run the application
if __name__ == "__main__":
    app.run(debug=True)