# TODO more criteria ?
#   Tries to give a variety of answers to compare against the guess of the player
#       - All answers are correct, just different from a linguistic pov 
#
#   This includes:
#       - Name support: Name initials can be used freely. E.g. D.J. Trump; Donald J. Trump
#               (just answering the surname is not sufficient)
#       - Number support: E.g. Iphone Two -> Iphone2.

# TODO: Accents -- unicode normalizing...
#       Objectification -- "The", "A"...
import re
from num2words import num2words
from difflib import SequenceMatcher

EQUALITY_RATIO = 0.8

numbers_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero' : '0'
}

def getNameVariants(answer):
    variants = []
    
    index = len(answer.split()) - 2 # Not the surname
    variants.append(answer)
    while index >= 0:
        name = answer.split()
        name[index] = name[index][0] + '.'
        variants.append(' '.join(name))
        index -= 1
        answer = ' '.join(name)
    return variants

def getStringNoNumbers(answer): # Assumes consistency
    validate = answer.split()

    for count, word in enumerate(validate):
        if word.isnumeric():
            validate[count] = num2words(validate[count])
    return ' '.join(validate)

def getStringNumbers(answer): # same
    return ' '.join(numbers_dict[ele] if ele in numbers_dict else ele for ele in answer.split())

def removeInColons(answer):
    return re.sub('\(.*?\)', '', answer)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def answerIsValid(guess, answer):
    assert len(guess) > 0
    guess = guess.lower()
    answer = answer.lower()
    
    answers = getNameVariants(answer)

    end = len(answers)
    i = 0
    while i < end:
        answers.append(getStringNoNumbers(answers[i]))
        i += 1
    end = len(answers)
    i = 0
    while i < end:
        answers.append(getStringNumbers(answers[i]))
        i += 1
    end = len(answers)
    i = 0
    while i < end:
        answers.append(removeInColons(answers[i]))
        i += 1
    
    answers = list(set(answers))
    print("Possible answers: " + ' '.join(answers) \
        + "\nApplying equality ratio of " +  str(EQUALITY_RATIO))

    for x in answers:
        if similar(guess, x) > EQUALITY_RATIO:
            return True

    return False