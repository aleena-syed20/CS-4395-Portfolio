# Aleena Syed, Norah Khan
# CS 4395.001
# Chatbot Project

import json
import random
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

# clean text
def clean_string(text):
    # remove punctuation
    text = ''.join([word for word in text if word not in string.punctuation])
    # lowercase sentence
    text = text.lower()
    # remove stopwords
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

# load json file
def load_json():
    f = open('intents.json')
    data = json.load(f)
    return data

# greeting 
def greeting(data):
    greetings_list = []
    # obtain user greeting
    user_greeting = input()
    # if user says goodbye, return null list
    if user_greeting == "Goodbye":
        responses = data['intents'][1]['responses']
        print(random.choice(responses))
        return greetings_list
    # else, save greeting with greeting patterns and return list
    else:
        greetings_list.append(user_greeting)
        patterns = data['intents'][0]['patterns']
        for i in patterns:
            greetings_list.append(i)
        return greetings_list

# opening questions
def opening_questions(data):
    questions_list = []
    # get user input for question
    user_question = input()
    # if user says goodbye, return null list
    if user_question == "Goodbye":
        responses = data['intents'][1]['responses']
        print(random.choice(responses))
        return questions_list
    # else, save question in list of question patterns
    else:
        questions_list.append(user_question)
        patterns = data['intents'][2]['patterns']
        for i in patterns:
            questions_list.append(i)
        return questions_list

# year in school questions
def year(data, user_name, userinfo, user_dict):
    years_list = []
    # get user's year in school
    user_year = input()
    key, value = 'year', user_year

    # if user does not already exist in dictionary, save their year
    if key in userinfo and value != userinfo[key]: 
        user_dict['year'] = user_year

    # if user says goodbye, return null list
    if user_year == "Goodbye":
        responses = data['intents'][1]['responses']
        print(random.choice(responses))
        return years_list
    # else, save response with year patterns
    else:
        years_list.append(user_year)
        patterns = data['intents'][3]['patterns']
        for i in patterns:
            years_list.append(i)
        return years_list

# year in school questions
def advising_response(data):
    ans_list = []
    # get user response for rating advising
    user_ans = input()
    ans_list.append(user_ans)
    patterns = data['intents'][5]['patterns']
    for i in patterns:
        ans_list.append(i)
    return ans_list

# graduation questions
def graduation(data):
    graduation_list = []
    # get user's response to graduation question
    user_grad = input()
    # if user enters goodbye, return null list
    if user_grad == "Goodbye":
        responses = data['intents'][1]['responses']
        print(random.choice(responses))
        return graduation_list
    # else, save response with othre graduation response patterns
    else:
        graduation_list.append(user_grad)
        patterns = data['intents'][4]['patterns']
        for i in patterns:
            graduation_list.append(i)
        return graduation_list

# vectorizer
def vectorizer(cleaned_text):
    # transforms sentences into vectors
    vectorizer = CountVectorizer().fit_transform(cleaned_text)
    # transforms vectors to an array
    vectors = vectorizer.toarray()
    return vectors

# calculate cosine similarity between two vectors
def csim(vectors):
    csim = cosine_similarity(vectors)
    return csim

# calculate cosine similarity
def cosine_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]

# ask and respond to intro questions
def intro(user_name):
    data = load_json()
    # if user said goodbye, end program
    greetings_list = greeting(data)
    if not greetings_list:
        exit()
    # process response patterns
    cleaned_text = list(map(clean_string, greetings_list))
    # transform them to vectors
    vectors = vectorizer(cleaned_text)
    # calculate similarity between user response and patterns chatbot is aware of
    similar = False
    for x in range(0, 3):
        for y in range(0, 3):
            if cosine_sim_vectors(vectors[x], vectors[y]) == 1 and x != y:
                similar = True
    # if user response is similar enough, chatbot will generate a response
    if similar == True:
        responses = data['intents'][0]['responses']
        print(random.choice(responses) + " " + user_name)

# ask and respond to starter questions
def start_questions():
    data = load_json()
    questions_list = opening_questions(data)
    # if user said goodbye, end program
    if not questions_list:
        exit()
    # process response patterns
    cleaned_text = list(map(clean_string, questions_list))
    # transform them to vectors
    vectors = vectorizer(cleaned_text)
    # calculate similarity between user response and patterns chatbot is aware of
    similar = False
    if cosine_sim_vectors(vectors[0], vectors[1]) >= 0.20:
        similar = True
    # if user response is similar enough, chatbot will generate a response
    if similar == True:
        responses = data['intents'][2]['responses']
        print(responses[0])

# ask and respond to year in school questions
def year_questions(user_name, userinfo, user_dict):
    data = load_json()
    years_list = year(data, user_name, userinfo, user_dict)
    # if user said goodbye, end program
    if not years_list:
        exit()
    # process response patterns
    cleaned_text = list(map(clean_string, years_list))
    # transform them to vectors
    vectors = vectorizer(cleaned_text)
    # calculate similarity between user response and patterns chatbot is aware of
    similar = False
    for x in range(0, 5):
        for y in range(0, 5):
            if cosine_sim_vectors(vectors[x], vectors[y]) >= 0.20 and x != y:
                similar = True
    # if user response is similar enough, chatbot will generate a response
    if similar == True:
        responses = data['intents'][3]['responses']
        if 'freshman' in cleaned_text[0]:
            print(responses[0])
        elif 'sophomore' in cleaned_text[0]:
            print(responses[1])
        elif 'junior' in cleaned_text[0]:
            print(responses[2])
        else:
            print(responses[3])

# ask and respond to favorite class questions
def favoriteclass_questions():
    data = load_json()
    responses = data['intents'][4]['responses']
    print(responses[0])

# ask and respond to graduation questions
def advising():
    data = load_json()
    adv_list = advising_response(data)
    # if user said goodbye, end program
    if not adv_list:
        exit()
    # process response patterns
    cleaned_text = list(map(clean_string, adv_list))
    # transform them to vectors
    vectors = vectorizer(cleaned_text)
    # calculate similarity between user response and patterns chatbot is aware of
    similar = False
    for x in range(0, 6):
        for y in range(0, 6):
            if cosine_sim_vectors(vectors[x], vectors[y]) == 1 and x != y:
                similar = True
    # if user response is similar enough, chatbot will generate a response
    if similar == True:
        responses = data['intents'][5]['responses']
        if 'very bad' in cleaned_text[0]:
            print(responses[0])
        elif 'bad' in cleaned_text[0]:
            print(responses[1])
        elif 'okay' in cleaned_text[0]:
            print(responses[2])
        elif 'good' in cleaned_text[0]:
            print(responses[3])
        else:
            print(responses[4])

# ask and respond to graduation questions
def graduation_questions():
    data = load_json()
    responses = data['intents'][6]['responses']
    
    print(responses[0])

# main program
def main():
    # load info from .json file
    f = open('userinfo.json')
    userinfo = json.load(f)
    # greet user
    print("Hello, I am the CS degree advisor chatbot! Before we begin, please enter your first name. Then, say hello to the chatbot to get started.")
    # get user's name
    user_name = input()
    key, value = 'user_name', user_name
    user_dict = ''
    present = False

    # if dict contains people already (which it will based on example user models), iterate through
    # to see if user already exists
    if len(userinfo) != 0:
        for i in range(len(userinfo)):
            # if user already exists, save its dict
            if key in userinfo[i] and value == userinfo[i][key]: 
                present = True
                user_dict = userinfo[i]
                break
            # if not found, create new user dict
            else:
                user_dict = {'user_name': '', 'year': '', 'utd_exp': '', 'favorite_class': ''}
                user_dict['user_name'] = user_name
    else:
        user_dict = {'user_name': '', 'year': '', 'utd_exp': '', 'favorite_class': ''}
        user_dict['user_name'] = user_name
    
    # Welcome user
    intro(user_name)
    print("Please ask this question to kickstart our chatbot: " + "1. ask about picking classes")
    # starter questions
    start_questions()
    # year in school questions
    year_questions(user_name, userinfo, user_dict)
    # if user did not exist, ask about their favorite class
    if present == False:  
        print("What is your favorite class at utd?")
        fav_class = input()
        user_dict['favorite_class'] = fav_class
        favoriteclass_questions()
    # if user did already exist, respond with their favorite class
    else:
        print("I remember your favorite class is ", user_dict['favorite_class'])
    # ask about advising experience
    print("How has your experience been with CS advising: very bad, bad, okay, good, or very good?")
    advising()
    # ask about if they need help with graduation 
    print("Are you needing assistance with graduation today?")
    grad = input()
    if grad == 'Yes' or grad == 'yes':
        graduation_questions()
        print("That's all I can help with you today, see you next time!")
    else:
        print("That's all I can help with you today, see you next time!")
    # append dict to previous dicts in json file if new 
    if present == False:
        userinfo.append(user_dict)
    # save dict to json file
    with open("userinfo.json", "w") as outfile:
        #save new persons/updated info to json file
        json.dump(userinfo, outfile)

main()