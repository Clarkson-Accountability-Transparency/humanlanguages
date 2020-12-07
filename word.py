import sys
import argparse
import logging

import yaml

import numpy as np
from wikipedia2vec import Wikipedia2Vec

def count_words(model, words):
    [print(w, model.get_word(w).count) for w in words]
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
        exit_code += count_words(wiki2vec, data['neutral_words'])
        exit_code += count_words(wiki2vec, data['word_pairs_flat'])
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
