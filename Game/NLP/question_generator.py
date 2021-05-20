''' Modern Gaming AI Algorithms

This script extracts Wikipedia articles and uses NLP to generate questions about the text.
Writes results (questions and answers) to a CSV file using pandas.

Written by Luuk Nolden

Used blog posts:
    https://levelup.gitconnected.com/two-simple-ways-to-scrape-text-from-wikipedia-in-python-9ce07426579b
    https://towardsdatascience.com/questgen-an-open-source-nlp-library-for-question-generation-algorithms-1e18067fcdc6

'''

# Import the NLP libraries
from Questgen import main
from pprint import pprint

qg = main.QGen()

# Library Imports
import pandas as pd
import re
import sys
import urllib

# Imports to extract wikipedia pages
from urllib.request import urlopen
from bs4 import BeautifulSoup

def Remove_stopwords(string):
    """Removes stop words from the given string

    Args:
        string (string): sentence with words to remove
    Returns:
        list: tokens from filtered sentence
    """    
    # To remove stopwords and evaluate strings
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize 

    stop_words = set(stopwords.words('english')) 

    word_tokens = word_tokenize(string) 

    filtered_sentence = [w for w in word_tokens if not w in stop_words] 

    filtered_sentence = [] 

    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w.lower()) 
    
    # print(word_tokens) 
    # print(filtered_sentence)

    return filtered_sentence 

link = sys.argv[1]

# Init of pandas dataframe
column_names = ["topic", "question", "answer"]
df = pd.DataFrame(columns = column_names)

source = urlopen(link).read()# Make a soup 
soup = BeautifulSoup(source,'lxml')

# Extract the name of the page
topic_name = link.split("/")[-1]
topic_name_normal = topic_name.replace("_", " ")
title = urllib.parse.unquote(topic_name_normal)

words = Remove_stopwords(title)

# Extract the plain text content from paragraphs
text = ''
for paragraph in soup.find_all('p'):
    text += paragraph.text
    
# Use regex to clean the text of wikipedia formatting
text = re.sub(r'\[.*?\]+', '', text)
text = text.replace('\n', '')

# Hack to generate more questions
text_splitted = text.split()

previous_split = 100
while not text_splitted[previous_split][-1] == ".":
        previous_split = previous_split + 1
previous_split = previous_split + 1
split_point = previous_split + 50

while len(df) < 10 and split_point < len(text_splitted):
    while not text_splitted[split_point-1][-1] == ".":
        split_point = split_point + 1

    text1 = text_splitted[previous_split:split_point]

    text1 = ' '.join([str(elem) for elem in text1])

    payload = { "input_text": text1 }

    # Run the model
    qg = main.QGen()
    output = qg.predict_shortq(payload)
    pprint(output)

    # Save the output

    if len(output) > 0:    
        for item in output['questions']:
            if len(item['Question']) < 100:
                print(item['Question'], item['Answer'])
                new_line = {'topic': title, 'question': item['Question'], 'answer': item['Answer']}
                df = df.append(new_line, ignore_index=True)

    previous_split = split_point
    split_point = split_point + 50

if split_point >= len(text_splitted):
    sys.exit(1)

# Now check the dataframe for proper answers
df["penalty"] = 0

for i in range(len(df)):
    
    q = df["question"][i].lower()
    a = df["answer"][i].lower()
   
    for word in words:
        # print(word, q)
        if word in q:
            print(q, 'contains', word)
            df["penalty"][i] += 1
        if word in a:
            print(a, 'contains', word)
            df["penalty"][i] += 1

df = df.sort_values(by=['penalty'])
df = df[:8] # we can only show 8 on screen
print(df)
df.to_csv('dataframe.csv', index = False, header=True)

sys.exit(0)