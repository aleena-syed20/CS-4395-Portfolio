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

# reads in text file
def method1(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

# finds lexical diversity of unique tokens in list
def findLexicalDiversity(text_in):
    listy = []
    # tokenize words
    listy = word_tokenize(text_in)
    # get unique tokens
    set_toks = set(listy)
    # calculate lexical diversity
    print("\nLexical diversity: %.2f" % (len(set_toks) / len(listy)))

# processes text and returns list of processed tokens and nouns
def preprocessText(text_in):
    listy = []
    # tokenize word
    listy = word_tokenize(text_in)
    # lowercase words
    l_tokens = [t.lower() for t in listy]
    # removes stopwords, numbers/special symbols and words smaller than 5 characters
    l1_tokens = [t for t in l_tokens if t.isalpha() and
           t not in stopwords.words('english') and len(t) > 5]
    # get the lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in l1_tokens]
    # get unique lemmas
    lemmas_unique = list(set(lemmas))
    # get pos tags for lemmas
    tags = pos_tag(lemmas_unique)
    nouns = []
    # make list of nouns 
    for index, tuple in enumerate(tags):
        if (tuple[1] == 'NN' or tuple[1] == 'NNS'):
            nouns.append(tuple)
    # print length of processed tokens and noun lists
    print("Number of tokens: " + str(len(l1_tokens)))
    print("Number of nouns: " + str(len(nouns)))
    return l1_tokens, nouns

# save nouns and their counts into a dictionary
def saveDictionary(tokens, nouns):
    dict_nouns = {}
    for t in tokens:
        # check if token in list is a noun; if so, add to dict with its current count
        for index, tup in enumerate(nouns):
            if t == tup[0]:
                if t in dict_nouns:
                    v = dict_nouns.get(t)
                    v += 1
                    dict_nouns[t] = v
                else:
                    dict_nouns[t] = 1
    # print 50 most common words in dictionary and their counts
    dict_nouns = dict(sorted(dict_nouns.items(), key=lambda item: item[1], reverse=True))
    print(dict(list(dict_nouns.items())[0:50]))
    fifty_nouns = (list(dict_nouns.keys())[0:50])
    return fifty_nouns

# function that allows user to play guessing game until score is below 0
# or game is manually ended with '!' character
def playGuessingGame(words):
    # randomly generate word
    seed(1234)
    index = randint(0, 49)
    guess_this_word = words[index]
    # set score to 5
    score = 5
    list_of_guessed_letters = []
    print("Let's play a guessing game!")
    # print word with blanks in place of characters
    guess_string = []
    guess_string.append("_")
    for _ in range(len(guess_this_word) - 1):
            guess_string.append(" _")
    print("".join(guess_string))
    guessed_letter = input("Guess a letter: ")
    # play game as long as score is not negative and not '!'
    while (score >= 0 and guessed_letter != '!'):
        # no letter entered; prompt user to enter letter
        if guessed_letter == "":
            print("Sorry, enter a letter.")
        # letter entered
        elif guessed_letter in guess_this_word:
            # if letter entered previously, prompt user for new letter
            if guessed_letter in list_of_guessed_letters:
                print("Sorry, you already entered this letter. Try a new letter.")
            # if letter exists in word and has not been previously entered, add one point to total score
            else:
                list_of_guessed_letters.append(guessed_letter)
                score += 1
                print("Right! Score is " + str(score))
                for idx, itm in enumerate(guess_this_word):
                    if itm == guessed_letter:
                        guess_string[idx] = guessed_letter
        # letter entered; incorrect, subtract one point from total score
        else:
            score -= 1
            if score >= 0:
                print("Sorry, guess again. Score is " + str(score))
            else:
                print("Sorry, your score is below 0. Better luck next time!")
                exit(0)
        print("".join(guess_string))
        # word is guessed; total score is shown; player is prompted to play again
        if '_' not in guess_string and ' _' not in guess_string:
            print("You solved it!")
            print("Current score: " + str(score))
            print("Guess another word")
            index = randint(0, 49)
            guess_this_word = words[index]
            guess_string = []
            guess_string.append("_")
            for _ in range(len(guess_this_word) - 1):
                guess_string.append(" _")
            print("".join(guess_string))
        guessed_letter = input("Guess a letter: ")
        
# main driver function for word guess game
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        # takes in file name as sys arg
        fp = sys.argv[1]
        # return file
        text_in = method1(fp)
        # find lexical diversty of text
        findLexicalDiversity(text_in)
        # process text and return list of processed tokens and nouns
        tokens, nouns = preprocessText(text_in)
        # return fifty most common nouns
        fifty_nouns = saveDictionary(tokens, nouns)
        # play word guessing game
        playGuessingGame(fifty_nouns)