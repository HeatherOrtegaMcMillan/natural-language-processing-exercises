######## NLP Prepare.py file
# Imports
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

######### Start of Functions 

#################### ~~~~~ HELPER FUNCTIONS ~~~~~ ####################

def basic_clean(string):
    '''
    This function takes in a string
    Lowercases everything
    Normalizes the unicode
    And removes eveyrhint that's not a number, letter, ', or whitespace
    Returns a string
    can be used with .apply for a dataframe
    '''
    # loop through columns turn everything into lower case
    # works with series
    new_string = string.lower()
            
    # normalize unicode 
    new_string =  unicodedata.normalize('NFKD', new_string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    # remove everything thats not a number letter ' or whitespace
    new_string = re.sub(r"[^a-z0-9'\s]", '', new_string)
    
    return new_string


def tokenize_me(string):
    '''
    This function takes in a string 
    Returns the tokenized string
    Can be used with .apply to apply to dataframe
    '''
    # make tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # tokenize string and assign to new_string
    new_string = tokenizer.tokenize(string, return_str=True)
    
    # return new_string
    return new_string

def stem(string):
    '''
    Function takes in a string
    Returns string stems 
    Uses Porter Stemmer
    can be used with .apply for dataframes
    '''
    # create stemmer
    ps = nltk.porter.PorterStemmer()
    
    # get the stems from string in list
    stems = [ps.stem(word) for word in string.split()]
    
    # join all words in string with a space
    string_stemmed = ' '.join(stems)
    
    return string_stemmed

def lemmatize(string):
    '''
    Function takes in string
    Returns lemmatized string
    
    '''
    
    wnl = nltk.stem.WordNetLemmatizer()

    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    string_stemmed = ' '.join(lemmas)
    
    return string_stemmed

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string
    And returns the string with the English stopwords removed
    Add extra_words (list)
    or exclude_words (list)
    with the optional arguements
    
    -- This might break if the excluded words aren't in the stopwords list
    '''
    # define stopwords list                    # make sure you have the right stuff imported
    stopwords_list = stopwords.words('English')
    
    # add or remove words based on arguements
    stopwords_list = set(stopwords_list) - set(exclude_words) # the set removes words
    
    stopwords_list = stopwords_list.union(set(extra_words))
        
    # remove stopwords from string
    # turn string into list
    words = string.split()
    
    # remove the stopwords
    filtered_words = [w for w in words if w not in stopwords_list]
    
    # turn back into a string
    new_string = ' '.join(filtered_words)
    
    return new_string

################## ~~~~~~ Prep Function ~~~~~~ ##################

def prep_nlp(df, content = 'content', extra_words = [], exclude_words=[] ):
    '''
    This function takes in a dataframe and returns a dataframe with
    an original column
    a cleaned (normalized, tokenized and no stop words) column
    a stemmed column
    and a lemmatized column
    '''
    # original content
    df['original'] = df[content]
    
    #clean (normalized, tokenized, no stopwords)
    df['clean'] = df['content'].apply(basic_clean).apply(tokenize_me).apply(lambda x: remove_stopwords(x, extra_words, exclude_words))
    
    #stemmed (version of clean)
    df['stemmed'] = df['clean'].apply(stem)
    
    #lemmatized (version of clean)
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df
    

