from pprint import pprint
from Questgen import main
import pickle
import pandas as pd
import re# Clean text

column_names = ["question", "answer"]
df = pd.DataFrame(columns = column_names)



from urllib.request import urlopen
from bs4 import BeautifulSoup# Specify url of the web page

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

for link in subjects:
    source = urlopen(link).read()# Make a soup 
    soup = BeautifulSoup(source,'lxml')

    # Extract the plain text content from paragraphs
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.text
        
    # Import package
    text = re.sub(r'\[.*?\]+', '', text)
    text = text.replace('\n', '')
    
    text1 = text.split()[0:500]
    text2 = text.split()[500:1000]

    text1 = ' '.join([str(elem) for elem in text1])
    text2 = ' '.join([str(elem) for elem in text2])

    # print(text)

    payload = { "input_text": text1 }

    qg = main.QGen()
    output = qg.predict_shortq(payload)
    pprint(output)
            
    for item in output['questions']:
        # print(item)
        print(item['Question'], item['Answer'])
        new_line = {'question': item['Question'], 'answer': item['Answer']}
        df = df.append(new_line, ignore_index=True)

    payload = { "input_text": text2 }

    output = qg.predict_shortq(payload)
    pprint(output)
            
    for item in output['questions']:
        # print(item)
        print(item['Question'], item['Answer'])
        new_line = {'question': item['Question'], 'answer': item['Answer']}
        df = df.append(new_line, ignore_index=True)


print('end')
print(df)
df.to_csv('./dataframe.csv', index = False, header=True)
