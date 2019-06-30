##
# @file app.py
# @author Jim Li
# @date 22 June 2019
#
# Manages the portfolio manager website.


# Imports
import flask as fl
import sqlite3

# Flask App Global Variables
app = fl.Flask(__name__)
hostname = "192.168.0.17"
portNum = 5000
DATABASE_FILE = "PortfolioAccounts.db"

@app.route("/")
##
# Loads the home page.
#
# @return index.html
def load_index():
    global hostname, portNum

    # Check if the user is logged in.
    username = fl.request.cookies.get("username")
    isLoggedIn = fl.request.cookies.get("isLoggedIn")
    if username == None or isLoggedIn != "True":
        return fl.render_template("index.html", hostname=hostname,\
            portNum=portNum, username = "", isLoggedIn = "False")
    else:
        return fl.render_template("index.html", hostname=hostname,\
            portNum=portNum, username = username, isLoggedIn = "True")

@app.route("/login/", methods = ["GET", "POST"])
##
# Handles user login.
#
# @return login.html
def login_handler():
    global DATABASE_FILE
    global hostname, portNum
    resultHTML = "" # what to return

    # The request method should be POST
    if fl.request.method == "POST":
        # Get Login Information entered from the user.
        result = fl.request.form
        loginInfoEntered = dict(result.items())
        username = loginInfoEntered["username"]
        password = loginInfoEntered["password"]

        # Check if this information is in the database.
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
            resultHTML = fl.render_template("index.html",
                hostname=hostname,
                portNum=portNum,
                login_error="Login Incorrect!"
            )
        else:
            resultHTML = fl.render_template("login.html",\
            result = result)

            # Store Login Information in the site's cookie
            resp = fl.make_response(resultHTML)
            resp.set_cookie("username", username)
            resp.set_cookie("isLoggedIn", "True")

            # Close DB, return resp
            conn.close()
            return resp

        conn.close()
        return resultHTML

    # Return an error page, stating that there is something
    # wrong with the login form.
    else:
        return "<b> GET METHOD ERROR </b>"

@app.route("/logout")
##
# Handles logout event. Resets cookies' login information.
#
# @return logout.html
def logout_handler():
    global hostname, portNum
    resp = fl.make_response(fl.render_template("logout.html",\
        logoutSuccess = "True", hostname=hostname,\
        portNum = portNum))
    resp.set_cookie("username", "")
    resp.set_cookie("isLoggedIn", "False")
    return resp


@app.route("/create_account_page/create_account",
    methods = ["GET", "POST"])
##
# Handles account creation.
#
# @return Success or fail HTML file.
def create_account():
    global hostname, portNum
    if fl.request.method.upper() == "POST":
        result = fl.request.form
        loginInfoEntered = dict(result.items())
        username = loginInfoEntered["username"]
        password = loginInfoEntered["password"]
        password_retyped = loginInfoEntered["password_retyped"]

        if password != password_retyped:
            return create_account_page(error_msg=\
            "Password Incorrect")
        elif password == "":
            return create_account_page(error_msg=\
            "Cannot Have Blank Password!")
        else:
            # Check if username already exists.
            conn = sqlite3.connect(DATABASE_FILE)

            sqlQueryUsername = \
            """
            SELECT USERNAME FROM ACCOUNTS
            WHERE USERNAME = '%s';
            """ %(username)

            cursor = conn.execute(sqlQueryUsername)
            usernamesFetched = list(cursor.fetchall())

            cursor.close()


            # Username does not exist in database.
            # create new username.
            if (len(usernamesFetched) == 0):
                conn.execute("""
                INSERT INTO ACCOUNTS VALUES ('%s', '%s');
                """ %(username, password)
                )

                conn.commit()
                conn.close()
                return fl.render_template(
                    "account_successfully_created.html",
                    username=username,
                    hostname=hostname,
                    portNum=portNum
                )

            # Username does exist!
            else:
                conn.commit()
                conn.close()
                return create_account_page(error_msg=\
                "Username: %s already exists!" %(username))

    # That should not happen.
    else:
        return "<b>Account Creation Error: GET METHOD</b>"

@app.route("/create_account_page/")
##
# Displays the account creation page.
#
# @param error_msg Error Message of account creation.
#
# @return create_account_page.html
def create_account_page(error_msg=""):
    return fl.render_template("create_account_page.html",\
    acct_creation_error=error_msg)

# Error Handlers
@app.errorhandler(404)
##
# Handles a 404 error. This happens if the user
# tries to access an invalid URL.
#
# @param error Error Flask object.error
#
# @return A 2-tuple containing a rendered
# error_404.html and the integer 404.
def not_found(error):
    return (fl.render_template("error_404.html"), 404)

##
# Main Function
def main():
    app.run(host=hostname, port=portNum)

# Run the Program
if __name__ == "__main__":
    main()
