"""
Author: Jim Li
Date: 22 June 2019

Manages the portfolio manager website.
"""
from flask import Flask, render_template, request
app = Flask(__name__)

# Load the home page.
@app.route("/")
def load_index():
    return render_template("index.html")

# Handle user login
@app.route("/login/", methods = ["GET", "POST"])
def login_handler():
    if request.method == "POST":
        result = request.form
        return render_template("login.html", result = result)
    else:
        return "<b> GET METHOD ERROR </b>"
# Main Program Area
if __name__ == "__main__":
    app.run()
