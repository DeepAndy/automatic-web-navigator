'''
Initial Author: Austin Moore
Description: Provides interface for adding web pages and actions to perform
	in a queue.
'''

from selenium import webdriver

#driver = webdriver.Chrome(executable_path=
#				"/Users/am058613/Desktop/chromedriver")

web_queue = []

def add_web_queue(web_queue):
	web_name = "\0"

	while (web_name == "\0"):
		print

		try:
			web_name = str(raw_input("Enter website name: "))
		except:
			print("Please enter a string.")
	
	web_queue.append(web_name)

	print
	print("Added \"" + web_name + "\" to queue")

	return web_queue

def print_queue(web_queue):
	print
	for index in range(len(web_queue)):
		print(web_queue[index])

def menu():
	option = "\0"

	while (option == "\0"):
		print
		print("1. Add website to queue")
		print("2. Add action for all websites in queue")
		print("3. Print queue")
		print("4. Quit")
		print

		try:
			option = int(raw_input("Select an option: "))
		except:
			print("Please enter an integer.")

		menu_input(web_queue, option)

def menu_input(web_queue, option):
	if (option == 1):
		web_queue = add_web_queue(web_queue)
		menu()
	elif (option == 2):
		add_action_all()
		menu()
	elif (option == 3):
		print_queue(web_queue)
		menu()
	elif (option == 4):
		quit()

menu()

#driver.get("file:///Users/am058613/Documents/awn/example1.html")
