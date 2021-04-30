# TODO more criteria ?
# e.g. initials instead of full name
# to lower
# check whether string contains answer

def answerIsValid(guess, answer):
    if guess.lower() in answer.lower():
        return True
    return False
