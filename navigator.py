# Initial Author: Austin Moore
# Description: Provides interface for adding websites and actions in a queue

from selenium import webdriver
import time
import re

def initialization():
	web_queue = []
	action_queue = []
	web_action_queue = 0
	menu(web_queue, action_queue, web_action_queue)

def add_web_queue(web_queue):
	web_name = ""
	while (web_name == ""):
		print
		web_name = raw_input("Enter website name: ")
	web_queue.append(web_name)
	print
	print("Added \"" + web_name + "\" to queue")
	return web_queue

def add_action_all_input(web_queue, action_queue, web_action_queue, option):
	if (option == 1):
		action_queue.append("connect")
		print
		print("Added \"connect\" to action queue")
		return action_queue
	elif (option == 2):
		print
		element_name = raw_input("Enter element name: ")
		action = "click`" + element_name
		attribute_name = ""
		while (attribute_name != "q"):
			print
			attribute_name = raw_input("Enter an attribute name (Type 'q' to stop entering attributes): ")
			if (attribute_name == "q"):
				action_queue.append(action)
				return action_queue
			else:
				print
				attribute_value = raw_input("Enter the attribute value: ")
				action += "`" + attribute_name + "`" + attribute_value
	elif (option == 3):
		print
		element_name = raw_input("Enter element name: ")
		action = "fill`" + element_name
		attribute_name = ""
		while (attribute_name != "q"):
			print
			attribute_name = raw_input("Enter an attribute name (Type 'q' to stop entering attributes): ")
			if (attribute_name == "q"):
				break
			else:
				print
				attribute_value = raw_input("Enter the attribute value: ")
				action += "`" + attribute_name + "`" + attribute_value
		print
		fill = raw_input("Enter your input: ")
		action += "`" + fill
		action_queue.append(action)
		return action_queue
	elif (option == 4):
		menu(web_queue, action_queue, web_action_queue)
	else:
		print
		print("Invalid number.")
		add_action_all(web_queue, action_queue, web_action_queue)

def add_action_all(web_queue, action_queue, web_action_queue):
	option = ""
	while (option == ""):
		print
		print("----------------------------------------------------")
		print("WARNING: MAKE SURE YOUR ACTION IS UNIQUE")
		print("         ACROSS ALL WEBSITES IN THE WEBSITE QUEUE")
		print("----------------------------------------------------")
		print("1. Connect to page in new tab")
		print("2. Click an element")
		print("3. Fill out a form")
		print("4. Back to menu")
		print("----------------------------------------------------")
		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			add_action_all(web_queue, action_queue, web_action_queue)
		action_queue = add_action_all_input(
			web_queue, action_queue, web_action_queue, option)
		return action_queue

def apply_action_queue_all(web_queue, action_queue, web_action_queue):
	if (len(web_queue) == 0 and len(action_queue) == 0):
		print
		print("The website queue is empty. Can not apply actions to no websites.")
		print("The action queue is empty. Can not apply any actions.")
		return
	elif (len(web_queue) == 0):
		print
		print("The website queue is empty. Can not apply actions to no websites.")
		return
	elif (len(action_queue) == 0):
		print
		print("The action queue is empty. Can not apply any actions.")
		return
	web_action_queue = []
	# Create the columns for our actions
	for index in range(len(web_queue)):
		web_action_queue.append([web_queue[index]])
		for action in action_queue:
			web_action_queue[index].append(action)
	print
	print("Applied action queue to website queue.")
	return web_action_queue

def insert_queue(queue, queue_type):
	if (queue_type != "web_action_queue"):
		if (queue_type == "web_queue"):
			if (len(queue) == 0):
				print
				print("The website queue is empty.")
				return
		elif (queue_type == "action_queue"):
			if (len(queue) == 0):
				print
				print("The action queue is empty.")
				return
		print
		for index in range(len(queue)):
			print("Website[" + str(index + 1) + "]: " + queue[index])
		option = ""
		while (option == ""):
			try:
				print
				option = int(raw_input("Enter the position to insert: "))
			except:
				print
				print("Not a number.")
				option = ""
		if (option <= len(queue) and option > 0):
			if (queue_type == "web_queue"):
				web_name = raw_input("Enter the website name: ")
				queue.insert(int(option - 1), web_name)
		else:
			print
			print("Invalid number.")
			insert_queue(queue, queue_type)

def insert_queue_menu(web_queue, action_queue, web_action_queue):
	option = ""
	while (option == ""):
		print
		print("----------------------------------------------------")
		print("1. Insert into website queue")
		print("2. Insert into action queue")
		print("3. Insert into website-action queue")
		print("4. Back")
		print("----------------------------------------------------")
		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			insert_queue_menu(web_queue, action_queue, web_action_queue)
		if (option == 1):
			queue_type = "web_queue"
			insert_queue(web_queue, queue_type)
		elif (option == 2):
			queue_type = "action_queue"
			insert_queue(action_queue, queue_type)
		elif (option == 3):
			queue_type = "web_action_queue"
			insert_queue(web_action_queue, queue_type)
		elif (option == 4):
			menu(web_queue, action_queue, web_action_queue)
		else:
			print
			print("Invalid number.")
			insert_queue_menu(web_queue, action_queue, web_action_queue)
	menu(web_queue, action_queue, web_action_queue)

def write_queue(queue_name, queue, queue_type):
	f = open(queue_name, "w")
	if (queue_type == "web_action_queue"):
		for index in range(len(queue)):
			for index2 in range(len(queue[index])):
				f.write(queue[index][index2] + "\n")
			if (index == len(queue) - 1):
				f.close()
				print
				print("Saved web queue to \"" + queue_name + "\"")
			else:
				f.write("\n")
	else:
		for name in queue:
			f.write(str(name) + "\n")
		print
		print("Saved web queue to \"" + queue_name + "\"")
		f.close()

def save_queue(queue, queue_type):
	exists = True
	answer = ""
	print
	queue_name = raw_input("Enter name of the queue: ")
	if (queue_type == "web_queue"):
		queue_name += ".wq"
		if (len(queue) == 0):
			print
			print("The website queue is empty.")
			return
	elif (queue_type == "action_queue"):
		queue_name += ".aq"
		if (len(queue) == 0):
			print
			print("The action queue is empty.")
			return
	elif (queue_type == "web_action_queue"):
		queue_name += ".waq"
		if (queue == 0):
			print
			print("The website-action queue is empty.")
			return
	try:
		open(queue_name)
		exists = True
	except:
		exists = False
	if (exists == True):
		print
		print("A file with that name already exists.")
		while (answer != "y" and answer != "n"):
			answer = raw_input("Would you like to overwrite \"" + queue_name + "\" (y or n): ")	
		if (answer == "y"):
			write_queue(queue_name, queue, queue_type)
		else:
			return
	else:
		write_queue(queue_name, queue, queue_type)

def load_queue(queue, queue_type):
	exists = True
	answer = ""
	print
	queue_name = raw_input("Enter name of the queue file: ")
	if (queue_type == "web_queue"):
		queue_name += ".wq"
	elif (queue_type == "action_queue"):
		queue_name += ".aq"
	elif (queue_type == "web_action_queue"):
		queue_name += ".waq"
	try:
		open(queue_name)
		exists = True
	except:
		exists = False
	if (exists == True):
		f = open(queue_name)
		lines = f.readlines()
		if (queue_type != "web_action_queue"):
			for line in lines:
				queue.append(line.replace("\n", ""))
		else:
			queue = [[]]
			# Create the columns for our actions
			index = 0
			for line in lines:
				if (line != "\n"):
					queue[index].append(line.replace("\n", ""))
				else:
					queue.append([])
					index += 1
					continue
		print
		print("\"" + queue_name + "\" has been loaded")
		return queue
	else:
		print
		print("A file of that name does not exist in this directory.")
		return queue

def print_web_queue(web_queue):
	if (len(web_queue) == 0):
		print
		print("The website queue is empty.")
		return
	print
	for web_name in web_queue:
		print("Website: " + web_name)

def print_action_queue(action_queue):
	if (len(action_queue) == 0):
		print
		print("The action queue is empty.")
		return
	print
	for action in action_queue:
		print("Action: " + action)

def print_web_action_queue(web_action_queue):
	if (web_action_queue == 0):
		print
		print("The website-action queue is empty.")
		return
	print
	first_time = True
	for index in range(len(web_action_queue)):
		print("Website: " + web_action_queue[index][0])
		for action in web_action_queue[index]:
			if (first_time == False):
				print("    Action: " + action)
			else:
				first_time = False
		first_time = True

def clear_web_queue(web_queue):
	web_queue = []
	print
	print("The website queue has been cleared.")
	return web_queue

def clear_action_queue(action_queue):
	action_queue = []
	print
	print("The action queue has been cleared.")
	return action_queue

def clear_web_action_queue(web_action_queue):
	web_action_queue = 0
	print
	print("The website-action queue has been cleared.")
	return web_action_queue

def run_web_action_queue(web_action_queue):
	xpath = ""
	key = -1
	if (web_action_queue == 0):
		print
		print("The website-action queue is empty.")
		return
	driver = webdriver.Chrome(executable_path="/Users/am058613/Desktop/chromedriver")
	web_check = True
	for index in range(len(web_action_queue)):
		first_time_connect = True
		for action in web_action_queue[index]:
			if (web_check == False):
				if (action == "connect"):
					if (index == 0):
						driver.get(web_action_queue[index][0])
					else:
						driver.execute_script("window.open('" + web_action_queue[index][0] + "');")

					time.sleep(2)
				elif (action.find("click") == 0):
					order = re.split(r'`', action)
					xpath += "//" + order[1]
					for index2 in range(2, len(order)):
						if (index2 % 2 == 0):
							xpath += "[@" + order[index2]
						else:
							xpath += "='" + order[index2] + "']"

					if (first_time_connect == True and key != index):
						driver.get(web_action_queue[index][0])
						time.sleep(2)
						key = index
						first_time_connect = False
					driver.find_element_by_xpath(xpath).click()
					xpath = ""
					time.sleep(2)
				elif (action.find("fill") == 0):
					order = re.split(r'`', action)
					xpath += "//" + order[1]

					for index2 in range(2, len(order) - 1):
						if (index2 % 2 == 0):
							xpath += "[@" + order[index2]
						else:
							xpath += "='" + order[index2] + "']"
					if (first_time_connect == True and key != index):
						driver.get(web_action_queue[index][0])
						time.sleep(2)
						key = index
						first_time_connect = False

					index2 += 1
					driver.find_element_by_xpath(xpath).send_keys(order[index2])
					xpath = ""
					time.sleep(2)
			else:
				web_check = False
		web_check = True
	driver.quit()

def save_queue_menu(web_queue, action_queue, web_action_queue):
	option = ""
	while (option == ""):
		print
		print("----------------------------------------------------")
		print("1. Save website queue")
		print("2. Save action queue")
		print("3. Save website-action queue")
		print("4. Back")
		print("----------------------------------------------------")
		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			save_queue_menu(web_queue, action_queue, web_action_queue)
		if (option == 1):
			queue_type = "web_queue"
			save_queue(web_queue, queue_type)
		elif (option == 2):
			queue_type = "action_queue"
			save_queue(action_queue, queue_type)
		elif (option == 3):
			queue_type = "web_action_queue"
			save_queue(web_action_queue, queue_type)
		elif (option == 4):
			menu(web_queue, action_queue, web_action_queue)
		else:
			print
			print("Invalid number.")
			save_queue_menu(web_queue, action_queue, web_action_queue)
	menu(web_queue, action_queue, web_action_queue)

def load_queue_menu(web_queue, action_queue, web_action_queue):
	option = ""
	while (option == ""):
		print
		print("----------------------------------------------------")
		print("1. Load website queue")
		print("2. Load action queue")
		print("3. Load website-action queue")
		print("4. Back")
		print("----------------------------------------------------")
		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			load_queue_menu(web_queue, action_queue, web_action_queue)
		if (option == 1):
			queue_type = "web_queue"
			web_queue = load_queue(web_queue, queue_type)
		elif (option == 2):
			queue_type = "action_queue"
			action_queue = load_queue(action_queue, queue_type)
		elif (option == 3):
			queue_type = "web_action_queue"
			web_action_queue = load_queue(web_action_queue, queue_type)
		elif (option == 4):
			menu(web_queue, action_queue, web_action_queue)
		else:
			print
			print("Invalid number.")
			load_queue_menu(web_queue, action_queue, web_action_queue)
	menu(web_queue, action_queue, web_action_queue)

def print_queue_menu(web_queue, action_queue, web_action_queue):
	option = ""
	while (option == ""):
		print
		print("----------------------------------------------------")
		print("1. Print website queue")
		print("2. Print action queue")
		print("3. Print website-action queue")
		print("4. Back")
		print("----------------------------------------------------")
		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			print_queue_menu(web_queue, action_queue, web_action_queue)
		if (option == 1):
			print_web_queue(web_queue)
		elif (option == 2):
			print_action_queue(action_queue)
			queue_type = "action_queue"
		elif (option == 3):
			print_web_action_queue(web_action_queue)
			queue_type = "web_action_queue"
		elif (option == 4):
			menu(web_queue, action_queue, web_action_queue)
		else:
			print
			print("Invalid number.")
			print_queue_menu(web_queue, action_queue, web_action_queue)
	menu(web_queue, action_queue, web_action_queue)

def clear_queue_menu(web_queue, action_queue, web_action_queue):
	option = ""
	while (option == ""):
		print
		print("----------------------------------------------------")
		print("1. Clear website queue")
		print("2. Clear action queue")
		print("3. Clear website-action queue")
		print("4. Back")
		print("----------------------------------------------------")
		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			clear_queue_menu(web_queue, action_queue, web_action_queue)
		if (option == 1):
			web_queue = clear_web_queue(web_queue)
		elif (option == 2):
			action_queue = clear_action_queue(action_queue)
			queue_type = "action_queue"
		elif (option == 3):
			web_action_queue = clear_web_action_queue(web_action_queue)
			queue_type = "web_action_queue"
		elif (option == 4):
			menu(web_queue, action_queue, web_action_queue)
		else:
			print
			print("Invalid number.")
			clear_queue_menu(web_queue, action_queue, web_action_queue)
	menu(web_queue, action_queue, web_action_queue)

def menu(web_queue, action_queue, web_action_queue):
	option = ""
	while (option == ""):
		print
		print("----------------------------------------------------")
		print("1. Add site to website queue")
		print("2. Add action to action queue")
		print("3. Apply action queue to all sites in website queue")
		print("4. Insert into a queue")
		print("5. Remove from queue (NOT IMPLEMENTED)")
		print("6. Save a queue")
		print("7. Load a queue")
		print("8. Print a queue")
		print("9. Clear a queue")
		print("10. Run website-action queue")
		print("11. Quit")
		print("----------------------------------------------------")
		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			menu(web_queue, action_queue, web_action_queue)
		if (option == 1):
			web_queue = add_web_queue(web_queue)
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 2):
			action_queue = add_action_all(
					web_queue, action_queue, web_action_queue)
			'''
			add_action_all() will redirect to add_action_all_input()
			which will require web_action_queue to call menu().
			This is why we need to add web_action_queue to this function
			'''
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 3):
			web_action_queue = apply_action_queue_all(
				web_queue, action_queue, web_action_queue)
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 4):
			insert_queue_menu(web_queue, action_queue, web_action_queue)
		elif (option == 6):
			save_queue_menu(web_queue, action_queue, web_action_queue)
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 7):
			load_queue_menu(web_queue, action_queue, web_action_queue)
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 8):
			print_queue_menu(web_queue, action_queue, web_action_queue)
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 9):
			clear_queue_menu(web_queue, action_queue, web_action_queue)
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 10):
			run_web_action_queue(web_action_queue)
			menu(web_queue, action_queue, web_action_queue)
		elif (option == 11):
			print
			quit()
		else:
			print
			print("Invalid number.")
			menu(web_queue, action_queue, web_action_queue)

initialization()
