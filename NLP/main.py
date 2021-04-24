from pprint import pprint
from Questgen import main

# f = open("payload.txt", "r")
# print(f.read()) 

# f = open("payload.txt")
# line = f.read().replace("\n", " ")
# f.close()

# exit(0)

# Import package
import wikipedia    # Specify the title of the Wikipedia page

# print(wikipedia.search("Hitler"))

# wiki = wikipedia.page('Nazi Germany') # Extract the plain text content of the page
# text = wiki.content

text = wikipedia.summary('Barrack Obama', sentences=10) # Extract the plain text content of the page


# print(text)

# Import package
import re   # Clean text
text = re.sub(r'==.*?==+', '', text)
text = text.replace('\n', '')
print(text)

qe= main.BoolQGen()
payload = {
            "input_text": text
        }

# Boolean Questions
print('Boolean')
output = qe.predict_boolq(payload)
pprint (output)

print('############################################################################################')

# Multiple Choice Questions
print('MCQ')
qg = main.QGen()
output = qg.predict_mcq(payload)
pprint (output)

print('############################################################################################')

# FAQ Questions
print('FAQ')
output = qg.predict_shortq(payload)
pprint (output)

# print('############################################################################################')

# # Paraphrasing Questions
# print('Paraphrasing')
# payload2 = {
#     "input_text" : "What is Sachin Tendulkar profession?",
#     "max_questions": 5
# }
# output = qg.paraphrase(payload2)
# pprint (output)


# print('############################################################################################')
# print('Question Answering')
# # Question Answering
# answer = main.AnswerPredictor()

# payload3 = {
#     "input_text" : '''Sachin Ramesh Tendulkar is a former international cricketer from 
#               India and a former captain of the Indian national team. He is widely regarded 
#               as one of the greatest batsmen in the history of cricket. He is the highest
#                run scorer of all time in International cricket.''',
#     "input_question" : "Who is Sachin tendulkar ? "
    
# }
# output = answer.predict_answer(payload3)
# pprint (output)

# print('############################################################################################')

# # Question Answering (Boolean)
# print('Question Answering (Boolean)')

# payload4 = {
#     "input_text" : '''Sachin Ramesh Tendulkar is a former international cricketer from 
#               India and a former captain of the Indian national team. He is widely regarded 
#               as one of the greatest batsmen in the history of cricket. He is the highest
#                run scorer of all time in International cricket.''',
#     "input_question" : "Is Sachin tendulkar  a former cricketer? "
# }
# output = answer.predict_answer(payload4)
# print (output)