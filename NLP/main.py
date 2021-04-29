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

# Library Imports
import pandas as pd
import re

# Init of pandas dataframe
column_names = ["question", "answer"]
df = pd.DataFrame(columns = column_names)

# Imports to extract wikipedia pages
from urllib.request import urlopen
from bs4 import BeautifulSoup

# To remove stopwords and evaluate strings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

def Remove_stopwords(string):
    """Removes stop words from the given string

    Args:
        string (string): sentence with words to remove
    Returns:
        list: tokens from filtered sentence
    """    
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

# Config variables
subjects_file = 'subjects.txt'

# Open the subjects given and put them in a list
with open(subjects_file) as f:
    content = f.readlines()
subjects = [x.strip() for x in content] 

# Extract the links, clean the text and run the NLP on it.
for link in subjects:
    source = urlopen(link).read()# Make a soup 
    soup = BeautifulSoup(source,'lxml')

    title = soup.find(id="firstHeading").string

    title = re.sub(r'[^\w\s]', '', title)

    words = Remove_stopwords(title)

    print(words)

    # Extract the plain text content from paragraphs
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.text
        
    # Use regex to clean the text of wikipedia formatting
    text = re.sub(r'\[.*?\]+', '', text)
    text = text.replace('\n', '')
    
    # Hack to generate more questions
    text1 = text.split()[0:500]
    text2 = text.split()[500:1000]

    text1 = ' '.join([str(elem) for elem in text1])
    text2 = ' '.join([str(elem) for elem in text2])

    payload = { "input_text": text1 }

    # Run the model
    qg = main.QGen()
    output = qg.predict_shortq(payload)
    pprint(output)

    # Save the output        
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

    # Now check the dataframe for proper answers
    df["penalty"] = 0

    for i in range(len(df)):
        
        q = df["question"][i].lower()

        # q = ''.join(ch for ch in q if not ch.isupper())
        
        for word in words:
            # print(word, q)
            if word in q:
                print(q, 'contains', word)
                df["penalty"][i] += 1


print(df)
df.to_csv('./dataframe.csv', index = False, header=True)

