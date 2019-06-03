import re

'''
Function: date_converter
Definition: Convert a string date to a string of numbers for Drupal
            Format is YYYY-MM-DD
Parameters: date (string)
'''
def date_converter(date):
    date = date.replace(',', '')
    date = date.replace('.', '')
    date_list = date.split(' ')

    if (int(date_list[1]) < 10):
        date_list[1] = '0' + date_list[1]

    if (re.search(r'Jan(uary)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-01-' + date_list[1]
    elif (re.search(r'Feb(ruary)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-02-' + date_list[1]
    elif (re.search(r'Mar(ch)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-03-' + date_list[1]
    elif (re.search(r'Apr(il)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-04-' + date_list[1]
    elif (re.search(r'May', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-05-' + date_list[1]
    elif (re.search(r'Jun(e)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-06-' + date_list[1]
    elif (re.search(r'Jul(y)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-07-' + date_list[1]
    elif (re.search(r'Aug(ust)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-08-' + date_list[1]
    elif (re.search(r'Sep(tember)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-09-' + date_list[1]
    elif (re.search(r'Oct(ober)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-10-' + date_list[1]
    elif (re.search(r'Nov(ember)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-11-' + date_list[1]
    elif (re.search(r'Dec(ember)?', date_list[0], re.IGNORECASE)):
        date = date_list[2] + '-12-' + date_list[1]

    return date
