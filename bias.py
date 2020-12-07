import sys
import argparse
import logging

import yaml

import numpy as np
from sklearn.decomposition import PCA
from wikipedia2vec import Wikipedia2Vec

def defining_set_direction(defining_sets, n=0):
    matrix = []
    for (w1,w2) in defining_sets:
        center = (w1+w2)/2 #center for covariance to be nice
        matrix.append(w1-center)
        matrix.append(w2-center)
    pca = PCA(n_components=3)
    #print("data matrix is: ")
    #print(matrix)
    pca.fit(matrix)
    print("Explained Variance Ratio: " + str(pca.explained_variance_ratio_)) 
    print(pca.components_[n])
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
            print("One of these words are missing: " + str((w1,w2)))
            pass

    g = defining_set_direction(defining_sets, n)
    return g

def corpus_bias(model, neutral_words, defining_set):
    g = compute_bias_direction(model, defining_set)
    print("Computing bias now")

    # The sum of all word vectors
    total = np.zeros(100);
    count = 0.0

    # The sum of dot products is the dot product of the sum
    for word in neutral_words:
        #if word in model:
        if model.dictionary.get_word(word) is not None:
            total += np.copy(model.get_word_vector(word))
            count += 1.0
        else:
            #print("word " + word + " not in model")
            pass

    # We only need 1 dot product
    total_bias = np.abs(np.dot(total,g)/(np.linalg.norm(total)*np.linalg.norm(g)))
    print(total_bias)

def bias_by_word(model, neutral_words, defining_set, pca):
    g = compute_bias_direction(model, defining_set, pca)
    print("Computing bias now")
    
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
    
    return 0

def main(yamlFilename):
   
    ### The following was used to create the initial yaml files.
    ##new_yaml = {'language':'English', 'language_code':'en', 'model':MODEL, 'neutral_words':NEUTRAL_WORDS, 'word_pairs':WORD_PAIRS}
    ##with open('english.yaml', 'wb') as yamlFile:
    ##    yaml.dump(new_yaml, yamlFile, encoding='utf-16-le', allow_unicode=True)
    ##print(word_pairs_flat)
    ##print(new_yaml)

    exit_code = 0
    logging.info(f'Processing "{yamlFilename}"')
    with open(yamlFilename, 'rb') as yamlFile:
        #ASSUME that we are using a safe source for yaml.
        data=yaml.load(yamlFile)
        #DEBUG:
        logging.debug(data)

    try:
        logging.info(f'Language: "{data["language"]}"')
        #complicated list comprehension, but basically iterates through data['word_pairs'] and returns a flat list of the list of lists.
        data['word_pairs_flat'] = [item for pair in data['word_pairs'] for item in pair]
        wiki2vec = Wikipedia2Vec.load(data['model'])
        exit_code += bias_by_word(wiki2vec, data['neutral_words'], data['word_pairs'], 0)
        exit_code += bias_by_word(wiki2vec, data['word_pairs_flat'],data['word_pairs'], 0)
        #exit_code += bias_by_word(wiki2vec, data['neutral_words'], data['word_pairs'], 1)
        #exit_code += bias_by_word(wiki2vec, data['word_pairs_flat'],data['word_pairs'], 1)
    except KeyError as e:
        logging.error(f'Unable to load key "{e.args[0]}" make sure it is in the yaml file!')
    return exit_code

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument('config', help='YAML file with data')
    argParser.add_argument('--debug', action='store_true', help='Enables debug printing')
    argParser.add_argument('--log', metavar='Log Filename', default=None, help='Logging Filename and enables logging.')
    args = argParser.parse_args()
    #defaults to INFO output, but can set debug to enable debugging output.
    if args.debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    logging.basicConfig(filename=args.log,level=logLevel)

    sys.exit(main(args.config))
