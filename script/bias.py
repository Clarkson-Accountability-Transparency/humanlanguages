#!/bin/env python3

import sys
import argparse
import logging

import yaml
import csv

import numpy as np
from sklearn.decomposition import PCA
from wikipedia2vec import Wikipedia2Vec
from os import listdir


def defining_set_direction(defining_sets, n=0):
    matrix = []
    for (w1,w2) in defining_sets:
        center = (w1+w2)/2 #center for covariance to be nice
        matrix.append(w1-center)
        matrix.append(w2-center)
    pca = PCA(n_components=10)
    #print("data matrix is: ")
    #print(matrix)
    pca.fit(matrix)
    #print("Explained Variance Ratio: " + str(pca.explained_variance_ratio_)) 
    return pca.components_[n]

def compute_bias_direction(model, pairs, n=0, ransac=False):
    defining_sets = []
    words = []
    for (w1,w2) in pairs:
        try:
            w1 = w1.lower().split()
            w1vec = sum([model.get_word_vector(w) for w in w1])
            w2 = w2.lower().split()
            w2vec = sum([model.get_word_vector(w) for w in w2])
            vector_pair = (w1vec,w2vec)

            defining_sets.append(vector_pair)
            words.append((' '.join(w1),' '.join(w2)))
        except KeyError as e:
            print("Marzieh owes me a dragon")
            print("Error on " + str((w1,w2)))
            pass

    g = defining_set_direction(defining_sets, n)
    return g

def bias_by_word(model, neutral_words, defining_set, pca):
    ret_code = 0
    g = compute_bias_direction(model, defining_set, pca)
    
    # This is much slower because its calculating len(neutral_words) dot products instead of 1
    for word in neutral_words:
        #if word in model:
        if model.dictionary.get_word(word) is not None:
            v = model.get_word_vector(word)
            bias = np.dot(v,g)/(np.linalg.norm(v)*np.linalg.norm(g))
            print(word + "," + str(bias))
        else:
            print(word + ",NA")
            pass
    return ret_code

def count_words(model, words):
    [print(w,',', model.get_word(w).count) if model.get_word(w) else print(w,',',0) for w in words]
    return 0 

def main(args):
    ### The following was used to create the initial yaml files.
    ##new_yaml = {'language':'English', 'language_code':'en', 'model':MODEL, 'neutral_words':NEUTRAL_WORDS, 'word_pairs':WORD_PAIRS}
    ##with open('english.yaml', 'wb') as yamlFile:
    ##    yaml.dump(new_yaml, yamlFile, encoding='utf-16-le', allow_unicode=True)
    ##print(word_pairs_flat)
    ##print(new_yaml)

    exit_code = 0

    logging.debug(f'Processing Neutral File: "{args.config}"')
    with open(args.config, 'rb') as yamlFile:
        #ASSUME that we are using a safe source for yaml.
        config=yaml.load(yamlFile, Loader=yaml.FullLoader)
        #DEBUG:
        logging.debug(config)
    
    model = config["model"]
    pairs_location = config["pairs"]

    logging.debug(f'Processing Pairs File: "{pairs_location}"')
    with open(pairs_location, 'rb') as yamlFile:
        #ASSUME that we are using a safe source for yaml.
        pairs=yaml.load(yamlFile, Loader=yaml.FullLoader)
        #DEBUG:
        logging.debug(pairs)

    #complicated list comprehension, but basically iterates through data['word_pairs'] and returns a flat list of the list of lists.
    pairs['word_pairs_flat'] = [item for pair in pairs['word_pairs'] for item in pair]
    
    # Load model
    wiki2vec = Wikipedia2Vec.load(model)

    if args.count:
        # Find word count
        exit_code += count_words(wiki2vec, config['neutral_words'])
        exit_code += count_words(wiki2vec, pairs['word_pairs_flat'])
    else:
        # Calculate bias
        exit_code += bias_by_word(wiki2vec, config['neutral_words'], pairs['word_pairs'], 1)
        exit_code += bias_by_word(wiki2vec, pairs['word_pairs_flat'], pairs['word_pairs'], 1)
    
    return exit_code

if __name__ == "__main__":
    #Gather arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument('config', help='YAML file with neutral words, model and location of pairs.')
    #argParser.add_argument('csvfile', help='Location where a CSV of output data is written')
    argParser.add_argument('--count', action='store_true', help='counts the occurence of words instead of calculating bias')
    argParser.add_argument('--debug', action='store_true', help='Enables debug printing')
    argParser.add_argument('--log', metavar='Log Filename', default=None, help='Logging Filename and enables logging.')
    args = argParser.parse_args()
    #defaults to INFO output, but can set debug to enable debugging output.
    if args.debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    logging.basicConfig(filename=args.log,level=logLevel)

    sys.exit(main(args))
