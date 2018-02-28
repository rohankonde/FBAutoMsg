from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import sys
import os, datetime
import sched, time, timeit
import random
import getpass
import json
import Tkinter as tk

SETTINGS_SCHEMA = {'EMAIL', 'MSG_COUNT', 'MSG_BODY', 'TIME_INT'}

class MessengerBot:
	settings = {}
	recipients = None
	browser = None
	userPass = None
	password = None

	def __init__(self, settings):
		self.settings = self.get_settings(settings)
		print(self.settings)
		self.open_session()
		try:
			with open('../data/friends.json', 'r') as fp:
				self.recipients = json.load(fp)
		except(OSError, IOError) as e:
			print "friends.json file not found. Creating new friends.json"
			self.recipients = self.scrape_1st_degrees()

	def get_settings(self, filename):
		settings = {}
		def set_settings():
			settings["EMAIL"] = e1.get()
			self.password = e2.get()
			settings["TIME_INT"] = e3.get()
			settings["MSG_BODY"] = e4.get("1.0",'end-1c')
			settings["MSG_COUNT"] = 1
			master.destroy()

			if "Colton" not in settings["MSG_BODY"]:
				sys.exit()
			if "Mehraz" not in settings["MSG_BODY"]:
				sys.exit()

		master = tk.Tk()
		tk.Label(master, text="Email").grid(row=0)
		tk.Label(master, text="Password").grid(row=1)
		tk.Label(master, text="Time Interval").grid(row=2)
		tk.Label(master, text="Message").grid(row=3)

		e1 = tk.Entry(master, width=80)
		e2 = tk.Entry(master, show="*", width=80)
		e3 = tk.Entry(master, width=80)
		e4 = tk.Text(master, height=20)

		e1.grid(row=0, column=1)
		e2.grid(row=1, column=1)
		e3.grid(row=2, column=1)
		e4.grid(row=3, column=1)

		tk.Button(master, text='Submit', command=set_settings).grid(row=4, column=0, sticky=tk.W, pady=4)

		tk.mainloop()

		with open('../data/settings.txt', 'w') as fp:
			json.dump(settings, fp)

		return settings


	def get_recipients(self, filename):
		return recipients

	def update_recipients(self):
		print("TEST")
		#update recipients from file
		with open('../data/friends.json', 'r') as fp:
				self.recipients = json.load(fp)
		print(self.recipients)

	def open_session(self):
		userPass = self.password

		print "Initializing Facebook Instance"
		self.browser = webdriver.Chrome('./chromedriver.exe')
		self.browser.maximize_window()
		self.browser.get('http://www.facebook.com')
		emailElem = self.browser.find_element_by_id("email")
		emailElem.send_keys(self.settings['EMAIL'])
		passElem = self.browser.find_element_by_id("pass")
		passElem.send_keys(userPass)
		passElem.send_keys(Keys.RETURN)
		return

	def run(self):
		for fbid in self.recipients:
			userTargetUrl = "http://www.facebook.com/messages/t/" + fbid
			userQuantity = self.settings['MSG_COUNT']
			userMessage = self.settings['MSG_BODY']
			userTimeInterval = self.settings['TIME_INT']

			userMessage = userMessage.replace("###", self.recipients[fbid].split()[0])

			self.browser.get(userTargetUrl)
			textAreaElem = self.browser.find_element_by_xpath("//div[@class='notranslate _5rpu' and @role='combobox']")
			
			for i in range(userQuantity):
				print "Sending message " + str(i + 1) + " of " + str(userQuantity) + "..."
				textAreaElem.send_keys(userMessage)
				textAreaElem.send_keys(Keys.RETURN)
				time.sleep(float(userTimeInterval))
		print "Operation successful."

	def scroll_to_bottom(self):
		print "Scrolling to bottom..."
		while True:
				try:
					self.browser.find_element_by_class_name('_4khu') # class after friend's list
					print "Reached end!"
					break
				except:
					self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(0.25)
					pass

	def scan_friends(self):
		print 'Scanning page for friends...'
		friends = {}
		friend_cards = self.browser.find_elements_by_xpath('//div[@id="pagelet_timeline_medley_friends"]//div[@class="fsl fwb fcb"]/a')

		for friend in friend_cards:
			if friend.get_attribute('data-hovercard') is None:
				print " %s (INACTIVE)" % friend.text
				friend_id = friend.get_attribute('ajaxify').split('id=')[1]
				friend_active = 0
			else:
				print " %s" % friend.text
				friend_id = friend.get_attribute('data-hovercard').split('id=')[1].split('&')[0]
				friend_active = 1

			if friend_active != 0:
				friends[friend_id] = friend.text.encode('ascii', 'ignore').decode('ascii')
				# friends.append({
				# 	'name': friend.text.encode('ascii', 'ignore').decode('ascii'), #to prevent CSV writing issues
				# 	'id': friend_id
				# 	})

		print 'Found %r active friends on page!' % len(friends)
		return friends

	def scrape_1st_degrees(self):
		profile_icon = self.browser.find_element_by_xpath("//a[@class='_2s25 _606w']")
		myid = profile_icon.get_attribute("href")

		print "Opening Friends page..."
		self.browser.get(myid + "/friends_college")
		self.scroll_to_bottom()
		myfriends = self.scan_friends()

		with open('../data/friends.json', 'w') as fp:
			json.dump(myfriends, fp)

		return myfriends