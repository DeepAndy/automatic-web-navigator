import re

'''
Function: date_converter
Definition: Convert a string date to a string of numbers for Drupal
Parameters: date (string)
'''
def date_converter(date):
    date_list = date.split(', ')
    print(date_list)
    if (re.search(r'Jan[uary]?', date, re.IGNORECASE)):
        date = '01' + date[1] + date[2]
    elif (re.search(r'May[uary]?', date, re.IGNORECASE)):
        date = '05' + date_list[1] + date_list[2]

    print('date = ' + date)
