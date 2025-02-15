from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from cs50 import SQL
from helpers import login_required, apology 

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///aniggas.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()  # Clear any existing session

    if request.method == "POST":
        # Get form data
        id = request.form.get("id")
        password = request.form.get("password")

        # Validate inputs
        if not id:
            return apology("must provide id", 403)
        elif not password:
            return apology("must provide password", 403)

        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE id = ?", id)

        # Ensure user exists and password is correct
        if len(rows) != 1 or rows[0]["password"] != password:
            return apology("invalid id and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect to home page
        return redirect("/")

    else:
        # If GET request, render the login page
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/services")
@login_required
def services():
    """Public Service Center"""
    # Fetch user data from the database
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    return render_template("services.html", user=user)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User Profile"""
    if request.method == "POST":
        # Update user data in the database
        name = request.form.get("name")
        password = request.form.get("password")
        surname = request.form.get("surname")
        db.execute("UPDATE users SET name = ?, password = ?, surname = ? WHERE id = ?", name, password, surname, session["user_id"])
        flash("Profile updated successfully!", "success")
        return redirect("/profile")

    else:
        # Fetch user data from the database
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)