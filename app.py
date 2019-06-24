"""
Author: Jim Li
Date: 22 June 2019

Manages the portfolio manager website.
"""

# Imports
from flask import Flask, render_template, request
import sqlite3

# Flask App Global Variables
app = Flask(__name__)
hostname = "192.168.0.17"
portNum = 5000

##
# Loads the home page.
@app.route("/")
def load_index():
    global hostname, portNum
    return render_template("index.html", hostname=hostname,\
        portNum=portNum)

##
# Handle user login
@app.route("/login/", methods = ["GET", "POST"])
def login_handler():
    resultHTML = "" # what to return

    # The request method should be POST
    if request.method == "POST":
        # Get Login Information entered from the user.
        result = request.form
        print(type(result.items()))
        loginInfoEntered = dict(result.items())
        username = loginInfoEntered["username"]
        password = loginInfoEntered["password"]

        # Check if this information is in the database.
        DATABASE_FILE = "PortfolioAccounts.db"
        conn = sqlite3.connect(DATABASE_FILE)

        # TODO: This is a really unsafe way to store/access
        # passwords on a database. The best practice is
        # to hash a salted password.
        sqlCheckLoginInfomation = """
        SELECT USERNAME, PASSWORD FROM ACCOUNTS
        WHERE USERNAME = '%s' AND PASSWORD = '%s';
        """ %(username, password)

        cursor = conn.execute(sqlCheckLoginInfomation)
        if len(cursor.fetchall()) <= 0:
            resultHTML = "<h1>LOGIN INCORRECT</h1>"
        else:
            resultHTML = render_template("login.html", result = result)
        conn.close()

        return resultHTML

    # Return an error page, stating that there is something
    # wrong with the login form.
    else:
        return "<b> GET METHOD ERROR </b>"

# Main Program Area
if __name__ == "__main__":
    app.run(host=hostname, port=portNum)
