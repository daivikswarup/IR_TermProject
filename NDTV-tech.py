
from __future__ import with_statement # Required in 2.5
import signal
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from bs4 import Tag
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import deque
import io
import urllib
import time
from threading import Timer
import thread, time, sys
import stopit



class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
def timeout():
    thread.interrupt_main()


def writetofile(link,fcount):
	browser.get(link)
	dict={}
	count=0
	
	#print "x"
	time.sleep(1)
	x=browser.page_source
	soup=BeautifulSoup(x)
	story=soup.find('div',{'class','ins_storybody'}).text
	framesrc= browser.find_element_by_id("ndtvSocialCommentForm").get_attribute("src")
	browser.get(framesrc)
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	x=browser.page_source
	soup=BeautifulSoup(x)
	time.sleep(5)
	while(count<10):
		count=count+1
		try:
			more=browser.find_element_by_class_name('morecomment_bot')
			more.click()
			time.sleep(2)
		except:
			print "error2"
			break
		finally:
			pass

	x=browser.page_source
	soup=BeautifulSoup(x)
	x=soup.findAll('div',{'class','com_user_text'})
	#print len(x)
	#print story
	#print x
	comments=[]
	#print "y"
	for comm in x:
		#print comm
		#print comm
		comments.append(comm)
	#sp1=BeautifulSoup(comm,'xml')
	#print "here"
	#print comments
	f=open("/home/daivik/IR/NDTV/Tech/Comments_"+str(fcount),"w")
	for comment in comments:
		print>>f,(comment.encode('utf8')+'\n')
	f.close()
	f=open("/home/daivik/IR/NDTV/Tech/Article_"+str(fcount),"w")
	print>>f,(story.encode('utf8')+'\n')
	#for part in story:
	#	print>>f,(part.string.encode('utf8')+'\n')
	f.close()
	return


# now Firefox will run in a virtual display. 
# you will not see the browser.
if __name__=='__main__':
	display = Display(visible=0, size=(800, 600))
	display.start()
	global browser
	browser = webdriver.Firefox()
	baseurl="http://www.ndtv.com/"
	urls=deque()
	finished=[]
	urls.append(baseurl)
	maxcount=50
	count=0
	dict={}
	while((len(urls)>0)and(count<=maxcount)):
		url=urls.pop()
		try:
			page = urllib.urlopen(url)
			soup = BeautifulSoup(page.read())
			print count
			for link in soup.find_all('a'):
				strin=link.get('href')
				if(strin and not strin in dict):
					dict[strin]=1
					if(strin.startswith("http://gadgets.ndtv.com/")):
						urls.append(strin)
						finished.append(strin)
						count=count+1
						if(count==50):
							break
		except:
			print "error"
#print finished
	cnt=0
	#print finished
	#finished=["http://www.telegraph.co.uk/finance/economics/12138466/when-is-the-next-financial-crash-coming-oil-prices-markets-recession.html#disqus_thread"]
	for url in finished:
		cnt=cnt+1
		print cnt
		print url
		try:
			with time_limit(60):
				writetofile(url,cnt)
		except:
			print "Timed out!"
			try:
				browser.quit()
			except:
				pass
			browser = webdriver.Firefox()
	browser.quit()
	display.stop()
