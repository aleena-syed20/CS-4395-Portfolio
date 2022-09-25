#Aleena Syed - AZS180003
#CS 4395.001

import sys  # to get the system parameter
import os   # used by method 1  
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

def method1(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

def findLexicalDiversity(text_in):
    listy = []
    listy = word_tokenize(text_in)
    set_toks = set(listy)
    lexical_diversity = (len(set_toks) / len(listy))
    print(lexical_diversity)

def preprocessText(text_in):
    listy = []
    listy = word_tokenize(text_in)
    l_tokens = [t.lower() for t in listy]
    l1_tokens = [t for t in l_tokens if t.isalpha() and
           t not in stopwords.words('english') and len(t) > 5]
    # get the lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in l1_tokens]
    # make unique
    lemmas_unique = list(set(lemmas))
    tags = pos_tag(lemmas_unique)
    #print(tags[:20])
    nouns = []
    for index, tuple in enumerate(tags):
        if (tuple[1] == 'NN' or tuple[1] == 'NNS'):
            nouns.append(tuple)
    print(len(listy))
    print(len(nouns))
    return l1_tokens, nouns

def saveDictionary(tokens, nouns):
    dict_nouns = {}
    for t in tokens:
        for index, tup in enumerate(nouns):
            if t == tup[0]:
                if t in dict_nouns:
                    v = dict_nouns.get(t)
                    v += 1
                    dict_nouns[t] = v
                else:
                    dict_nouns[t] = 1

    dict_nouns = dict(sorted(dict_nouns.items(), key=lambda item: item[1], reverse=True))
    print(dict(list(dict_nouns.items())[0:50]))
    fifty_nouns = (list(dict_nouns.keys())[0:50])
    return fifty_nouns

def playGuessingGame(words):
    #print(words)
    seed(1234)
    index = randint(0, 49)
    guess_this_word = words[index]
    print(guess_this_word)
    score = 5
    print("Let's play a guessing game!")
    guess_string = []
    guess_string.append("_")
    for _ in range(len(guess_this_word) - 1):
            guess_string.append(" _")
    print("".join(guess_string))
    guessed_letter = input("Guess a letter: ")
    while (score >= 0 or guessed_letter == '!'):
        if guessed_letter in guess_this_word:
            score += 1
            print("Right! Score is " + str(score))
            for idx, itm in enumerate(guess_this_word):
                if itm == guessed_letter:
                    guess_string[idx] = guessed_letter
            #guess_string[:] = [x if x != "_" or " _" else guessed_letter for x in guess_string]
        else:
            score -= 1
            print("Sorry, guess again. Score is " + str(score))
        print("".join(guess_string))
        if '_' and ' _' not in guess_string:
            print("You solved it!")
            print("Current score: " + str(score))
            print("Guess another word")
            index = randint(0, 49)
            guess_this_word = words[index]
            guess_string = []
            guess_string.append("_")
            for _ in range(len(guess_this_word) - 1):
                guess_string.append(" _")
            #score = 5
            print("".join(guess_string))
        guessed_letter = input("Guess a letter: ")
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        text_in = method1(fp)
        findLexicalDiversity(text_in)
        tokens, nouns = preprocessText(text_in)
        fifty_nouns = saveDictionary(tokens, nouns)
        playGuessingGame(fifty_nouns)