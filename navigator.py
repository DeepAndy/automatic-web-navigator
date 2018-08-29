'''
Initial Author: Austin Moore
Description: Provides interface for adding web pages and actions to perform
	in a queue.
'''

from selenium import webdriver

#driver = webdriver.Chrome(executable_path=
#				"/Users/am058613/Desktop/chromedriver")

web_queue = []
action_queue = []
web_action_queue = [[]]

def add_web_queue(web_queue):
	web_name = "\0"

	while (web_name == "\0"):
		print

		web_name = raw_input("Enter website name: ")
	
	web_queue.append(web_name)

	print
	print("Added \"" + web_name + "\" to queue")

	return web_queue

def add_action_all_input(web_queue, action_queue, option):
	if (option == 1):
		action_queue.append("connect")
		print
		print("Added \"connect\" to action queue")
	elif (option == 2):
		menu()
	else:
		print
		print("Invalid number.")
		add_action_all(web_queue, action_queue)

def add_action_all(web_queue, action_queue):
	option = "\0"

	while (option == "\0"):
		print
		print("----------------------------------------------------------------------")
		print("1. Connect to page in new tab")
		print("2. Back to menu")
		print("----------------------------------------------------------------------")

		try:
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			add_action_all(web_queue, action_queue)

		add_action_all_input(web_queue, action_queue, option)

def print_web_queue(web_queue):
	print
	for web_name in web_queue:
		print(web_name)

def print_action_queue(action_queue):
	print
	for action in action_queue:
		print(action)

def menu():
	option = "\0"

	while (option == "\0"):
		print
		print("----------------------------------------------------------------------")
		print("1.  Add site to website queue")
		print("2.  Add action to action queue")
		print("----------------------------------------------------------------------")
		print("3.  Apply action queue to all sites in website queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------------------------")
		print("4.  Save website queue (NOT IMPLEMENTED)")
		print("5.  Save action queue (NOT IMPLEMENTED)")
		print("6.  Save website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------------------------")
		print("7.  Load website queue (NOT IMPLEMENTED)")
		print("8.  Load action queue (NOT IMPLEMENTED)")
		print("9.  Load website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------------------------")
		print("10. Print website queue")
		print("11. Print action queue")
		print("12. Print website-action queue (NOT IMPLEMENTED)")
		print("----------------------------------------------------------------------")
		print("13. Quit")
		print("----------------------------------------------------------------------")

		try:
			option = int(raw_input("Select an option: "))
		except:
			print
			print("Not a number.")
			menu()

		menu_input(web_queue, action_queue, option)

def menu_input(web_queue, action_queue, option):
	if (option == 1):
		web_queue = add_web_queue(web_queue)
		menu()
	elif (option == 2):
		action_queue = add_action_all(web_queue, action_queue)
		menu()
	elif (option == 10):
		print_web_queue(web_queue)
		menu()
	elif (option == 11):
		print_action_queue(action_queue)
		menu()
	elif (option == 13):
		print
		quit()
	else:
		print
		print("Invalid number.")
		menu()

menu()

#driver.get("file:///Users/am058613/Documents/awn/example1.html")
