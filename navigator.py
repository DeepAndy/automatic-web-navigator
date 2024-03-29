'''
Author:         Austin Moore
Script Type:    Main Script
Description:    A queue system for queueing websites and specific actions to be
                performed on them
Python 3.7.2
'''

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import re
import configparser
import os
import sys
import importlib
import math

class queue:
    def __init__(self, web_queue, action_queue, web_action_queue):
        self.web_queue = web_queue
        self.action_queue = action_queue
        self.web_action_queue = web_action_queue

class web_driver:
    def __init__(self, driver_type, driver_path, chrome_profile, firefox_profile):
        self.driver_type = driver_type
        self.driver_path = driver_path
        self.chrome_profile = chrome_profile
        self.firefox_profile = firefox_profile

'''
Function:       load_last_queue()
Arguments:      list
Return Type:    void
Description:    Reads last_queue.txt and loads the web-action-queue that was
                saved there
'''
def load_last_queue(queues):
    web_queue_found = False
    action_queue_found = False
    web_action_queue_found = False

    web_queue_name = "last_web_queue.txt"
    action_queue_name = "last_action_queue.txt"
    web_action_queue_name = "last_web_action_queue.txt"

    try:
        f1 = open(web_queue_name, "r")
        web_queue_found = True
    except:
        print("No web queue used last")

    try:
        f2 = open(action_queue_name, "r")
        action_queue_found = True
    except:
        print("No action queue used last")

    try:
        f3 = open(web_action_queue_name, "r")
        web_action_queue_found = True
    except:
        print("No web action queue used last")

    if (web_queue_found == True):
        web_queue_text = f1.read()
        web_queue_text = web_queue_text.strip()
        f1.close()
        check = False

        if (not re.match(r"^\s*$", web_queue_text)):
            try:
                f = open(web_queue_text)
                check = True
            except:
                print()
                print("Not able to find \"" + web_queue_text + "\"")
                print("Will not load the file")

            if (check == True):
                lines = f.readlines()
                queues.web_queue = []

                for line in lines:
                    queues.web_queue.append(line.strip())

                print()
                print('"' + web_queue_text + '"' + " has been loaded automatically")

    if (action_queue_found == True):
        action_queue_text = f2.read()
        action_queue_text = action_queue_text.strip()
        f2.close()
        check = False

        if (not re.match(r"^\s*$", action_queue_text)):
            try:
                f = open(action_queue_text)
                check = True
            except:
                print()
                print("Not able to find \"" + action_queue_text + "\"")
                print("Will not load the file")

            if (check == True):
                lines = f.readlines()
                queues.action_queue = []

                for line in lines:
                    queues.action_queue.append(line.strip())

                print()
                print('"' + action_queue_text + '"' + " has been loaded automatically")

    if (web_action_queue_found == True):
        web_action_queue_text = f3.read()
        web_action_queue_text = web_action_queue_text.strip()
        f3.close()
        check = False

        if (not re.match(r"^\s*$", web_action_queue_text)):
            try:
                f = open(web_action_queue_text)
                check = True
            except:
                print()
                print("Not able to find \"" + action_queue_text + "\"")
                print("Will not load the file")

            if (check == True):
                lines = f.readlines()
                queues.web_action_queue = [[]]

                # Create the columns for our actions
                index = 0

                for line in lines:
                    if (line != "\n"):
                        queues.web_action_queue[index].append(line.replace("\n", ""))
                    else:
                        queues.web_action_queue.append([])
                        index += 1
                        continue

                print()
                print('"' + web_action_queue_text + '"' + " has been loaded automatically")

def initialization():
    queues = queue([], [], [[]])
    config = configparser.ConfigParser()
    config_file = "config.ini"
    complete_config = True

    try:
        config.read(config_file)
    except:
        print()
        print("Could not find the configuration file \"" + config_file + "\" or the file has no sections")
        print()
        quit()

    found_driver_section = False
    driver_section = "Driver"

    for section in config.sections():
        if (section == driver_section):
            found_driver_section = True

    if (found_driver_section == False):
        print()
        print("Could not find the \"" + driver_section + "\" section.")
        print("Make sure a \"[" + driver_section + "]\" section is included in \"" + config_file + "\".")
        print()
        quit()

    driver_option_type = "driver_type"
    driver_option_path = "driver_path"
    driver_option_chrome_profile = "chrome_profile"
    driver_option_firefox_profile = "firefox_profile"
    found_driver_type = False
    found_correct_driver_type = False
    found_driver_path = False
    found_chrome_profile = False
    found_firefox_profile = False

    for option in config.options(driver_section):
        if (option == driver_option_type):
            found_driver_type = True

            if (config.get(driver_section, driver_option_type) == "chrome" or config.get(driver_section, driver_option_type) == "firefox"):
                found_correct_driver_type = True
                driver_type = config.get(driver_section, driver_option_type)

        if (option == driver_option_path):
            found_driver_path = True
            driver_path = config.get(driver_section, driver_option_path)

        if (option == driver_option_chrome_profile):
            chrome_profile = config.get(driver_section, driver_option_chrome_profile)
        else:
            found_chrome_profile = True

        if (option == driver_option_firefox_profile):
            firefox_profile = config.get(driver_section, driver_option_firefox_profile)
        else:
            found_firefox_profile = True

    if (found_driver_type == False):
        print()
        print("Could not find the \"" + driver_option_type + "\" option.")
        print("Make sure a \"" + driver_option_type + "\" option is included under the \"[" + driver_section + "]\" section.")
        complete_config = False

    if (found_correct_driver_type == False):
        print()
        print("The \"" + driver_option_type + "\" value is either incorrect or the option is missing.")
        print("Make sure the value is a valid option.")
        complete_config = False

    if (found_driver_path == False):
        print()
        print("Could not find the \"" + driver_option_path + "\" option.")
        print("Make sure a \"" + driver_option_path + "\" option is included under the \"[" + driver_section + "]\" section.")
        complete_config = False

    if (found_chrome_profile == False):
        chrome_profile = ""

    if (found_firefox_profile == False):
        firefox_profile = ""

    if (complete_config == False):
        print()
        quit()
    else:
        the_driver = web_driver(driver_type, driver_path, chrome_profile, firefox_profile)

    load_last_queue(queues)
    menu(queues, the_driver)

def add_web_queue(queues):
    web_name = ""

    while (web_name == ""):
        print()
        web_name = input("Enter website name: ")

    queues.web_queue.append(web_name)
    print()
    print("Added \"" + web_name + "\" to queue")
    return queues.web_queue

def add_action(queues, the_driver, option, pos, pos2, from_web_action):

    if (option == 1):
        if (pos < 0):
            queues.action_queue.append("connect")
        else:
            if (from_web_action == False):
                queues.action_queue.insert(pos, "connect")
            else:
                queues.web_action_queue[pos].insert(pos2, "connect")

        print()
        print("Added \"connect\" to action queue")
        return queues.action_queue
    elif (option == 2):
        print()
        xpath = input("Enter xpath of element: ")
        action = "click`" + xpath

        if (pos < 0):
                queues.action_queue.append(action)
        else:
                if (from_web_action == False):
                        queues.action_queue.insert(pos, action)
                else:
                        queues.web_action_queue[pos].insert(pos2, action)

        print()
        print("Added element to action queue")
        return queues.action_queue
    elif (option == 3):
        print()
        xpath = input("Enter xpath of element: ")
        action = "fill`" + xpath
        print()
        fill = input("Enter your input: ")
        action += "`" + fill

        if (pos < 0):
            queues.action_queue.append(action)
        else:
            if (from_web_action == False):
                queues.action_queue.insert(pos, action)
            else:
                queues.web_action_queue[pos].insert(pos2, action)

            print()
            print("Added element to action queue")
            return queues.action_queue
    elif (option == 4):
        print()
        js_line = input("Enter line of JavaScript: ")
        action = "js_line`" + js_line

        if (pos < 0):
            queues.action_queue.append(action)
        else:
            if (from_web_action == False):
                queues.action_queue.insert(pos, action)
            else:
                queues.web_action_queue[pos].insert(pos2, action)

        print()
        print("Added JS line to action queue")
        return queues.action_queue
    elif (option == 5):
        print()
        dirs = os.listdir("javascript")
        for file in dirs:
            if (re.findall(r'[^\.].*?(\.js)$', str(file))):
                print(str(file.split(".js")[0]))

        print()
        exists = False

        while (exists == False):
            script = input("Enter name of the JavaScript file: ")
            script_file = "javascript/" + script + ".js"

            try:
                open(script_file)
                exists = True
            except:
                exists = False
                print()
                print("Could not find the script")

        action = "js_script`" + script

        if (pos < 0):
            queues.action_queue.append(action)
        else:
            if (from_web_action == False):
                queues.action_queue.insert(pos, action)
            else:
                queues.web_action_queue[pos].insert(pos2, action)

        print()
        print("Added \"" + script_file + "\" to action queue")
        return queues.action_queue
    elif (option == 6):
        print()
        dirs = os.listdir(".")
        for file in dirs:
            if (re.findall(r'[^\.].*?(\.py)$', str(file))):
                print(str(file.split(".py")[0]))

        print()
        exists = False

        while (exists == False):
            script = input("Enter name of the Python script: ")
            script_file = script + ".py"

            try:
                open(script_file)
                exists = True
            except:
                exists = False
                print()
                print("Could not find the script")

        action = "py_script`" + script

        if (pos < 0):
            queues.action_queue.append(action)
        else:
            if (from_web_action == False):
                queues.action_queue.insert(pos, action)
            else:
                queues.web_action_queue[pos].insert(pos2, action)

        print()
        print('Added "' + script_file + '" to the action queue')
        return queues.action_queue
    elif (option == 7):
        menu(queues, the_driver)
    else:
        print()
        print("Invalid number.")
        add_action_menu(queues, option, pos, pos2, from_web_action)

def add_action_menu(queues, the_driver, pos, pos2, from_web_action):
    option = ""

    while (option == ""):
        print()
        print("----------------------------------------------------")
        print("WARNING: MAKE SURE YOUR ACTION IS UNIQUE")
        print("----------------------------------------------------")
        print("1.  Connect to page in new tab")
        print("2.  Click an element")
        print("3.  Fill out a form")
        print("4.  Execute line of JavaScript")
        print("5.  Add JavaScript file")
        print("6.  Add Python script")
        print("7.  Back to menu")
        print("----------------------------------------------------")

        try:
            print()
            option = int(input("Select an option: "))
        except:
            print()
            print("Not a number.")
            add_action_menu(queues, the_driver, pos, pos2, from_web_action)

        queues.action_queue = add_action(queues, the_driver, option, pos, pos2, from_web_action)
        return queues.action_queue

def apply_action_queue_all(queues):
    if (len(queues.web_queue) == 0 and len(queues.action_queue) == 0):
        print()
        print("The website queue is empty. Can not apply actions to no websites.")
        print("The action queue is empty. Can not apply any actions.")
        return
    elif (len(queues.web_queue) == 0):
        print()
        print("The website queue is empty. Can not apply actions to no websites.")
        return
    elif (len(queues.action_queue) == 0):
        print()
        print("The action queue is empty. Can not apply any actions.")
        return

    queues.web_action_queue = []

    # Create the columns for our actions
    for index in range(len(queues.web_queue)):
        queues.web_action_queue.append([queues.web_queue[index]])
        for action in queues.action_queue:
            queues.web_action_queue[index].append(action)
    print()
    print("Applied action queue to website queue.")
    return queues.web_action_queue

def edit_print(queues, queue_type, edit_type):
    last_index_web = 0
    last_index_action = 0

    if (queue_type == "web_queue"):
        if (len(queues.web_queue) == 0):
            print()
            print("Website[1]: ")
        else:
            for index in range(len(queues.web_queue)):
                print("Website[" + str(index + 1) + "]: " + queues.web_queue[index])
                last_index = index + 2

            if (edit_type == "insert"):
                print("Website[" + str(last_index) + "]: ")
    elif (queue_type == "action_queue"):
        if (len(queues.action_queue) == 0):
            print()
            print("Action[1]: ")
        else:
            for index in range(len(queues.action_queue)):
                print("Action[" + str(index + 1) + "]: " + queues.action_queue[index])
                last_index = index + 2

            if (edit_type == "insert"):
                print("Action[" + str(last_index) + "]: ")
    elif (queue_type == "web_action_queue"):
        if (queues.web_action_queue == [[]]):
            print()
            print("Website[1]: ")
        else:
            for index in range(len(queues.web_action_queue)):
                print()
                print("Website[" + str(index + 1) + "]: " + queues.web_action_queue[index][0])
                last_index_web = index + 2

                for index2 in range(1, len(queues.web_action_queue[index])):
                    print("    Action[" + str(index2) + "]: " + queues.web_action_queue[index][index2])
                    last_index_action = index2 + 1

                if (len(queues.web_action_queue[index]) == 1):
                    print("    Action[1]: ")
                else:
                    if (edit_type == "insert"):
                        print("    Action[" + str(last_index_action) + "]: ")

            if (edit_type == "insert"):
                print()
                print("Website[" + str(last_index_web) + "]: ")

def edit_queue(queues, queue_type, edit_type, the_driver):
    if (queue_type == "web_queue"):
        edit_print(queues, queue_type, edit_type)
        option = ""

        while (option == ""):
            try:
                print()
                if (edit_type == "insert"):
                    option = int(input("Enter the position to insert: "))
                elif (edit_type == "remove"):
                    option = int(input("Enter the position to remove: "))
            except:
                option = ""
                print()
                print("Not a number.")
                edit_print(queues, queue_type, edit_type)
                continue

            if (option <= len(queues.web_queue) + 1 and option > 0):
                print()

                if (edit_type == "insert"):
                    web_name = input("Enter the website name: ")
                    queues.web_queue.insert(int(option - 1), web_name)
                elif (edit_type == "remove"):
                    try:
                        del queues.web_queue[option - 1]
                    except:
                        option = ""
                        print()
                        print("Invalid number.")
                        edit_print(queues, queue_type, edit_type)
                        continue
            else:
                option = ""
                print()
                print("Invalid number.")
                edit_print(queues, queue_type, edit_type)
                continue
    elif (queue_type == "action_queue"):
        edit_print(queues, queue_type, edit_type)
        option = ""

        while (option == ""):
            try:
                print()

                if (edit_type == "insert"):
                    option = int(input("Enter the position to insert: "))
                elif (edit_type == "remove"):
                    option = int(input("Enter the position to remove: "))
            except:
                option = ""
                print()
                print("Not a number.")
                edit_print(queues, queue_type, edit_type)
                continue

            if (option <= len(queues.action_queue) + 1 and option > 0):
                print()

                if (edit_type == "insert"):
                    add_action_menu(queues, the_driver, option - 1, -1, False)
                elif (edit_type == "remove"):
                    try:
                        del queues.action_queue[option - 1]
                    except:
                        option = ""
                        print()
                        print("Invalid number.")
                        edit_print(queues, queue_type, edit_type)
                        continue
            else:
                option = ""
                print()
                print("Invalid number.")
                edit_print(queues, queue_type, edit_type)
                continue
    elif (queue_type == "web_action_queue"):
        # Error checking
        option = ""

        while (option == ""):
            arg1 = -1
            arg2 = -1
            edit_print(queues, queue_type, edit_type)
            print()
            option = input("Enter the position to remove: ")
            options = re.split(r' ', option)

            if (len(options) > 2):
                option = ""
                print()
                print("Must take 1 or 2 arguments")
                continue
            try:
                arg1 = int(options[0])
            except:
                option = ""
                print()
                print("The first argument is not a number")
                continue

            if (len(options) == 2):
                try:
                    arg2 = int(options[1])
                except:
                    option = ""
                    print()
                    print("The second argument is not a number")
                    continue

            if (queues.web_action_queue == [[]]):
                if (arg1 > len(queues.web_action_queue) or arg1 < 1):
                    option = ""
                    print()
                    print("Invalid website position")
                    continue
            else:
                if (arg1 > (len(queues.web_action_queue) + 1) or arg1 < 1):
                    option = ""
                    print()
                    print("Invalid website position")
                    continue

            if (arg2 != -1):
                try:
                    queues.web_action_queue[arg1 - 1]
                except:
                    option = ""
                    print()
                    print("Invalid action position")
                    continue

                if (arg2 > len(queues.web_action_queue[arg1 - 1]) or arg1 < 1):
                    option = ""
                    print()
                    print("Invalid action position")
                    continue
        if (arg2 == -1):
            if (edit_type == "insert"):
                print()
                web_name = input("Enter the website name: ")

            if (queues.web_action_queue == [[]]):
                queues.web_action_queue[arg1 - 1].insert(0, web_name)
            else:
                if (edit_type == "insert"):
                    queues.web_action_queue.insert(arg1 - 1, [web_name])
                elif (edit_type == "remove"):
                    del queues.web_action_queue[arg1 - 1]
        else:
            if (edit_type == "insert"):
                add_action_menu(queues, the_driver, arg1 - 1, arg2, True)
            elif (edit_type == "remove"):
                try:
                    del queues.web_action_queue[arg1 - 1][arg2]
                except:
                    option = ""
                    print()
                    print("Invalid action position")
                    edit_queue(queues, queue_type, edit_type, the_driver)

def edit_queue_menu(queues, the_driver, edit_type):
    option = ""

    while (option == ""):
        if (edit_type == "insert"):
            print()
            print("----------------------------------------------------")
            print("1.  Insert into website queue")
            print("2.  Insert into action queue")
            print("3.  Insert into website-action queue")
            print("4.  Back")
            print("----------------------------------------------------")
        elif (edit_type == "remove"):
            print()
            print("----------------------------------------------------")
            print("1.  Remove from website queue")
            print("2.  Remove from action queue")
            print("3.  Remove from website-action queue")
            print("4.  Back")
            print("----------------------------------------------------")

        try:
            print()
            option = int(input("Select an option: "))
        except:
            print()
            print("Not a number.")
            edit_queue_menu(queues, the_driver, edit_type)

        if (option == 1):
            if (edit_type == "remove"):
                if (len(queues.web_queue) == 0):
                    print()
                    print("The website queue is empty")
                    edit_queue_menu(queues, the_driver, edit_type)

            edit_queue(queues, "web_queue", edit_type, the_driver)
        elif (option == 2):
            if (edit_type == "remove"):
                if (len(queues.action_queue) == 0):
                    print()
                    print("The action queue is empty")
                    edit_queue_menu(queues, the_driver, edit_type)

            edit_queue(queues, "action_queue", edit_type, the_driver)
        elif (option == 3):
            if (edit_type == "remove"):
                if (queues.web_action_queue == [[]]):
                    print()
                    print("The website-action queue is empty")
                    edit_queue_menu(queues, the_driver, edit_type)

            edit_queue(queues, "web_action_queue", edit_type, the_driver)
        elif (option == 4):
            menu(queues, the_driver)
        else:
            print()
            print("Invalid number.")
            edit_queue_menu(queues, the_driver, edit_type)

def write_queue(queue_name, queues, queue_type):
    f = open(queue_name, "w")
    if (queue_type == "web_action_queue"):
        for index in range(len(queues.web_action_queue)):
            for index2 in range(len(queues.web_action_queue[index])):
                f.write(queues.web_action_queue[index][index2] + "\n")
            if (index == len(queues.web_action_queue) - 1):
                f.close()
                print()
                print("Saved web queue to \"" + queue_name + "\"")
            else:
                f.write("\n")
    elif (queue_type == "web_queue"):
        for name in queues.web_queue:
            f.write(str(name) + "\n")
        print()
        print("Saved web queue to \"" + queue_name + "\"")
        f.close()
    elif (queue_type == "action_queue"):
        for name in queues.action_queue:
            f.write(str(name) + "\n")
        print()
        print("Saved web queue to \"" + queue_name + "\"")
        f.close()

'''
Function:       save_last_queue(queue_name, queue_type)
Arguments:      string, string
Return:         void
Description:    Saves the file name of the current web action queue loaded by
                this program
'''
def save_last_queue(queue_name, queue_type):
    web_queue_name = "last_web_queue.txt"
    action_queue_name = "last_action_queue.txt"
    web_action_queue_name = "last_web_action_queue.txt"

    if (queue_type == "web_queue"):
        f = open(web_queue_name, "w")
        f.write(queue_name + "\n")
    elif (queue_type == "action_queue"):
        f = open(action_queue_name, "w")
        f.write(queue_name + "\n")
    elif (queue_type == "web_action_queue"):
        f = open(web_action_queue_name, "w")
        f.write(queue_name + "\n")

def save_queue(queues, queue_type):
    exists = True
    answer = ""
    print()
    queue_name = input("Enter name of the queue: ")

    if (queue_type == "web_queue"):
        queue_name = "web-queues/" + queue_name + ".wq"
        if (len(queues.web_queue) == 0):
            print()
            print("The website queue is empty.")
            return
    elif (queue_type == "action_queue"):
        queue_name = "action-queues/" + queue_name + ".aq"
        if (len(queues.action_queue) == 0):
            print()
            print("The action queue is empty.")
            return
    elif (queue_type == "web_action_queue"):
        queue_name = "web-action-queues/" + queue_name + ".waq"
        if (queues.web_action_queue == [[]]):
            print()
            print("The website-action queue is empty.")
            return
    try:
        open(queue_name)
        exists = True
    except:
        exists = False

    if (exists == True):
        print()
        print("A file with that name already exists.")

        while (answer != "y" and answer != "n"):
            answer = input("Would you like to overwrite \"" + queue_name + "\" (y or n): ")

        if (answer == "y"):
            write_queue(queue_name, queues, queue_type)
            save_last_queue(queue_name, queue_type)
            print()
            print('"' + queue_name + '"'+ " will automatically be loaded the next time you launch this program.")
        else:
            return
    else:
        write_queue(queue_name, queues, queue_type)
        save_last_queue(queue_name, queue_type)
        print()
        print('"' + queue_name + '"'+ " will automatically be loaded the next time you launch this program.")

def load_queue(queues, queue_type):
    exists = True
    print()

    if (queue_type == "web_queue"):
        path = "web-queues/"
        print("Website Queues:")
    elif (queue_type == "action_queue"):
        path = "action-queues/"
        print("Action Queues:")
    elif (queue_type == "web_action_queue"):
        path = "web-action-queues/"
        print("Website-Action Queues:")

    dirs = os.listdir(path)

    for file in dirs:
        if (queue_type == "web_queue"):
            print(str(file.split(".wq")[0]))
        elif (queue_type == "action_queue"):
            print(str(file.split(".aq")[0]))
        elif (queue_type == "web_action_queue"):
            print(str(file.split(".waq")[0]))

    print()
    queue_name = input("Enter name of the queue file: ")

    if (queue_type == "web_queue"):
        queue_name = "web-queues/" + queue_name + ".wq"
    elif (queue_type == "action_queue"):
        queue_name = "action-queues/" + queue_name + ".aq"
    elif (queue_type == "web_action_queue"):
        queue_name = "web-action-queues/" + queue_name + ".waq"

    try:
        open(queue_name)
        exists = True
    except:
        exists = False

    if (exists == True):
        if (queue_type == "web_queue"):
            queues.web_queue = []
        elif (queue_type == "action_queue"):
            queues.action_queue = []

        f = open(queue_name)
        lines = f.readlines()

        if (queue_type != "web_action_queue"):
            for line in lines:
                if (queue_type == "web_queue"):
                    queues.web_queue.append(line.replace("\n", ""))
                elif (queue_type == "action_queue"):
                    queues.action_queue.append(line.replace("\n", ""))

            if (queue_type == "web_queue"):
                save_last_queue(queue_name, "web_queue")
            elif (queue_type == "action_queue"):
                save_last_queue(queue_name, "action_queue")
        else:
            queues.web_action_queue = [[]]
            # Create the columns for our actions
            index = 0

            for line in lines:
                if (line != "\n"):
                    queues.web_action_queue[index].append(line.replace("\n", ""))
                else:
                    queues.web_action_queue.append([])
                    index += 1
                    continue

            save_last_queue(queue_name, "web_action_queue")
        print()
        print("\"" + queue_name + "\" has been loaded")
        print()
        print('"' + queue_name + '"'+ " will automatically be loaded the next time you launch this program.")
    else:
        print()
        print("A file of that name does not exist in this directory.")

def print_queue(queues, queue_type):
    if (queue_type == "web_queue"):
        if (len(queues.web_queue) == 0):
            print()
            print("The website queue is empty.")
            return

        print()

        for web_name in queues.web_queue:
            print("Website: " + web_name)
    elif (queue_type == "action_queue"):
        if (len(queues.action_queue) == 0):
            print()
            print("The action queue is empty.")
            return

        print()

        for action in queues.action_queue:
            print("Action: " + action)
    elif (queue_type == "web_action_queue"):
        if (queues.web_action_queue == [[]]):
            print()
            print("The website-action queue is empty.")
            return

        print()
        first_time = True

        for index in range(len(queues.web_action_queue)):
            print("Website: " + queues.web_action_queue[index][0])

            for action in queues.web_action_queue[index]:
                if (first_time == False):
                    print("    Action: " + action)
                else:
                    first_time = False

            first_time = True

def clear_queue(queues, queue_type):
    print()

    if (queue_type == "web_queue"):
        queues.web_queue = []
        print("The website queue has been cleared.")
    elif (queue_type == "action_queue"):
        queues.action_queue = []
        print("The action queue has been cleared.")
    elif (queue_type == "web_action_queue"):
        queues.web_action_queue = [[]]
        print("The website-action queue has been cleared.")

def run_web_action_queue(queues, web_action_queue, the_driver):
    key = -1
    entries = len(web_action_queue)
    percent_complete = 0
    entries_complete = 0
    average_time = 0
    times = []

    if (web_action_queue == [[]]):
        print()
        print("The website-action queue is empty.")
        return
    if (the_driver.driver_type == "chrome"):
        try:
            if (re.match("^\s*$", the_driver.chrome_profile)):
                driver = webdriver.Chrome(executable_path=the_driver.driver_path)
            else:
                options = webdriver.ChromeOptions()
                options.add_argument("user-data-dir=" + the_driver.chrome_profile)
                driver = webdriver.Chrome(executable_path=the_driver.driver_path, options = options)
        except:
            print()
            print("Could not open the chromedriver")
            print("Check that the driver type and driver path and browser profile is correct in config.ini")
            print("These are the current driver settings:")
            print()
            print("driver_type = " + the_driver.driver_type)
            print("driver_path = " + the_driver.driver_path)
            print("chrome_profile = " + the_driver.chrome_profile)
            print("firefox_profile = " + the_driver.firefox_profile)
            print()
            print("It may also be possible that the set browser profile is already in use")
            print()
            menu(queues, the_driver)
    elif (the_driver.driver_type == "firefox"):
        try:
            if (re.match("^\s*$", the_driver.firefox_profile)):
                driver = webdriver.Firefox(executable_path=the_driver.driver_path)
            else:
                profile = webdriver.FirefoxProfile(the_driver.firefox_profile)
                driver = webdriver.Firefox(executable_path=the_driver.driver_path, firefox_profile=profile)

        except:
            print()
            print("Could not open the chromedriver")
            print("Check that the driver type and driver path and browser profile is correct in config.ini")
            print("These are the current driver settings:")
            print()
            print("driver_type = " + the_driver.driver_type)
            print("driver_path = " + the_driver.driver_path)
            print("chrome_profile = " + the_driver.chrome_profile)
            print("firefox_profile = " + the_driver.firefox_profile)
            print()
            print("It may also be possible that the set browser profile is already in use")
            print()
            menu(queues, the_driver)

    web_check = True
    time_left = 0
    time_left_seconds = 0
    time_left_minutes = 0
    time_left_hours = 0
    start_time = time.time()
    elapsed_time = 0
    elapsed_time_hours = 0
    elapsed_time_minutes = 0
    elapsed_time_seconds = 0
    print()

    for index in range(len(web_action_queue)):
        if (index != 0):
            if (len(times) > 30):
                times.pop(0)

            if (len(times) > 0):
                average_time = sum(times) / float(len(times))

            time_left = float(average_time) * (entries - entries_complete)
            elapsed_time = time.time() - start_time
            time_left_hours_exact = float(time_left) / float(3600)
            elapsed_time_hours_exact = float(elapsed_time) / float(3600)
            time_left_hours = math.floor(float(time_left_hours_exact))
            elapsed_time_hours = math.floor(float(elapsed_time_hours_exact))
            time_left_minutes_exact = (float(time_left_hours_exact) - float(time_left_hours)) * float(60)
            elapsed_time_minutes_exact = (float(elapsed_time_hours_exact) - float(elapsed_time_hours)) * float(60)
            time_left_minutes = math.floor(float(time_left_minutes_exact))
            elapsed_time_minutes = math.floor(float(elapsed_time_minutes_exact))
            time_left_seconds_exact = float(time_left_minutes_exact) - float(time_left_minutes)
            elapsed_time_seconds_exact = float(elapsed_time_minutes_exact) - float(elapsed_time_minutes)
            time_left_seconds = math.floor(float(time_left_seconds_exact * 60))
            elapsed_time_seconds = math.floor(float(elapsed_time_seconds_exact * 60))

        first_time_connect = True
        sys.stdout.write("\rElapsed: [" + str(int(elapsed_time_hours)) + "h " + str(int(elapsed_time_minutes)) + "m " + str(int(elapsed_time_seconds)) + "s]    " + "Remaining: [" + str(int(time_left_hours)) + "h " + str(int(time_left_minutes)) + "m " + str(int(time_left_seconds)) + "s]    [" + str(int(percent_complete)) + "%]    [" + str(entries_complete) + "/" + str(entries) + "]")
        sys.stdout.flush()
        cycle_start_time = time.time()

        for action in web_action_queue[index]:
            if (web_check == False):
                order = re.split('`', action)
                if (action == "connect"):
                    if (index == 0):
                        driver.get(web_action_queue[index][0])
                    else:
                        driver.execute_script("window.open('" + web_action_queue[index][0] + "');")
                elif (action.find("click") == 0):
                    xpath = order[len(order) - 1]

                    if (first_time_connect == True and key != index):
                        driver.get(web_action_queue[index][0])
                        key = index
                        first_time_connect = False

                    driver.find_element_by_xpath(xpath).click()
                elif (action.find("fill") == 0):
                    xpath = order[len(order) - 2]

                    if (first_time_connect == True and key != index):
                        driver.get(web_action_queue[index][0])
                        key = index
                        first_time_connect = False

                    driver.find_element_by_xpath(xpath).send_keys(order[len(order) - 1])
                elif (action.find("js_line") == 0):
                    driver.get(web_action_queue[index][0])
                    driver.execute_script(order[1])
                elif (action.find("js_script") == 0):
                    f = open("javascript/" + order[1] + ".js", "r+")
                    driver.get(web_action_queue[index][0])
                    driver.execute_script(f.read())
                elif (action.find("py_script") == 0):
                    import_module = order[len(order) - 1]
                    func = importlib.import_module(import_module).__getattribute__("script_main")
                    driver.get(web_action_queue[index][0])
                    func(driver, web_action_queue[index][0], index)
            else:
                web_check = False

        entries_complete += 1
        percent_complete = math.floor((float(entries_complete) / float(entries)) * 100)

        times.append(time.time() - cycle_start_time)

        web_check = True

    if (len(times) > 0):
        average_time = sum(times) / float(len(times))

    time_left = float(average_time) * (entries - entries_complete)
    elapsed_time = time.time() - start_time
    time_left_hours_exact = float(time_left) / float(3600)
    elapsed_time_hours_exact = float(elapsed_time) / float(3600)
    time_left_hours = math.floor(float(time_left_hours_exact))
    elapsed_time_hours = math.floor(float(elapsed_time_hours_exact))
    time_left_minutes_exact = (float(time_left_hours_exact) - float(time_left_hours)) * float(60)
    elapsed_time_minutes_exact = (float(elapsed_time_hours_exact) - float(elapsed_time_hours)) * float(60)
    time_left_minutes = math.floor(float(time_left_minutes_exact))
    elapsed_time_minutes = math.floor(float(elapsed_time_minutes_exact))
    time_left_seconds_exact = float(time_left_minutes_exact) - float(time_left_minutes)
    elapsed_time_seconds_exact = float(elapsed_time_minutes_exact) - float(elapsed_time_minutes)
    time_left_seconds = math.floor(float(time_left_seconds_exact * 60))
    elapsed_time_seconds = math.floor(float(elapsed_time_seconds_exact * 60))
    sys.stdout.write("\rElapsed: [" + str(int(elapsed_time_hours)) + "h " + str(int(elapsed_time_minutes)) + "m " + str(int(elapsed_time_seconds)) + "s]    " + "Remaining: [" + str(int(time_left_hours)) + "h " + str(int(time_left_minutes)) + "m " + str(int(time_left_seconds)) + "s]    [" + str(int(percent_complete)) + "%]    [" + str(entries_complete) + "/" + str(entries) + "]")
    sys.stdout.flush()
    print()

    driver.quit()

def save_queue_menu(queues, the_driver):
    option = ""
    while (option == ""):
        print()
        print("----------------------------------------------------")
        print("1.  Save website queue")
        print("2.  Save action queue")
        print("3.  Save website-action queue")
        print("4.  Back")
        print("----------------------------------------------------")
        try:
            print()
            option = int(input("Select an option: "))
        except:
            print()
            print("Not a number.")
            save_queue_menu(queues, the_driver)
        if (option == 1):
            save_queue(queues, "web_queue")
        elif (option == 2):
            save_queue(queues, "action_queue")
        elif (option == 3):
            save_queue(queues, "web_action_queue")
        elif (option == 4):
            menu(queues, the_driver)
        else:
            print()
            print("Invalid number.")
            save_queue_menu(queues, the_driver)
        menu(queues, the_driver)

def load_queue_menu(queues, the_driver):
    option = ""
    while (option == ""):
        print()
        print("----------------------------------------------------")
        print("1.  Load website queue")
        print("2.  Load action queue")
        print("3.  Load website-action queue")
        print("4.  Back")
        print("----------------------------------------------------")
        try:
            print()
            option = int(input("Select an option: "))
        except:
            print()
            print("Not a number.")
            load_queue_menu(queues, the_driver)
        if (option == 1):
            load_queue(queues, "web_queue")
        elif (option == 2):
            load_queue(queues, "action_queue")
        elif (option == 3):
            load_queue(queues, "web_action_queue")
        elif (option == 4):
            menu(queues, the_driver)
        else:
            print()
            print("Invalid number.")
            load_queue_menu(queues, the_driver)
        menu(queues, the_driver)

def print_queue_menu(queues, the_driver):
    option = ""
    while (option == ""):
        print()
        print("----------------------------------------------------")
        print("1.  Print website queue")
        print("2.  Print action queue")
        print("3.  Print website-action queue")
        print("4.  Back")
        print("----------------------------------------------------")
        try:
            print()
            option = int(input("Select an option: "))
        except:
            print()
            print("Not a number.")
            print_queue_menu(queues, the_driver)
        if (option == 1):
            print_queue(queues, "web_queue")
        elif (option == 2):
            print_queue(queues, "action_queue")
        elif (option == 3):
            print_queue(queues, "web_action_queue")
        elif (option == 4):
            menu(queues, the_driver)
        else:
            print()
            print("Invalid number.")
            print_queue_menu(queues, the_driver)
        menu(queues, the_driver)

def clear_queue_menu(queues, the_driver):
    option = ""
    while (option == ""):
        print()
        print("----------------------------------------------------")
        print("1.  Clear website queue")
        print("2.  Clear action queue")
        print("3.  Clear website-action queue")
        print("4.  Back")
        print("----------------------------------------------------")
        try:
            print()
            option = int(input("Select an option: "))
        except:
            print()
            print("Not a number.")
            clear_queue_menu(queues, the_driver)
        if (option == 1):
            clear_queue(queues, "web_queue")
        elif (option == 2):
            clear_queue(queues, "action_queue")
        elif (option == 3):
            clear_queue(queues, "web_action_queue")
        elif (option == 4):
            menu(queues, the_driver)
        else:
            print()
            print("Invalid number.")
            clear_queue_menu(queues, the_driver)
        menu(queues, the_driver)

def menu(queues, the_driver):
    option = ""
    while (option == ""):
        print()
        print("----------------------------------------------------")
        print("1.  Add site to website queue")
        print("2.  Add action to action queue")
        print("3.  Apply action queue to all sites in website queue")
        print("4.  Insert into a queue")
        print("5.  Remove from a queue")
        print("6.  Save a queue")
        print("7.  Load a queue")
        print("8.  Clear a queue")
        print("9.  Print a queue")
        print("10. Run website-action queue")
        print("11. Quit")
        print("----------------------------------------------------")
        try:
            print()
            option = int(input("Select an option: "))
        except:
            print()
            print("Not a number.")
            menu(queues, the_driver)
        if (option == 1):
            queues.web_queue = add_web_queue(queues)
            menu(queues, the_driver)
        elif (option == 2):
            queues.action_queue = add_action_menu(queues, the_driver, -1, -1, False)
            menu(queues, the_driver)
        elif (option == 3):
            queues.web_action_queue = apply_action_queue_all(queues)
            menu(queues, the_driver)
        elif (option == 4):
            edit_queue_menu(queues, the_driver, "insert")
            menu(queues, the_driver)
        elif (option == 5):
            edit_queue_menu(queues, the_driver, "remove")
            menu(queues, the_driver)
        elif (option == 6):
            save_queue_menu(queues, the_driver)
            menu(queues, the_driver)
        elif (option == 7):
            load_queue_menu(queues, the_driver)
            menu(queues, the_driver)
        elif (option == 8):
            clear_queue_menu(queues, the_driver)
            menu(queues, the_driver)
        elif (option == 9):
            print_queue_menu(queues, the_driver)
            menu(queues, the_driver)
        elif (option == 10):
            run_web_action_queue(queues, queues.web_action_queue, the_driver)
            menu(queues, the_driver)
        elif (option == 11):
            print()
            quit()
        else:
            print()
            print("Invalid number.")
            menu(queues, the_driver)

initialization()
