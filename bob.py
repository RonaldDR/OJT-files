import Queue
from threading import Thread, Lock, Event, BoundedSemaphore
import threading
import time

mutex = Lock()
q = Queue.Queue
mutex = threading.Semaphore()

class Customer:
    def __init__(self, name):
        self.name = name

class Barber:
    barber_event = Event()

    def __init__(self, name):
        self.name = name

    def sleep(self):
        self.barber_event.wait()

    def wakeUp(self):
        print 'The barber is awake. '
        self.barber_event.set()

    def cut(self, customer):
        self.barber_event.clear()

        print 'Barber cuts ' + customer.name + '\'hair ' 
        time.sleep(1)
        print 'Barber is done cutting '+ customer.name +'\'s hair'

class Shop():
    waiting_room =[]






names = ["Paul","Peter", "Matthew", "John", "Andrew" ]
people = []

def main():
    
    for ctr in range(5):
        people.append(Customer(names[ctr]))

main()

# Barber 
# Check the waiting room if there is a customer
# If there is no customer, go to sleep.
# If there is a customer:
#     Serve the customer according to haircut // a haircut may vary in service time
#     If the customer is the last customer // Hint: You can assign a customer as the last customer as a way to end the simulation
#         Close the shop

# Customer
# Checks if the barber is sleeping:
#     If he is asleep wake him up
# If the barber is busy:
#     Are waiting chairs free? Take one seat
#     Are all chairs are occupied? Leave