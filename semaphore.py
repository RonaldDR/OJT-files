from Queue import Queue
from threading import Thread, Semaphore
import time

class Barber(Thread):

	def __init__(self, name, chair):
		Thread.__init__(self)
		self.name = name
		self.chair  =chair
		self.customer_count = 0

	def run(self):
		while True:
			customer = self.chair.get()
			if customer is None:
				print '{} is sleeping'.format(self.name)
				time.sleep(1)
			else:
				self.cutHair(customer)
				if customer.is_last:
					print '{} is done and closes shop. '.format(self.name)
					break


	def cutHair(self, customer):
		print '{} cuts {}\'s hair.'.format(self.name, customer.name)
		time.sleep(3)
		print '{} is done cutting {}\'s hair.'.format(self.name, customer.name)
		customer.pwede.release()
		self.customer_count += 1

class Customer(Thread):
	is_last = False
	is_tired = False

	def __init__(self, name, chair, pwede):
		Thread.__init__(self)
		self.name = name 
		self.chair = chair
		self.pwede = pwede
		self.time_waited = 0

	def run(self):
		while True:
			if self.is_tired:
				print '{} is tired of waiting and leaves the shop.'.format(self.name)
				break
			can_sit = self.pwede.acquire(False)
			if can_sit:
				self.chair.put(self)
				print '{} sits in.'.format(self.name)
				break
			else:
				self.waiting()
	def waiting(self):
		print '{} can\'t find vacant seats.'.format(self.name)
		self.time_waited += 1
		if self.time_waited >= 2:
			self.is_tired = True
		time.sleep(2)



def main():
	chair = Queue()
	pwede = Semaphore(7)
	names = ['Ronald', 'Trint', 'Santino', 'Pete', 'Bob', 'Gray', 'Gram', 'Adele']
	customers = [Customer(x, chair, pwede, ) for x in names ]
	barber = Barber('The Barber', chair)
	customers[-2].is_last = True

	barber.start()
	for customer in customers:
		customer.start()

	barber.join()
	for customer in customers:
		customer.join()

	print 'Total customers served: {}'.format(barber.customer_count)

if __name__ == '__main__':
	main()
