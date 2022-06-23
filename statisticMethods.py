  # Calculate the number of XP points given for a message
def calculateXP(message) :
    # 1 XP point given per word
    messageArr = message.split(" ")
    return len(messageArr)