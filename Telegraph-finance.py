
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
	x=browser.page_source
	soup=BeautifulSoup(x)
	dict={}
	story=soup.find('div',{'class':'body'})
	#x=soup.find_all('p',{'class','comment-text'})
	#x=soup.select('article[class="comment"] > p[class="comment-text"]')
	fram=soup.find('iframe',{'id':'dsq-app2'})
	#print fram
	newurl=fram.get("src")
	#print newurl
	browser.get(newurl)
	count=0
	time.sleep(1)
	while(count<10):
		count=count+1
		try:
			more=browser.find_element_by_css_selector('div.load-more')
			more.click()
			time.sleep(1)
		except:
			print "error2"
			break
		finally:
			pass
	#print "x"
	time.sleep(1)
	x=browser.page_source
	#print x
	soup=BeautifulSoup(x)
	x=soup.findAll('div',{'class','post-message'})
	#print x
	comments=[]
	#print "y"
	for comm in x:
		#print comm
		for tex in comm.findAll('p'):
			comments.append(tex)
	#sp1=BeautifulSoup(comm,'xml')
	#print "here"
	#print comments
	f=open("/home/daivik/IR/Telegraph/Finance/Comments_"+str(fcount),"w")
	for comment in comments:
		print>>f,(comment.encode('utf8')+'\n')
	f.close()
	f=open("/home/daivik/IR/Telegraph/Finance/Article_"+str(fcount),"w")
	print>>f,(story.encode('utf8')+'\n')
	#for part in story:
	#	print>>f,(part.string.encode('utf8')+'\n')
	f.close()
	return


# now Firefox will run in a virtual display. 
# you will not see the browser.
if __name__=='__main__':
	#display = Display(visible=0, size=(800, 600))
	#display.start()
	global browser
	browser = webdriver.Firefox()
	baseurl="http://www.telegraph.co.uk"
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
					if(strin.startswith(baseurl) and strin.endswith('.html') and (('http://www.telegraph.co.uk/finance/' in strin))):
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
		#try:
		#	with time_limit(60):
		writetofile(url,cnt)
		#except:
		#	print "Timed out!"
		#	try:
		#		browser.quit()
		#	except:
		#		pass
		#	browser = webdriver.Firefox()
	browser.quit()
	#display.stop()
