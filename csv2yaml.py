#
# 2020 - T. Middleton Clarkson University (tmiddlet@clarkson.edu)
#
# This source is intended to read in a specific csv file format
# and then export it into individual yaml files. Example of the
# csv file format is listed here. 
# 
# csv file format:
#  1) Assume first column and first row contain identifiers col[0], row[0]
#  2) cell[0,0] is ignored but may have a future use
#  3) cell[0,n] == 'comment(s)' may be a future case
#  4) use columns [1:] for main identifier (e.g. language)
#  5) use rows[1:] to indicate sub identifier (e.g. case)
#
# Example:
#  case   ,English ,French,
#  neutral,teacher ,prof,
#  female ,teacher ,professeuse,
#  male   ,teacher ,professeur ,
#  group  ,teachers,professeurs,
#
# Will generate 8 files. English_neutral.yaml, French_neutral.yaml, English_female.yaml, etc.
#  The files with language_case will contain all elements in the column (language) that have the same 'case'
#
# TODO: (extra credit)
#  1) what if we want multiple values in one language+case?
#  2) make this pull directly from google sheets
#  3) Maybe allow to "span" cases? assume that last seen value in a column when case is blank? risky if no values entered.
#     a) Maybe force an ID into the csv to group like terms to allow spanning
#  4) allow way to exclude items

#Built-in python libraries
import argparse
import collections
import csv
import logging
import os
import os.path
import sys
import time

#third-party libraries
import yaml

#local libraries

#MODELS = "/home/tmiddlet_/languages/data/models/"
#PAIRS = "/home/tmiddlet_/languages/script/PAIRS/"

# To get the paths of the current working directory.
cwd = os.getcwd()
MODELS = str(cwd) + "/models/"
PAIRS = str(cwd) + "/PAIRS/"

#class languagesCSV(csv):
#    def __init__(self, *args, **kwargs):
#        #inherit and act like a csv object.
#        super(self, *args, **kwargs)

def convert_word_pair_to_yaml(csvFilename, yamlDir=''):
    '''This reads in a csv file and converts to the word pairs. The csv must be in a specific
       format as follows:
        1) Column names should be unique and define separate output files
        2) Column named:'Pair ID' is used to group word pairs
        e.g.
        Pair ID, English , German , ...
        1      , woman   , Frau   , ...
        1      , man     , Mann   , ...
        2      , daughter, Tochter, ...
        2      , son     , Sohn   , ...
    '''
    languageData = {}
    languages = []
    with open(csvFilename, newline='') as csvFile:
        languagesCSV = csv.DictReader(csvFile)
        logging.debug(languagesCSV.fieldnames)
        #Remove Pair ID and comment from the list since they are not "languages"
        languages = set(languagesCSV.fieldnames) - set(['Pair ID','comment'])
        for lang in languages:
            #'languages' create entries
            logging.debug(lang)
            languageData[lang] = {'word_pairs':{}}
        for line in languagesCSV:
            logging.debug(line)
            for lang in languages:
                try:
                    languageData[lang]['word_pairs'][line['Pair ID']].append(line[lang])
                except KeyError as e:
                    languageData[lang]['word_pairs'][line['Pair ID']] = [line[lang]]

        logging.debug(languageData)

    
    
    #now push all out to yaml files.
    for lang in languageData:
        print(languageData[lang])
        #First we convert the word_pairs to list of list vs dict of list
        languageData[lang]['word_pairs'] = [languageData[lang]['word_pairs'][pair] for pair in languageData[lang]['word_pairs']]
        print(languageData[lang])
        with open(os.path.join(yamlDir, 'pair_{}.yaml'.format(lang)), 'wb') as yamlFile:
            yaml.dump(languageData[lang], yamlFile, encoding='utf-16-le', allow_unicode=True)


def convert_sets_to_yaml(csvFilename, yamlDir=''):
    #This converts data from the Definig Sets spreadsheet format (See above)
    languageData = {}
    languages = []
    with open(csvFilename, newline='') as csvFile:
        languagesCSV = csv.DictReader(csvFile)
        logging.debug(languagesCSV.fieldnames)
        languages = set(languagesCSV.fieldnames) - set(['include','ID'])
        for lang in languages:
            #'languages' create entries
            logging.debug(lang)
            languageData[lang] = {"neutral_words":[]}
        
        for line in languagesCSV:
            logging.debug("line:" + str(line))

            logging.debug("Inlucde ? " + str(line["include"] == "y")) 
            if line["include"] == "y":
                for lang in languages:
                    logging.debug(line[lang])
                    languageData[lang]["neutral_words"].append(line[lang])
            elif line["include"] == "ISO639-3":
                for lang in languages:
                    logging.debug(MODELS + line[lang].upper() + "WIKI")
                    languageData[lang]["model"] = MODELS + line[lang].upper() + "WIKI"
                    languageData[lang]["pairs"] = PAIRS + "pair_" + line[lang].upper() + ".yaml"

        logging.debug(languageData)
    
    #now push all out to yaml files.
    for lang in languageData:
        print(lang)
        #TODO should check for special characters or spaces (spaces = '_'?)
        with open(os.path.join(yamlDir, '{}.yaml'.format(lang)), 'wb') as yamlFile:
            yaml.dump(languageData[lang], yamlFile, encoding='utf-16-le', allow_unicode=True)

def convert_sets_to_newcsv(csvFilename, yamlDir=''):
    #This converts data from the Definig Sets spreadsheet format (See above)
    languageData = {}
    languages = []
    outputLines = collections.OrderedDict()
    outputFields = []
    with open(csvFilename, newline='') as csvFile:
        languagesCSV = csv.DictReader(csvFile)
        logging.debug(languagesCSV.fieldnames)
        languages = set(languagesCSV.fieldnames) - set(['case','comment'])
        for line in languagesCSV:
            logging.debug(line)
            newDict = dict() #Make a new dictionary
            for lang in languages:
                key = f'{lang}-{line["case"]}'
                #stow the keys for later
                outputFields.append(key)
                newDict[key] = line[lang]
            logging.debug(newDict)
            try:
                outputLines[line['English']].update(newDict)
            except KeyError as e:
                outputLines[line['English']] = dict(newDict) #force a copy
            print(outputLines[line['English']])
            
    #logging.debug(outputLines)
    with open(os.path.join(yamlDir, 'output.csv'), 'w', newline='') as csvOut:
        outputFields = list(set(outputFields)) #trim duplicates
        outputFields.sort() #make it sorted alphabetically for output
        outputCSVWriter = csv.DictWriter(csvOut,outputFields)
        outputCSVWriter.writeheader()
        for langCase in outputLines:
            logging.debug(langCase)
            outputCSVWriter.writerow(outputLines[langCase])
 

def main(args):
    timeStamp = time.strftime('%Y%M%d')

    if args.output_dir == '':
        yamlDir = timeStamp
    else:
        yamlDir = args.output_dir

    if not os.path.exists(yamlDir):
        logging.warning(f'Path: {yamlDir} not found, attempting to create directories.')
        os.mkdir(yamlDir)

    if args.reformat:
        convert_sets_to_newcsv(args.input_file, yamlDir=yamlDir)
    elif args.pairs:
        convert_word_pair_to_yaml(args.input_file, yamlDir=yamlDir)
    else:
        convert_sets_to_yaml(args.input_file, yamlDir=yamlDir)
    return 0


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('input_file', help='CSV File with data to convert')
    argParser.add_argument('output_dir', nargs='?', default='',  help='YAML file output directory')
    argParser.add_argument('--debug', action='store_true', help='Enables debug printing')
    argParser.add_argument('--pairs', action='store_true', help='Default is word lists, this enables word pairs filetype')
    argParser.add_argument('--reformat', action='store_true', help='Default is word lists, this enables word pairs filetype')
    argParser.add_argument('--log', metavar='Log Filename', default=None, help='Logging Filename and enables logging.')
    args = argParser.parse_args()
    #defaults to INFO output, but can set debug to enable debugging output.
    if args.debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    logging.basicConfig(filename=args.log,level=logLevel)
    sys.exit(main(args))

