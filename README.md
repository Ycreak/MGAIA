# MGAIA
Navigate to the Game folder
$ cd Game

Create a virtual environment
$ python3 -m venv env

Activate the environment
$ source env/bin/activate

Install the requirements
$ pip3 install -r requirements.txt

Install NLTK and Spacy
$ python3 -m nltk.downloader universal_tagset
$ python3 -m spacy download en

Navigate to the NLP folder and download the following dataset (for question generation):
wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
tar -xvf  s2v_reddit_2015_md.tar.gz

Return to the Game folder and run the game
$ cd ..
$ python3 riddler_game.py
