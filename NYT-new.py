
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



urls=deque()
cnt=0
dict={}
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


def writetofile():
	global browser
	global cnt
	if(len(urls)==0):
		return
	url=urls.pop()
	try:
		page = urllib.urlopen(url)
		soup = BeautifulSoup(page.read())
		for link in soup.find_all('a'):
			strin=link.get('href')
			if(strin and not strin in dict):
				dict[strin]=1
				if(strin.startswith('http://www.nytimes.com/20') and (('/opinion/' in strin))):
					#print strin
					urls.append(strin)
	except:
		print "error"
	
	
	#print "x"
	try:
		with time_limit(300):
			print url
			browser.set_page_load_timeout(60)
			browser.get(url+"?&target=comments?hp&target=comments#commentsContainer")
			time.sleep(5)
			print 1
			al=browser.find_element_by_css_selector('li.all')
			print 2
			al.click()
			print 3
			count=0
			time.sleep(2)
			while(more and count<10):
				count=count+1
				try:
					more=browser.find_element_by_css_selector('div.comments-expand')
					more.click()
					time.sleep(2)
				except:
					break
				finally:
					pass
			print "x"
			x=browser.page_source
			soup=BeautifulSoup(x,'html.parser')
			story=soup.find_all('p',{'class','story-body-text'})
	#x=soup.find_all('p',{'class','comment-text'})
	#x=soup.select('article[class="comment"] > p[class="comment-text"]')
			x=soup.find_all('p',{'class','comment-text'})
			comments=[]
			print "y"
			for comm in x:
				tex=comm.string
				if(tex):
					comments.append(tex)
			if(len(comments)>0):
				f=open("/home/daivik/IR/NYT/Opinion/Comments_"+str(cnt),"w")
				for comment in comments:
					try:
						print>>f,(comment.encode('utf8')+'\n')
						#print>>f,("_____________")
					except:
						pass
				f.close()
				f=open("/home/daivik/IR/NYT/Opinion/Article_"+str(cnt),"w")
				print>>f,(story.encode('utf8')+'\n')
				cnt=cnt+1;
	#for part in story:
	#	print>>f,(part.string.encode('utf8')+'\n')
				f.close()
	except Exception as e:
		print "Timed out!"
		print e.message
		#try:
		#	browser.quit()
		#except:
		#	pass
		#	browser = webdriver.Firefox()	
	writetofile()
	return


# now Firefox will run in a virtual display. 
# you will not see the browser.
if __name__=='__main__':
	#display = Display(visible=0, size=(800, 600))
	#display.start()
	global browser
	browser = webdriver.Firefox()
	baseurl='http://www.nytimes.com/pages/opinion'
	#finished=[]
	urls.append(baseurl)
	writetofile()
	#maxcount=50
	#count=0
	#while((len(urls)>0)and(count<=maxcount)):
	#	url=urls.pop()
	#	try:
	#		page = urllib.urlopen(url)
	#		soup = BeautifulSoup(page.read())
	#		print count
	#		for link in soup.find_all('a'):
	#			strin=link.get('href')
	#			if(strin and not strin in dict):
	#				dict[strin]=1
	#				if(strin.startswith(baseurl) and (('http://www.ndtv.com/india-news/' in strin))):
	#					urls.append(strin)
	#					finished.append(strin)
	#	except:
	#		print "error"
#print finished
	#cnt=0
	#print finished
	#finished=["http://www.telegraph.co.uk/finance/economics/12138466/when-is-the-next-financial-crash-coming-oil-prices-markets-recession.html#disqus_thread"]
	#for url in finished:
	#	cnt=cnt+1
	#	print cnt
	#	print url
	#	try:
	#		with time_limit(60):
	#			writetofile(url,cnt)
	#	except:
	#		print "Timed out!"
	#		try:
	#			browser.quit()
	#		except:
	#			pass
	#		browser = webdriver.Firefox()
	browser.quit()
	#display.stop()