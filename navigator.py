'''
Initial Author: Austin Moore
Description: Provides interface for adding web pages and actions to perform
	in a queue.
'''

#from selenium import webdriver

#driver = webdriver.Chrome(executable_path=
#				"/Users/am058613/Desktop/chromedriver")

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
		menu(web_queue, action_queue, web_action_queue)
	else:
		print
		print("Invalid number.")
		add_action_all(web_queue, action_queue)

def add_action_all(web_queue, action_queue, web_action_queue):
	option = "\0"

	while (option == "\0"):
		print
		print("----------------------------------------------------")
		print("1. Connect to page in new tab")
		print("2. Back to menu")
		print("----------------------------------------------------")

		try:
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			add_action_all(web_queue, action_queue)

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
		print("Website: " + web_queue[index]),
		for index2 in range(len(action_queue)):
			print("    Action: " + action_queue[index2])

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
		print("4.  Save website queue (NOT IMPLEMENTED)")
		print("5.  Save action queue (NOT IMPLEMENTED)")
		print("6.  Save website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------")
		print("7.  Load website queue (NOT IMPLEMENTED)")
		print("8.  Load action queue (NOT IMPLEMENTED)")
		print("9.  Load website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------")
		print("10. Print website queue")
		print("11. Print action queue")
		print("12. Print website-action queue")
		print("----------------------------------------------------")
		print("13. Run website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------")
		print("14. Quit")
		print("----------------------------------------------------")

		try:
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
	elif (option == 14):
		print
		quit()
	else:
		print
		print("Invalid number.")
		menu(web_queue, action_queue, web_action_queue)

initialization()

#driver.get("file:///Users/am058613/Documents/awn/example1.html")
