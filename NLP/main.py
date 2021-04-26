from pprint import pprint
from Questgen import main
import pickle
import pandas as pd

column_names = ["question", "answer"]
df = pd.DataFrame(columns = column_names)

# f = open("payload.txt")
# line = f.read().replace("\n", " ")
# f.close()


# Based on https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b
# https://towardsdatascience.com/questgen-an-open-source-nlp-library-for-question-generation-algorithms-1e18067fcdc6
# Import package
import wikipedia    # Specify the title of the Wikipedia page
# wiki = wikipedia.page('Nazi Germany') # Extract the plain text content of the page
# text = wiki.content

with open('subjects.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
subjects = [x.strip() for x in content] 

loading = False

myDict = {}

for subject in subjects:

    text = wikipedia.summary(subject, sentences=10) # Extract the plain text content of the page

    # Import package
    import re   # Clean text
    text = re.sub(r'==.*?==+', '', text)
    text = text.replace('\n', '')
    print(text)

    # qe= main.BoolQGen()
    payload = { "input_text": text }

    # FAQ Questions
    print('FAQ')

    if loading:
        output = pickle.load(open("output.pickle", "rb" ))

    else:
        qg = main.QGen()
        output = qg.predict_shortq(payload)
        pprint(output)
        with open('output.pickle', 'wb') as f:
            pickle.dump(output, f)
        
    print('nicely formatted')
    for item in output['questions']:
        # print(item)
        print(item['Question'], item['Answer'])
        new_line = {'question': item['Question'], 'answer': item['Answer']}
        df = df.append(new_line, ignore_index=True)


print('end')
print(df)
df.to_csv('./dataframe.csv', index = False, header=True)
