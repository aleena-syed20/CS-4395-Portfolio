import sys  # to get the system parameter
import os   # used by method 1  
import re   # used for regex
import pickle # used to save dict as oickle file

# Person class
class Person:
    # create Person object with specified name, id and phone number
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

# read and return file
def method1(filepath):

    # open and read file, skipping first line
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        skip_line = f.readline()
        text_in = f.read().splitlines()
    return text_in

# process text: split on comma and use capital case for name (first, middle, last)
# return processed text
def processText(text_in):
    # split on comma to get fields as text variables
    for i in range(len(text_in)):
        text_in[i] = text_in[i].split(',')
        sentence = text_in[i]
        # capitalize first name, last name and middle initial
        for j in range(2):
            sentence[j] = sentence[j].title()
        if (text_in[i][2].isupper() == 0):
            text_in[i][2] = text_in[i][2].upper()
        # If middle initial does not exist, use 'X'
        if (text_in[i][2] == ''):
            text_in[i][2] = 'X'
    return text_in
    
# use regex to modify ID if not in proper format
# return modified text
def modifyID(text_in):
    for i in range(len(text_in)):
        sentence = text_in[i]
        # if ID does not match format, ask user for new ID
        match= re.match("[A-Z][A-Z][0-9][0-9][0-9][0-9]", sentence[3])
        check_match = bool(match)
        # keep prompting for new ID if still invalid
        while (check_match == 0):
            print("ID invalid: " + sentence[3] + '\n')
            print("ID is two letters followed by four digits.\n")
            id = input("Please enter a valid id: ")
            text_in[i][3] = id
            sentence = text_in[i]
            match= re.match("[A-Z][A-Z][0-9][0-9][0-9][0-9]", sentence[3])
            check_match = bool(match)
    return text_in

# modify phone number if not in proper format
# return modified text
def modifyPhoneNumber(text_in):
    for i in range(len(text_in)):
        sentence = text_in[i]
        # if phone number does not match format, ask user for new number
        match= re.match("[\d]{3}-[\d]{3}-[\d]{4}", sentence[4])
        check_match = bool(match)
        # keep prompting for new number if still invalid
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
    # for each line in file, pass appropriate variables to create Person object
    for person in text_in:
        p = Person(person[0], person[1], person[2], person[3], person[4])
        # add person to dict if their ID has not been added
        if dict_person.get(person[3]) is None:
            dict_person[person[3]] = p
        else:
            print("Error - ID already exists")
    return dict_person

# save dictionary as pickle file and print list of employees
def savePickle(dict_person):
    pickle.dump(dict_person, open('dict.p', 'wb'))
    dict_in = pickle.load(open('dict.p', 'rb'))  # read binary
    # print employee list from pickle file
    print("Employee List: \n")
    for item in dict_in:
        dict_in[item].display()

# main function
if __name__ == '__main__':
    # if sys arg is not entered, prompt user for appropriate file name
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









