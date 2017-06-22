import time
from Queue import Queue
from threading import Thread, Semaphore


class Manliligaw(Thread):
    is_last = False
    pagod_na = False

    def __init__(self, name, silya, pwede):
        Thread.__init__(self)
        self.name = name
        self.silya = silya
        self.pwede = pwede
        self.paasa_count = 0

    def run(self):
        while True:
            if self.pagod_na:
                print '{}: Maghahanap nalang ako ng iba :('.format(self.name)
                break
            pwede_pa = self.pwede.acquire(False)
            if pwede_pa:
                self.silya.put(self)
                print '{} : Nakaupo na rin sa wakas'.format(self.name)
                break
            else:
                self.hintay()

    def hintay(self):
        print '{} : Maghihintay ako sinta'.format(self.name)
        self.paasa_count += 1
        if self.paasa_count >= 3:
            self.pagod_na = True
        time.sleep(2)


class Sinta(Thread):

    def __init__(self, name, silya):
        Thread.__init__(self)
        self.name = name
        self.silya = silya
        self.basted_count = 0

    def run(self):
        while True:
            manliligaw = self.silya.get()
            if manliligaw is None:
                print '{}: Hintay lang ako ng ibabasted'.format(self.name)
                time.sleep(2)
            else:
                self.basted(manliligaw)
                if manliligaw.is_last:
                    print '{}: Tapos na akong mang-busted for today'.format(
                        self.name)
                    break

    def basted(self, manliligaw):
        print '{} at {} nag-uusap...'.format(self.name, manliligaw.name)
        time.sleep(3)
        print '{}: Hindi kita type {} eh'.format(self.name, manliligaw.name)
        self.basted_count += 1


def main():
    silya = Queue()
    pwede = Semaphore(5)
    matatapang = ['Bea', 'Gal', 'Liza', 'Angel', 'Kim', 'Tita Gwapa']
    suitors = [Manliligaw(x, silya, pwede, ) for x in matatapang]
    sinta = Sinta('Kevin', silya)
    suitors[-2].is_last = True  # No quality assurance. Terminating condition

    sinta.start()
    for suitor in suitors:
        suitor.start()

    sinta.join()
    for suitor in suitors:
        suitor.join()

    print 'Total basted count: {}'.format(sinta.basted_count)


if __name__ == '__main__':
    main()