  # Calculate the number of XP points given for a message
def calculateXP(message) :
    # 1 XP point given per word
    messageArr = message.split(" ")
    return len(messageArr)

# Bubble sort algorithmn to sort usersXP. Any change made to usersXP will be applied to users, so that users is also sorted in order of usersXP
# Data sorted is in descending order
# Once sorted, the data is returned in the format user, xp, user, xp...
def sortUsersOnLeaderBoard(users, usersXP) :
  arrayToReturn = []
  swapMade = True

  while (swapMade == True) :
    swapMade = False
    # For every element in list
    for i in range(0, len(usersXP)):
      # If the end of the array is not reached
      if (i != len(usersXP)-1) :
        # If the next element is bigger than the current element
        if (int(usersXP[i]) > int(usersXP[i+1])) :
          # Swap items in usersXP array
          temp = usersXP[i]
          usersXP[i] = usersXP[i+1]
          usersXP[i+1] = temp

          # Swap items in users array
          temp = users[i]
          users[i] = users[i+1]
          users[i+1] = temp

          swapMade = True

  # Combine usersXP and users into a single array in the format user, xp, user, xp
  for item in range(0, len(usersXP)) :
    arrayToReturn.append(users[item])
    arrayToReturn.append(usersXP[item])

  return arrayToReturn