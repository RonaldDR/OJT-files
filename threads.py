from threading import Thread, Lock
import threading
import time
import logging

fork =[Lock(),Lock(),Lock(),Lock(),Lock()]
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class Diners(Thread):

    def __init__(self, name, left, right):
        Thread.__init__(self)
        self.name = name
        self.left = left
        self.right = right	


    def run(self):
    	time.sleep(1)

    	with self.left:
    		logging.debug(self.name + " picks the left fork. ") 
    		with self.right:
    			logging.debug(self.name + " picks the right fork.\n"+self.name + " is eating")
    			logging.debug(self.name + " is full.")

    	# if not self.right.is_released():
    	# 	logging.debug(self.name + " drops the left fork.Can't get the right fork.")
    	# 	if not self.left.acquired():
    	# 		self.left.release()

def main():
    a = Diners('Aristotle', fork[0], fork[1])
    b = Diners('Kant', fork[1], fork[2])
    c = Diners('Buddha', fork[2], fork[3])
    d = Diners('Marx', fork[3], fork[4])
    e = Diners('Russel', fork[4], fork[0])

    a.start()
    b.start()
    c.start()
    d.start()
    e.start()

    a.join()
    b.join()
    c.join()
    d.join()
    e.join()

    logging.debug("Everyone is full. ")



main()