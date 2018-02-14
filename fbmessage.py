from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sched, time, timeit
import random
import getpass


prompt = False

while prompt:
	userEmail = raw_input("Email:\n")
	userPass = getpass.getpass("Password\n")
	userQuantity = input("Number of Messages:\n")
	userTimeInterval = input("Time interval (Seconds):\n")
	userMessageType = raw_input("Please enter message type ['single' or 'multiple', without quotes]. \n")
	if userMessageType == 'single':
		userMessageQuantity = 1
		userMessage = raw_input("Enter Message: \n")
		userMessages = [userMessage]
		operation = True
	elif userMessageType == 'multiple':
		userMessageQuantity = input("How many messages?\n")
		userMessages = []
		for i in range(1, userMessageQuantity + 1):
			thisMessage = raw_input("Enter message " + str(i) + " of " + str(userMessageQuantity) + ":\n")
			userMessages.append(thisMessage)
		operation = True
	else:
		print("Invalid input.")
		operation = False
		input("Press ENTER to restart the program.\n")


	if operation:
		print "Please confirm:\n"
		print "Email: " + userEmail + "\n"
		print "Target user: " + userTarget + "\n"
		print "Message count: " + str(userQuantity) + "\n"
		print "Time interval: " + str(userTimeInterval) + "\n"
		print "Messages: \n"
		print "    " + "Number of distinct messages: " + str(userMessageQuantity) + "\n"
		for i in range(userMessageQuantity):
			print "    " + str(i + 1) + " " + userMessages[i] + "\n"
		print "Estimated completion time: " + str(userQuantity * userTimeInterval) + " seconds OR " + str((userQuantity * userTimeInterval)/60.0) + " minutes."
		proceed = raw_input("Proceed? y/n\n")
		if proceed == 'y':
			operation = True
			break;
		else:
			print "Operation aborted.\n"
			input("Press ENTER to restart the program.\n")
			operation = False

operation = True

if prompt == False:
	userPass = getpass.getpass("Password:\n")



if operation:
	print "Initializing..."

	with open('settings.txt') as s:
		for line in s:
			x = line.split(":")
			if x[0] == "EMAIL":
				userEmail = x[1]
			elif x[0] == "MSG_COUNT":
				userQuantity = int(x[1])
			elif x[0] == "TIME_INT":
				userTimeInterval = int(x[1])
			elif x[0] == "MESSAGE_BODY":
				userMessages = [x[1]]	

	with open('demo.txt') as f:
		content = f.readlines()
	content = [x.strip() for x in content]


	browser = webdriver.Chrome('chromedriver.exe')
	browser.maximize_window()

	print "Operation in progress."

	browser.get('http://www.facebook.com')
	emailElem = browser.find_element_by_id("email")
	emailElem.send_keys(userEmail)
	passElem = browser.find_element_by_id("pass")
	passElem.send_keys(userPass)
	passElem.send_keys(Keys.RETURN)
	for fbid in content:
		userTargetUrl = "http://www.facebook.com/messages/t/" + fbid
		browser.get(userTargetUrl)
		textAreaElem = browser.find_element_by_xpath("//div[@class='notranslate _5rpu' and @role='combobox']")
		for i in range(userQuantity):
			print "Sending message " + str(i + 1) + " of " + str(userQuantity) + "..."
			thisMessage = random.choice(userMessages)
			textAreaElem.send_keys(thisMessage)
			textAreaElem.send_keys(Keys.RETURN)
			time.sleep(userTimeInterval)
	print "Operation successful."