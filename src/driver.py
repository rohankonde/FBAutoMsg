from fbmessage import MessengerBot
import client
from threading import Thread
from twisted.internet import task, reactor


if __name__ == "__main__":
	bot = MessengerBot("settings.txt")
	
	t1 = Thread(target=client.main, args=(reactor,))
	t1.start()
	t1.join()

	bot.update_recipients()
	bot.run()