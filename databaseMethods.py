# Handles methods for the database
import csv
from re import search
import uuid
from statisticMethods import calculateXP, sortUsersOnLeaderBoard
import datetime


# Add a user to the database
def addUserToDatabase(username, password) :
    # Generate a uniue user ID
    userID = uuid.uuid4()

    with open("database/users.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow([userID, username, password])
        csvfile.close()


# Find a user by their username(1st position in csv file starting from 0) or password (2nd position in csv file)
def searchUsers(searchTerm, collumn) :
    matchFound = False

    # For every line in users.csv
    with open("database/users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            # If the collumn(th) position of the array line = searchTerm (If search term found)
            if (len(line) != 0) :
                if (line[collumn] == searchTerm) :
                    matchFound = True
                    csvfile.close()
                    # Return the line found
                    return line

    # If no match found
    if (matchFound == False) :
        csvfile.close()
        return "False"


# Find a chatroom detail by the chatroomName
def locateChatroomCollumn(searchTerm, collumn) :
    matchFound = False

    # For every line in users.csv
    with open("database/chatrooms.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            # If the collumn(th) position of the array line = searchTerm (If search term found)
            if (line[collumn] == searchTerm) :
                matchFound = True
                csvfile.close()
                # Return the line found
                return line

    # If no match found
    if (matchFound == False) :
        csvfile.close()
        return "False"

def createChatroom(name, language, username) :
    # Generate a unique chatroom ID
    chatroomID = uuid.uuid4()

    # Find the user's userID from their username - we can assume that the userID will be found since the username is passed from a cookie, only created if a user has successfully logged in and thus 
    # has their details uploaded to the users.csv file
    userID = searchUsers(username, 1)[0]

    #Add the user to the chatroomUsers.csv file
    with open("database/chatroomUsers.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([userID, chatroomID])
        csvfile.close()

    # Add the database to the chatrooms.csv file:
    with open("database/chatrooms.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([chatroomID, language, name])
        csvfile.close()
    
    # Add the chatroom to chatroomMessages.csv
    with open("database/chatroomMessages.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([chatroomID])
        csvfile.close()

# Find the chatrooms which username has joined
def findChatroomsJoined(username) :
    chatroomsJoined = []
    ChatroomDetails = []

    #  Convert username to a userID
    userID = searchUsers(username, 1)[0]

    # Search chatroomUsers.csv to find all the chatrooms which userID has joined
    with open("database/chatroomUsers.csv", "r") as csvfile:
        # For every line in the csv file
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            if (line[0] == userID) :
                # Append the database ID to databases joined
                chatroomsJoined.append(line[1])
        csvfile.close()

    # Find the name and language of every chatroom in chatroomsJoined
    with open("database/chatrooms.csv", "r") as csvfile:
        # For every line in the file:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            # Look at every chatroomID in chatroomsJoined
            for chatroom in range (0, len(chatroomsJoined)):
                # If the line in chatrooms.csv being viewed describes a database which the user has joined
                if (line[0] == chatroomsJoined[chatroom]) :
                    # Append the name and language of the chatroom to chatroom details
                    ChatroomDetails.append(line[1])
                    ChatroomDetails.append(line[2])
    
    return ChatroomDetails

def searchChatrooms() :
    # Get an array of all the chatrooms which have been created
    chatrooms = []

    # Open the file in read mode
    with open("database/chatrooms.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        # For each line in the file
        for line in csvreader :
            # Add the chatroom name
            chatrooms.append(line[2])
    return chatrooms

def addUserToChatroom (username, chatroomName) :
    #  Convert username to the userID
    userID = searchUsers(username, 1)[0]

    # Convert chatroom name to the chatroomID
    chatroomID = locateChatroomCollumn(chatroomName, 2)[0]

    # Add the userID and chatroomID to the chatroomUsers.csv file
    with open("database/chatroomUsers.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([userID, chatroomID])
        csvfile.close()

# Add an amount of xp to a user's profile
# note in users.csv, element 3 = total xp and element 4 is streak length, and element 5 is the xp for the given week
def addXPToUser(XP, user) :
    #  Convert username to a userID
    userID = searchUsers(user, 1)[0]
    userDetails = [[]]

    # For every line in users.csv
    with open("database/users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            #If the line is not blank
            if (len(line) != 0) :
                # If the current line contains the information for user
                if (line[0] == userID) :
                    # Add XP to the current XP value
                    line[3] = str(int(line[3]) + XP)
                    # Also add xp to the weekly xp value
                    line[5] = str(int(line[5]) + XP)
                    userDetails.append(line)
                else :
                    userDetails.append(line)
    csvfile.close()

    # Replace users.csv with the new edited data in userDetails
    with open("database/users.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, len(userDetails)):
            csvwriter.writerow(userDetails[i])
    csvfile.close()

# Uploads a message to chatroommessages.csv
def uploadMessage(message, chatroomName, user) :
    # Convert chatroom name to the chatroomID
    chatroomID = locateChatroomCollumn(chatroomName, 2)[0]

    messagesList = [[]]
    i = 0

    xpGained = calculateXP(message)
    addXPToUser(xpGained, user)

    # Messages are in the format: chatroomID, message1, message2, message3...
    # Save the file to memerory
    with open("database/chatroomMessages.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        # For each line in the file
        for line in csvreader :
            # If line does not equal nothing
            if (len(line) != 0) :
                # If the current line stores all messages for chatroomID
                if (line[0] == chatroomID) :
                    # Add message to the line and save it to messagesList
                    line.append(message)
                    for collumn in range(0, len(line)) :
                        messagesList[i].append(line[collumn])
                    messagesList.append([])
                else :
                    # Otherwise save the line to messages list
                    messagesList.append(line)
                i = i + 1
    csvfile.close()

    # Replace chatroomMessages.csv with the data in messages
    with open("database/chatroomMessages.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, len(messagesList)):
            csvwriter.writerow(messagesList[i])
    csvfile.close()

def readChatroomMessages(chatroomName) :
    # Convert chatroom name to the chatroomID
    chatroomID = locateChatroomCollumn(chatroomName, 2)[0]

    messagesList = []

    # For every line in chatroomMessages.csv
    with open("database/chatroomMessages.csv", "r") as csvfile :
        csvreader = csv.reader(csvfile)
        for line in csvreader :
            # If line is not blank 
            if (len(line) != 0) :
                # If the current line stores the data for chatroomID
                if (line[0] == chatroomID) :
                    # Store all the messages in line to messagesList (store every item in line after the first in messageslist)
                    for i in range(1, len(line)) :
                        messagesList.append(line[i])

    return messagesList


# Run when a messages is sent - increment the streak data for the user
def increaseStreak(user) :

    #  Convert username to a userID
    userID = searchUsers(user, 1)[0]

    userDetails = [[]]

    # Increase the streak
    # Open the users.csv file where element 3 = total xp and element 4 is streak length, and element 5 is the xp for the given week
    with open("database/users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        # For every line in csvreader
        for line in csvreader:
            #If the line is not blank
            if (len(line) != 0) :
                # If the current line contains the information for user
                if (line[0] == userID) :
                    # Add XP to teh current XP value
                    line[4] = str(int(line[4]) + 1)
                    userDetails.append(line)
                else :
                    userDetails.append(line)
    csvfile.close()

    # Replace the text in users.csv with the data in userDetails
    with open("database/users.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, len(userDetails)):
            # If the line is not blank
            print ("userdetails" + str(userDetails[i]))
            if (userDetails[i] != []) :
                # Add the line to users.csv
                csvwriter.writerow(userDetails[i])
    csvfile.close()


# Reset the streak back to zero
def resetStreak(user) :

    #  Convert username to a userID
    userID = searchUsers(user, 1)[0]

    userDetails = [[]]

    # Increase the streak
    # Open the users.csv file where element 3 = total xp and element 4 is streak length, and element 5 is the xp for the given week
    with open("database/users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        # For every line in csvreader
        for line in csvreader:
            #If the line is not blank
            if (len(line) != 0) :
                # If the current line contains the information for user
                if (line[0] == userID) :
                    # Add XP to teh current XP value
                    line[4] = "0"
                    userDetails.append(line)
                else :
                    userDetails.append(line)
    csvfile.close()

    # Replace the text in users.csv with the data in userDetails
    with open("database/users.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(0, len(userDetails)):
            # If the line is not blank
            print ("userdetails" + str(userDetails[i]))
            if (userDetails[i] != []) :
                # Add the line to users.csv
                csvwriter.writerow(userDetails[i])
    csvfile.close()

# Returns the user's streak
def findStreak(user) :
    #  Convert username to a userID
    userID = searchUsers(user, 1)[0]
    streak = 0

    # Open the users.csv file
    with open("database/users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        # For every line in users.csv
        for line in csvreader:
            # If the line is not blank
            if (len(line) != 0) :
                # If the line contains the details for user
                if (line[0] == userID) :
                    # Save the user's streak
                    streak = line[4]
    csvfile.close()
    return streak

# Check if the weekly xp count needs to be reset. If so, reset if
def checkIfWeeklyXPNeedsReset(lastResetYear, lastResetMonth, lastResetDay, user) :
    #  Convert username to a userID
    userID = searchUsers(user, 1)[0]

    reset = False

    userDetails = [[]]

    # Convert the last reset year, month and day to datetime format
    lastReset = datetime.datetime(int(lastResetYear), int(lastResetMonth), int(lastResetDay))
    # Get the current date
    date = datetime.datetime.now()
    # Find how long ago the last streak was
    delta = date - lastReset

    # If the last reset was more that a week ago
    if (delta.days > 6) :
    # Open the users.csv file where element 3 = total xp and element 4 is streak length, and element 5 is the xp for the given week
        with open("database/users.csv", "r") as csvfile:
            csvreader = csv.reader(csvfile)
            # For every line in csvreader
            for line in csvreader:
                #If the line is not blank
                if (len(line) != 0) :
                    # If the current line contains the information for user
                    if (line[0] == userID) :
                        # Reset the streak
                        line[5] = "0"
                        userDetails.append(line)
                        reset = True
                    else :
                        userDetails.append(line)
        csvfile.close()

        # Replace the text in users.csv with the data in userDetails
        with open("database/users.csv", "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            for i in range(0, len(userDetails)):
                # If the line is not blank
                print ("userdetails" + str(userDetails[i]))
                if (userDetails[i] != []) :
                    # Add the line to users.csv
                    csvwriter.writerow(userDetails[i])
        csvfile.close()

    return reset

# Return a list of users sorted by their weekly xp in the format: user, xp, user, xp...
def sortUsersByXP() :
    users = []
    usersXP = []

    # Fill users and usersXP with the relevant data
    # Open the users.csv file
    with open("database/users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        
        # For every line in the file
        for line in csvreader:
            # If the line is not blank
            if (len(line) != 0) :
                # Store the username in users
                users.append(line[1])
                # Store the user's xp in usersXP
                usersXP.append(line[5])

    # Using usersXP, sort users and usersXP in descending order and return th given array - in format user, xp, user, xp...
    return sortUsersOnLeaderBoard(users, usersXP)