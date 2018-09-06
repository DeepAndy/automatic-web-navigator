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
	web_name = "\0"

	while (web_name == "\0"):
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
		attribute_name = "\0"
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
		attribute_name = "\0"
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
	option = "\0"

	while (option == "\0"):
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
	for index in range(len(web_queue)):
		column = []
		for index2 in range(len(action_queue)):
			column.append(0)
		web_action_queue.append(column)

	for index in range(len(web_queue)):
		for index2 in range(len(action_queue)):
			web_action_queue[index][index2] = action_queue[index2]

	print
	print("Applied action queue to website queue.")

	return web_action_queue

def write_queue(queue_name, queue):
	f = open(queue_name, "w")

	for name in queue:
		f.write(name + "\n")

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
	elif (queue_type == "action_queue"):
		queue_name += ".aq"

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
			write_queue(queue_name, queue)
		else:
			return
	else:
		write_queue(queue_name, queue)

def load_queue(queue, queue_type):
	exists = True
	answer = ""

	print
	queue_name = raw_input("Enter name of the queue file (include file extension): ")

	try:
		open(queue_name)
		exists = True
	except:
		exists = False

	if (exists == True):
		f = open(queue_name)
		lines = f.readlines()
		for line in lines:
			queue.append(line.replace("\n", ""))
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

def print_web_action_queue(web_queue, action_queue, web_action_queue):
	if (web_action_queue == 0):
		print
		print("The website-action queue is empty.")
		return
	print
	for index in range(len(web_queue)):
		print("Website: " + web_queue[index])
		for index2 in range(len(action_queue)):
			print("    Action: " + action_queue[index2])

def run_web_action_queue(web_queue, action_queue, web_action_queue):
	xpath = ""
	key = -1

	if (web_action_queue == 0):
		print
		print("The website-action queue is empty.")
		return

	driver = webdriver.Chrome(executable_path="/Users/am058613/Desktop/chromedriver")

	for index in range(len(web_queue)):
		first_time_connect = True
		for index2 in range(len(action_queue)):
			if (web_action_queue[index][index2] == "connect"):
				if (index == 0):
					driver.get(web_queue[index])
				else:
					driver.execute_script("window.open('" + web_queue[index] + "');")

				time.sleep(2)
			elif (web_action_queue[index][index2].find("click") == 0):
				order = re.split(r'`', web_action_queue[index][index2])
				xpath += "//" + order[1]

				for index3 in range(2, len(order)):
					if (index3 % 2 == 0):
						xpath += "[@" + order[index3]
					else:
						xpath += "='" + order[index3] + "']"

				if (first_time_connect == True and key != index):
					driver.get(web_queue[index])
					time.sleep(2)
					key = index
					first_time_connect = False

				driver.find_element_by_xpath(xpath).click()
				xpath = ""

				time.sleep(2)
			elif (web_action_queue[index][index2].find("fill") == 0):
				order = re.split(r'`', web_action_queue[index][index2])
				xpath += "//" + order[1]

				for index3 in range(2, len(order) - 1):
					if (index3 % 2 == 0):
						xpath += "[@" + order[index3]
					else:
						xpath += "='" + order[index3] + "']"

				if (first_time_connect == True and key != index):
					driver.get(web_queue[index])
					time.sleep(2)
					key = index
					first_time_connect = False

				index3 += 1
				driver.find_element_by_xpath(xpath).send_keys(order[index3])
				xpath = ""

				time.sleep(2)

	driver.quit()

def menu(web_queue, action_queue, web_action_queue):
	option = "\0"

	while (option == "\0"):
		print
		print("----------------------------------------------------")
		print("1.  Add site to website queue")
		print("2.  Add action to action queue")
		print("----------------------------------------------------")
		print("3.  Apply action queue to all sites in website queue")
		print("----------------------------------------------------")
		print("4.  Save website queue")
		print("5.  Save action queue")
		print("6.  Save website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------")
		print("7.  Load website queue")
		print("8.  Load action queue")
		print("9.  Load website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------")
		print("10. Print website queue")
		print("11. Print action queue")
		print("12. Print website-action queue")
		print("----------------------------------------------------")
		print("13. Run website-action queue")
		print("----------------------------------------------------")
		print("14. Quit")
		print("----------------------------------------------------")

		try:
			print
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			menu(web_queue, action_queue, web_action_queue)

		menu_input(web_queue, action_queue, web_action_queue, option)

def menu_input(web_queue, action_queue, web_action_queue, option):
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
		queue_type = "web_queue"
		save_queue(web_queue, queue_type)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 5):
		queue_type = "action_queue"
		save_queue(action_queue, queue_type)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 7):
		queue_type = "web_queue"
		web_queue = load_queue(web_queue, queue_type)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 8):
		queue_type = "action_queue"
		action_queue = load_queue(action_queue, queue_type)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 10):
		print_web_queue(web_queue)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 11):
		print_action_queue(action_queue)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 12):
		print_web_action_queue(
			web_queue, action_queue, web_action_queue)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 13):
		run_web_action_queue(
			web_queue, action_queue, web_action_queue)
		menu(web_queue, action_queue, web_action_queue)
	elif (option == 14):
		print
		quit()
	else:
		print
		print("Invalid number.")
		menu(web_queue, action_queue, web_action_queue)

initialization()
