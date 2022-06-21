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
