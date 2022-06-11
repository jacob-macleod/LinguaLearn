# Handles methods for the database
import csv
import uuid

def addUserToDatabase(username, password) :
    userID = uuid.uuid4()

    with open("database/users.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow([userID, username, password])
    
def searchUsers(searchTerm, collumn) :
    matchFound = False

    # For every line in users.csv
    with open("database/users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            # If the collumn(th) position of the array line = searchTerm (If search term found)
            if (line[collumn] == searchTerm) :
                matchFound = True
                # Return the line found
                return line

    # If no match found
    if (matchFound == False) :
        return "False"
        
searchUsers("Jacrob", 1)