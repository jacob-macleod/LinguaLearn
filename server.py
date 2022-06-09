# Handles the code for the server
from flask import Flask, render_template, request, redirect, url_for, flash, make_response

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    # Store the contents of the loggedIn cookie to loggenID - if the cookie has not been made the value will = null, otherwise it will = False or True
    loggedIn = request.cookies.get("loggedIn")

    # If the user clicks the login button on signIn.html
    if request.method == "POST":
        username = request.form.get("usernameInput")
        # TODO! Add encryption for the password!
        password = request.form.get("passwordInput")
        

    if (loggedIn == "True") :
        # Load the dashboard.html page
        # Below text is temporary
        print("hello world")
    else:
        return render_template("signIn.html")

@app.route("/signup")
def signUp () :
    return render_template("signUp.html")

app.run(debug=True, host='0.0.0.0')