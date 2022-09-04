import sys  # to get the system parameter
import os   # used by method 1  
import re
import pickle

# Person class
class Person:
    def __init__(self, last, first, mi, id_val, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id_val = id_val
        self.phone = phone

    # display employee information
    def display(self):
        msg = (
            f'Employee id: {self.id_val}\n'
            f'       {self.first} {self.mi} {self.last}\n'
            f'       {self.phone}'
        )
        print(msg)

# read in file 
def method1(filepath):

    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        skip_line = f.readline()
        text_in = f.read().splitlines()
    return text_in

# process text: split on comma and use capital case for name (first, middle, last)
def processText(text_in):
    for i in range(len(text_in)):
        text_in[i] = text_in[i].split(',')
        sentence = text_in[i]
        for j in range(2):
            sentence[j] = sentence[j].title()
        if (text_in[i][2].isupper() == 0):
            text_in[i][2] = text_in[i][2].upper()
    print(text_in)
    return text_in
    
# use regex to modify ID if not in proper format
def modifyID(text_in):
    for i in range(len(text_in)):
        sentence = text_in[i]
        match= re.match("[A-Z][A-Z][0-9][0-9][0-9][0-9]", sentence[3])
        check_match = bool(match)
        while (check_match == 0):
            print("ID invalid: " + sentence[3] + '\n')
            print("ID is two letters followed by four digits.\n")
            id = input("Please enter a valid id: ")
            text_in[i][3] = id
            sentence = text_in[i]
            match= re.match("[A-Z][A-Z][0-9][0-9][0-9][0-9]", sentence[3])
            check_match = bool(match)
    print(text_in)
    return text_in

# modify phone number if not in proper format
def modifyPhoneNumber(text_in):
    for i in range(len(text_in)):
        sentence = text_in[i]
        match= re.match("[\d]{3}-[\d]{3}-[\d]{4}", sentence[4])
        check_match = bool(match)
        while (check_match == 0):
            print("Phone: " + sentence[4] + " is invalid\n")
            print("Enter phone number in form 123-456-7890\n")
            pn = input("Enter phone number: ")
            text_in[i][4] = pn
            sentence = text_in[i]
            match= re.match("[\d]{3}-[\d]{3}-[\d]{4}", sentence[4])
            check_match = bool(match)
    return text_in

# save Person objects in dictionary
def savePerson(text_in):
    dict_person = {}
    for person in text_in:
        print(person)
        p = Person(person[0], person[1], person[2], person[3], person[4])
        if dict_person.get(person[3]) is None:
            dict_person[person[3]] = p
        else:
            print("Error - ID already exists")
    print(dict_person)
    return dict_person

# save dictionary as pickle file and print list of employees
def savePickle(dict_person):
    pickle.dump(dict_person, open('dict.p', 'wb'))
    dict_in = pickle.load(open('dict.p', 'rb'))  # read binary
    print("Employee List: \n")
    for item in dict_in:
        dict_in[item].display()

# main function
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        text_in = method1(fp)
        text_in = processText(text_in)
        text_in = modifyID(text_in)
        text_in = modifyPhoneNumber(text_in)
        dict_person = savePerson(text_in)
        savePickle(dict_person)









