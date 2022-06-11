# Handles methods for the database
import csv
from re import search
import uuid

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
            if (line[collumn] == searchTerm) :
                matchFound = True
                csvfile.close()
                # Return the line found
                return line

    # If no match found
    if (matchFound == False) :
        csvfile.close()
        return "False"

def createDatabase(name, language, username) :
    # Generate a unique chatroom ID
    chatroomID = uuid.uuid4()

    # Find the user's userID from their username - we can assume that the userID will be found since the username is passed from a cookie, only created if a user has successfully logged in and thus 
    # has their details uploaded to the users.csv file
    userID = searchUsers(username, 1)[1]
    print (userID)

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

