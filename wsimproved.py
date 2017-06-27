from Queue import Queue
from threading import Thread, Semaphore
import time
import requests
from PIL import Image
from StringIO import StringIO
from bs4 import BeautifulSoup
import os
import glob 

img_url = []

folderPath = "_Gallery_"

try:
    if not os.path.exists(folderPath):
        print ' Making directory... '
        os.makedirs(folderPath)
        print 'Directory made'
    else:
        print 'Directory exists.. '
except Exception as e:
    print 'Error: {} '.format(e)

class Uris(Thread):
	
	def __init__(self, num,limit):
		Thread.__init__(self)
		self.num = num
		self.limit = limit
		self.count = 0
		print '{} : {}'.format(self.num, self.limit)

	def run(self):
		while True:
			if self.count >= self.limit:
				break
			self.save()
			print self.count


	def save(self):
		
		rr = requests.get('https://c.xkcd.com/random/comic/')
		soup = BeautifulSoup(rr.text, 'html.parser')
		selector = '#comic img'
		img = soup.select(selector)[0]
		image_url = 'https:' + img.attrs['src']
		filename = image_url.split('/')[-1]
		allfiles = glob.glob('_Gallery_/*.jpg') + glob.glob('_Gallery_/*.png')
		somefile = [ff.split('/')[-1] for ff in allfiles]
	
		if not filename in somefile:		
			r = requests.get(image_url)
			i = Image.open(StringIO(r.content))
			i.save(folderPath +'/'+filename)
			self.count+= 1
			with open ("./_Gallery_/urls.txt", 'a') as f:
				f.write("\n" + rr.url)
		else:
			print 'duplicate'
		


def main():
	workers = []
	try:
		limit_main = int(input('No. of images: '))
	except ValueError:
		print 'you pressed invalid input. The default number is 40.'
		limit_main = 40

	for x in range(4):
		kani_limit = limit_main/5
		workers.append(Uris(x,kani_limit))
	temp = kani_limit + (limit_main%5)
	workers.append(Uris(4,temp))

	for worker in workers:
		worker.start()
	for worker in workers:
		worker.join()


if __name__ == '__main__':
	main()