# Importing libraries
import re
import random
from predict import predictDisease

# Function to check the probability of the message
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

# Function to return the answer based on user input
def check_all_messages(user_input):
    message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    highest_prob_list = {}
    

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)
    

    # Responses -------------------------------------------------------------------------------------------------------
    response(hello(),['hello','hi','hey','hai','smart','doc','hei','hay'], single_response=True)
    response(greetings(),['morning','mrng','afternoon','noon','nun','evening','eve','greetings'],single_response=True)
    response(bye(),['bye','goodbye','bubye','tata'], single_response=True)
    response(help(),['please','help','pls'], single_response=True)
    response(how(),['how','are','you','doing'], required_words=['how'])
    response(good(),['fine','good','great','better','awesome','nice'], single_response=True)
    response(thanks(),['thank','thanks'], single_response=True)
    response(yeah(),['yeah','sure','yes','definitely','yup', 'ok','okie'], single_response=True)
    response(pain(),['i','have','got','not','feeling','paining','sick','tired'], single_response=True)
    response(book_appointment(),['book','appointment', 'doctor','schedule'],single_response=True)
    
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')
    if highest_prob_list[best_match] < 1:
        return symptoms(user_input)
    else:
       return best_match

# Functions to respond back--------------------------------------------------------------------------------------------
def hello():
    hello=['Hi, How can I help you today?',
            'Hello there, How can I be of service?',
            'Hi, How can I help you?',
            'Hello, How can I help?',
            'Hey, How can I help?',
            'Hi. It\'s good to hear from you. How can I help?'
          ][
    random.randrange(6)]
    return hello

def greetings():
    greetings=['Greetings of the day! How are you doing?',
               'Nice to see you!',
               'Greetings of the day!',
               'Hi. It\'s good to hear from you. How can I help?',
               'Have a great day!',
               'Hey, How can I help?'
              ][
    random.randrange(6)]
    return greetings


def bye():
    bye=['Take care, See you!',
         'Have a nice day!',
         'Take care, bye!',
         'bye',
         'ta-ta',
         'goodbye'
        ][
    random.randrange(6)]
    return bye  
        
def help():
    help=['I\'m here to help you.',
          'I\'ll do my best.',
          'I\'ll do all I can.',
          'I\'m glad to help you.',
          'I\'m here to listen.',
          'I would love to help you.'    
         ][
    random.randrange(6)]
    return help

def how():
    how=['I\'m doing fine, and you?',
         'I\'m fine. You\'re very kind to ask, especially in these tempestous times.',
         'I\'m splendid, Thank you for asking.',
         'Great, thanks. What can I do for you?',
         'I\'m great. Thank you for asking.',
         'Awesome! What about you?'
        ][
    random.randrange(6)]
    return how

def good():
    good=['It\'s awesome being able to help.',
          'Great!',
          'It\'s good to hear.',
          'Cool.',
          'Cool, Is there anything else I can do?',
          'I\'m happy you\'re happy.'
         ][
    random.randrange(6)]
    return good
         
def thanks():
    thanks=['You\'re very welcome!',
            'I\'m honoured to serve.',
            'No worries, I\'m here to help.',
            'I\'m here to help.',
            'You\'re the best, I love helping you.',
            'Just doing my job.'
           ][
    random.randrange(6)]
    return thanks

def yeah():
    yeah=['Okie..',
          'Nice',
          'Ok',
          'Okay',
          'Cool',
          'Right!'
        ][
    random.randrange(6)]
    return yeah

def pain():
    pain=['That does not sound good. Could you please mention your symptoms?',
          'I\'m sorry to hear that. Could you please mention your symptoms?',
          'Could you please mention your symptoms?',
          'I\'m sorry. Could you please mention your symptoms?',
          'I can understand. Could you please mention your symptoms?',
          'Okie, I get it. Could you please mention your symptoms?'
        ][
    random.randrange(6)]
    return pain

def book_appointment():
    website="https://www.apollo247.com/specialties"
    return "Please go to this link to book an appointment: "+website


def symptoms(rawData):
    ans=predictDisease(rawData)
    return ans