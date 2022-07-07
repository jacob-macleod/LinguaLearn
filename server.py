# Handles the code for the server
from cgitb import reset
from importlib import reload
from telnetlib import theNULL
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from databaseMethods import searchUsers, addUserToDatabase, createChatroom, findChatroomsJoined, searchChatrooms, addUserToChatroom, uploadMessage, readChatroomMessages, increaseStreak, resetStreak, findStreak, checkIfWeeklyXPNeedsReset
import datetime
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

        # If username and password are found in the file
        if (searchUsers(username, 1) != "False") and (searchUsers(password, 2) != "False") :
            # Setup the redirect page
            xp = searchUsers(username, 1)[3]
            dashboardTemplate = make_response(render_template("dashboard.html", chatrooms=findChatroomsJoined(username), xp=xp, streak=findStreak(username)))
            
            # Check if the cookie storing the last time the weekly xp count was updated needs to be reset. If so, reset it and set the weekly xp count to 0
            # Find the date of the last reset
            year = request.cookies.get("lastResetYear")
            month = request.cookies.get("lastResetMonth")
            day = request.cookies.get("lastResetDay")
            
            # If the cookies have already been set
            try :
                lastReset = datetime.datetime(int(year), int(month), int(day))
            except :
                # If the cookies have not been set yet
                lastReset = datetime.datetime.now()

                # Update the cookies to show the data from today
                dashboardTemplate.set_cookie("lastResetYear", datetime.datetime.now().strftime("%Y"))
                dashboardTemplate.set_cookie("lastResetMonth", datetime.datetime.now().strftime("%m"))
                dashboardTemplate.set_cookie("lastResetDay", datetime.datetime.now().strftime("%d"))

                # Store the data of the last reset
                year = datetime.datetime.now().strftime("%Y")
                month = datetime.datetime.now().strftime("%m")
                day = datetime.datetime.now().strftime("%d")
            
            reset = checkIfWeeklyXPNeedsReset(year, month, day, username)
            # If the weekl xp has been reset
            if (reset == True) :
                # Update the relevant cookies accordingly
                dashboardTemplate.set_cookie("lastResetYear", datetime.datetime.now().strftime("%Y"))
                dashboardTemplate.set_cookie("lastResetMonth", datetime.datetime.now().strftime("%m"))
                dashboardTemplate.set_cookie("lastResetDay", datetime.datetime.now().strftime("%d"))

            # Take the user to the dashboard page and set the username cookie
            dashboardTemplate.set_cookie('username', username)
            return dashboardTemplate
        else :
            # If the username or password are not found
            return render_template("signInFail.html")
        

    if (loggedIn == "True") :
        # Load the dashboard.html page
        username = request.cookies.get("username")
            
        # Setup the redirect page
        xp = searchUsers(username, 1)[3]
        dashboardTemplate = make_response(render_template("dashboard.html", chatrooms=findChatroomsJoined(username), xp=xp, streak=findStreak(username)))
            
        # Check if the cookie storing the last time the weekly xp count was updated needs to be reset. If so, reset it and set the weekly xp count to 0
        # Find the date of the last reset
        year = request.cookies.get("lastResetYear")
        month = request.cookies.get("lastResetMonth")
        day = request.cookies.get("lastResetDay")
            
        # If the cookies have already been set
        try :
            lastReset = datetime.datetime(int(year), int(month), int(day))
        except :
            # If the cookies have not been set yet
            lastReset = datetime.datetime.now()

            # Update the cookies to show the data from today
            dashboardTemplate.set_cookie("lastResetYear", datetime.datetime.now().strftime("%Y"))
            dashboardTemplate.set_cookie("lastResetMonth", datetime.datetime.now().strftime("%m"))
            dashboardTemplate.set_cookie("lastResetDay", datetime.datetime.now().strftime("%d"))

            # Store the data of the last reset
            year = datetime.datetime.now().strftime("%Y")
            month = datetime.datetime.now().strftime("%m")
            day = datetime.datetime.now().strftime("%d")
                
        reset = checkIfWeeklyXPNeedsReset(year, month, day, username)
        # If the weekl xp has been reset
        if (reset == True) :
            # Update the relevant cookies accordingly
            dashboardTemplate.set_cookie("lastResetYear", datetime.datetime.now().strftime("%Y"))
            dashboardTemplate.set_cookie("lastResetMonth", datetime.datetime.now().strftime("%m"))
            dashboardTemplate.set_cookie("lastResetDay", datetime.datetime.now().strftime("%d"))

        # Take the user to the dashboard page and set the username cookie
        dashboardTemplate.set_cookie('username', username)
        return dashboardTemplate
    else:
        return render_template("signIn.html")

@app.route("/signup", methods=["GET", "POST"])
def signUp () :

    # If the user presses the create an account button:
    if request.method == "POST" :
        username = request.form.get("usernameInput")
        password = request.form.get("passwordInput")

        addUserToDatabase(username, password)
        # Take the user to the dashboard page and set the username cookie
        dashboardTemplate = make_response(render_template("dashboard.html", chatrooms=findChatroomsJoined(username)))
        dashboardTemplate.set_cookie('username', username)
        return dashboardTemplate

    return render_template("signUp.html")

# When the user clicks the button on the dahsboard to create a chatroom
@app.route("/createChatroom", methods=["POST", "GET"])
def createChatroomPage () :

    # When the user clicks the create a chatroom button
    if (request.method == "POST") :
        language = request.form.get("languageInput")
        name = request.form.get("nameInput")

        # Find the value of the username cookie
        username = request.cookies.get("username")

        # Add the chatroom to chatrooms.csv and add the user to users.csv
        createChatroom(name, language, username)

    return render_template("createChatroom.html")

@app.route("/joinChatroom", methods=["GET", "POST"])
def joinChatroom() :
    # Get a list of all the chatrooms
    chatrooms = searchChatrooms()

    # If the joinChatroom button is clicked
    if (request.method == "POST") :
        chatroomName = request.form.get("chatroomOptions")

        # Add the user to the chatroom
        addUserToChatroom(request.cookies.get("username"), chatroomName)

        #Take the user to the main page
        return redirect("/")
    return render_template("joinChatroom.html", chatrooms=chatrooms)

@app.route("/chatroom", methods=["GET", "POST"])
def chatroom() :
    chatroomName = request.cookies.get("chatroomName")

    # If a post is submitted
    if (request.method == "POST") :
        xp = searchUsers(request.cookies.get("username"), 1)[3]
        reloadPage = make_response(render_template("chatroom.html", chatroomName=chatroomName, messages=readChatroomMessages(chatroomName), xp=xp))

        # Find the date of the last streak
        year = request.cookies.get("year")
        month = request.cookies.get("month")
        day = request.cookies.get("day")
        
        # If the cookies have been set
        try :
            lastStreak = datetime.datetime(int(year), int(month), int(day))
        except :
            # If the cookies have not been set
            lastStreak = datetime.datetime.now()

            # Update the streak by one day
            # Update the cookies to reflect the data for today
            reloadPage.set_cookie("year", datetime.datetime.now().strftime("%Y"))
            reloadPage.set_cookie("month", datetime.datetime.now().strftime("%m"))
            reloadPage.set_cookie("day", datetime.datetime.now().strftime("%d"))
            
            # Actually increase the streak
            increaseStreak(request.cookies.get("username"))


        # Get the current date
        date = datetime.datetime.now()
        # Find how long ago the last streak was
        delta = date - lastStreak

        # If the streak was last updated 1 day ago
        if (delta.days == 1) :
            # Update the cookies to reflect the data for today
            reloadPage.set_cookie("year", datetime.datetime.now().strftime("%Y"))
            reloadPage.set_cookie("month", datetime.datetime.now().strftime("%m"))
            reloadPage.set_cookie("day", datetime.datetime.now().strftime("%d"))
            
            # Increase the streak
            increaseStreak(request.cookies.get("username"))
        elif (delta.days > 1) :
            # If the streak was updated more than one day ago
            # Update the cookies to reflect the data for today
            reloadPage.set_cookie("year", datetime.datetime.now().strftime("%Y"))
            reloadPage.set_cookie("month", datetime.datetime.now().strftime("%m"))
            reloadPage.set_cookie("day", datetime.datetime.now().strftime("%d"))
            resetStreak(request.cookies.get("username"))
            
            increaseStreak(request.cookies.get("username"))
        else:
            # If the streak was done today do nothing
            pass

        uploadMessage(request.form.get("message"), chatroomName, request.cookies.get("username"))
        # Reload the page so the sent message can be seen
        # Also clear the message cookie
        reloadPage.set_cookie("message", "")
        return reloadPage
    
    xp = searchUsers(request.cookies.get("username"), 1)[3]
    return render_template("chatroom.html", chatroomName=chatroomName, messages=readChatroomMessages(chatroomName), xp=xp)
    
app.run(debug=True, host='0.0.0.0')