
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
	baseurl="http://www.ndtv.com/opinion"
	#finished=[]
	urls.append(baseurl)
	global browser
	global cnt
	while len(urls)>0:
		url=urls.pop()
		try:
			page = urllib.urlopen(url)
			soup = BeautifulSoup(page.read())
			for link in soup.find_all('a'):
				strin=link.get('href')
				if(strin and not strin in dict):
					dict[strin]=1
					if(strin.startswith(baseurl) and (('http://www.ndtv.com/opinion/' in strin))):
						urls.append(strin)
		except:
			print "error"
		
		
		#print "x"
		try:
			with time_limit(300):
				browser.set_page_load_timeout(60)
				print url
				browser.get(url)
				count=0
				time.sleep(5)
				print 'a'
				x=browser.page_source
				soup=BeautifulSoup(x)
				print 'b'
				headline=soup.find('div',{'class','ins_headline'}).contents[0].text
				print headline
				print 'c'
				date=soup.find('div',{'class','firstpublising'}).contents[1].get('datetime')
				print date
				print 'd'
				story=soup.find('div',{'class','ins_storybody'}).text
				print 'e'
				framesrc= browser.find_element_by_id("ndtvSocialCommentForm").get_attribute("src")
				print 'f'
				browser.set_page_load_timeout(60)
				browser.get(framesrc)
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				#x=browser.page_source
				#soup=BeautifulSoup(x)
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
				print 'g'

				x=browser.page_source
				soup=BeautifulSoup(x)
				commentlist=soup.find('div',{'class','newcomment_list'})
				print 'h'
				ul=commentlist.contents[0]
				#print ul
				#x=soup.findAll('div',{'class','com_user_text'})
		#print len(x)
		#print story
		#print x
				comments=[]
		#print "y"
				#comlist=ul.children
				for comm in ul.children:
			#print comm
			#print comm
					#print comm
					#auth=comm.li.div.div.div.contents[1].string
					#print "here"
					try:
						auth=comm.contents[0].contents[0].contents[0].contents[1]
						comment=comm.find('div',{'class','com_user_text'})
						#print {auth,comment}
						comments.append((auth,comment))
					except:
						pass
		#sp1=BeautifulSoup(comm,'xml')
		#print "here"
		#print comments
				if(len(comments)>0):
					# f=open("/home/daivik/IR/NDTV/India-news/Comments_"+str(cnt),"w")
					# for comment in comments:
					# 	try:
					# 		print>>f,(comment[0].encode('utf8')+'\n')
					# 		print>>f,(comment[1].encode('utf8')+'\n')
					# 		#print>>f,("_____________")
					# 	except:
					# 		pass
					# f.close()
					f=open("/home/daivik/IR/recrawl/NDTV/opinion/Article_"+str(cnt),"w")
					print 'i'
					print>>f,("Headline::::"+headline.encode('utf8')+'\n\n\n')
					print 'j'
					print>>f,("DateTime::::"+date+'\n\n\n')
					print 'k'
					print>>f,(story.encode('utf8')+'\n\n\n')
					for comment in comments:
						try:
							print 'l'
							print>>f,('Author::::'+comment[0].encode('utf8')+'\n')
							print 'm'
							print>>f,('Comment::::'+comment[1].encode('utf8')+'\n\n\n')
							print 'n'
							#print>>f,("_____________")
						except:
							pass
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
		#writetofile()
	return


# now Firefox will run in a virtual display. 
# you will not see the browser.
if __name__=='__main__':
	display = Display(visible=0, size=(800, 600))
	display.start()
	global browser
	browser = webdriver.Firefox()
	
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
	display.stop()
