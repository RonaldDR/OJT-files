from Queue import Queue
from threading import Thread, Semaphore
import time

class Barber(Thread):

    def __init__(self, name, chair, pwede):
        Thread.__init__(self)
        self.name = name
        self.chair = chair
        self.pwede = pwede
        self.customer_count = 0

    def run(self):
        while True:
            customer = self.chair.get()
            if customer is None:
                print '{} is sleeping. '.format(self.name)
                time.sleep(1)
                break
            can_cut = self.pwede.acquire(False)
            if can_cut:
                self.cutHair(customer)
            if customer.is_last:
                print '{} is done and closes shop. '.format(self.name)

    def cutHair(self, customer):
        print '{} cuts {}\'s hair. '.format(self.name, customer.name)
        time.sleep(3)
        print '{} is done cutting {}\'s hair. '.format(self.name, customer.name)
        self.customer_count += 1


class Customer(Thread):
    is_tired = False
    is_last = False

    def __init__(self, name, chair):
        Thread.__init__(self)
        self.name = name
        self.chair = chair
        self.time_waited = 0

    def run(self):
        while True:
            if self.is_tired:
                print '{} is tired of waiting and leaves the shop.'.format(self.name)
                break
            if self.chair.qsize() >= 5:
                self.waiting()
                break
            self.chair.put(self)
            print '{} sits in. '. format(self.name)


    def waiting(self):
        print '{} can\'t find vacant seats.'.format(self.name)
        self.time_waited += 1
        if self.time_waited >= 3:
            self.is_tired = True
        time.sleep(2)

def main():
    chair = Queue()
    pwede = Semaphore(5)
    names = ['Ronald','Trint', 'Santino', 'Pete', 'Bob']
    customers = [Customer(x, chair,) for x in names]
    barber = Barber('The Barber', chair, pwede)
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