#!/usr/bin/python3
from gensim.models import Word2Vec
from ast import literal_eval as readlist
from nltk.tokenize import word_tokenize
import jieba
import sys
import nltk.data

if __name__ == "__main__":
    with open("spanish.txt", "r") as f:
        text = f.read()
    
    tokenizer = nltk.data.load('file:/usr/nltk_data/tokenizers/punkt/spanish.pickle')
    sentences = [ word_tokenize(s) for s in tokenizer.tokenize(text.strip()) ]

    print("Model is training....")
    model = Word2Vec(sentences,size=100,min_count=1)
    print("Model is trained!!")
    model.save("spanish.model")
