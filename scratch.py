questions = ["1", "1", "1", "4", "5", "6", "1"]

def questionType(questionID):
    if questionID == "0":
        return "All Questions"
    elif questionID == "1":
        return "Reference Questions"
    elif questionID == "2":
        return "Guest Passes"
    elif questionID == "3":
        return "Technology Questions"
    elif questionID == "4":
        return "Reader's Advisory Questions"
    elif questionID == "5":
        return "Directional Questions"
    elif questionID == "6":
        return "Interloan Requests"
    elif questionID == "7":
        return "Referrals"
    elif questionID == "8":
        return "Game Computer Requests"
    elif questionID == "9":
        return "Other Questions"
    elif questionID == "999":
        return "Please Select a Question Type"
    else:
        return "Weird"

for i in range(0, len(questions)):
    qType = questionType(questions[i])
    if qType != "Weird":
        questions[i] = qType

print(questions)
