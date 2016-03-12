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
	browser = webdriver.Firefox()
	baseurl="https://in.news.yahoo.com/"
	#finished=[]
	urls.append(baseurl)
	while(len(urls)>0):
		url=urls.pop()
		#try:
		#	page = urllib.urlopen(url)
		#		strin=link.get('href')
		#		if(strin and not strin in dict):
		#			dict[strin]=1
		#			print strin
		#			if((strin.startswith('http://www.theatlantic.com/politics/'))):
		#				urls.append(strin)
		#except :
		#	print "error"
	
	
	#print "x"
		try:
			with time_limit(300):
				print url
				try:
					browser.set_page_load_timeout(120)
				#browser.get(url)
					#if(not url.endswith('#disqus_thread')):
					#	url=url+'/#article-comments'
					browser.get(url)
				except:
					pass
				time.sleep(5)
				x=browser.page_source
			#print x
			#print 1
			#f=open("source"+str(cnt)+".txt","w")
			#print>>f,x
			#cnt=cnt+1
			#f.close()
				soup=BeautifulSoup(x)
				try:
					print "here"
					for link in soup.find_all('a'):
						strin=link.get('href')
						#if(not strin.endswith('#disqus_thread')):
						if(not strin.endswith('/')):
							strin=strin+'/'
								#strin=strin+'#disqus_thread'
						if(strin and not strin in dict):
							#print strin
							if(strin.startswith('/')):
								print "x"
								dict[strin]=1
                                                                urls.append("https://in.news.yahoo.com"+strin)
				except :
					print "error"
			#print 2
			#dict={}
			#page = urllib.urlopen(url)
			#soup = BeautifulSoup(page.read())
				print "yo"
				#f=open('f'+str(cnt),'w')
				#cnt=cnt+1
				#f.write(x.encode('utf8'))
				#f.close()
				#app=soup.find('body')
				#print 1
				#artid=app.contents[0].contents[0].get('data-reactid')
				#print 2
				#el=browser.find_element_by_xpath("//div[@data-reactid='"+artid+".$0.0.0.2.5.0.0.$Col1-0-ContentCanvasProxy']")
				#print 3
				#browser.execute_script("return arguments[0].scrollIntoView();",el)
				#x=browser.page_source
				#soup=BeautifulSoup(x)
				storydiv=soup.find('div',{'class':'canvas-body'})
				date=soup.find('div',{'class':'date'}).text
				print date
				#if('2016' not in date):
				#	continue
				#print storydiv
				story=""
				#print len(storydiv.find_all('p'))
				for para in storydiv.find_all('p'):
					story=story+para.text
	#x=soup.find_all('p',{'class','comment-text'})
	#x=soup.select('article[class="comment"] > p[class="comment-text"]')
			#print story
				print "xxx"
				#print story
	#			fram=soup.find('iframe',{'id':'dsq-app2'})
				
				#el=browser.find_element_by_xpath("//div[@data-reactid='"+artid+".$0.0.0.2.5.0.0.$Col1-2-CommentsProxy']")
				#print 3
				#browser.execute_script("return arguments[0].scrollIntoView();",el)
				print 4
				#browser.execute_script("scroll(0, -1000);");
				button=browser.find_element_by_class_name('view-comments')
				print button
				time.sleep(10)
				print 5
				button.click()
				print 6
				time.sleep(2)
                                #button=browser.find_element_by_class_name('view-comments')
                                #print "here2"
                                #button.click()
	#print fram		
	#			newurl=fram.get("src")
				print "here1"
	#print newurl
	#			browser.set_page_load_timeout(120)
	#			browser.get(newurl)
				count=0
        #			time.sleep(4)
				try:
					with time_limit(60):
						print 1
						while(count<10):
	#						print 2
							count=count+1
							try:
								print 3
								#with time_limit(2):
								more=browser.find_element_by_css_selector('li.comments-button')
								more.click()
	#							print 5
								time.sleep(1)
							except:
        							print "error2"
								break
							finally:
								pass
				except:
					pass
	#print "x"	
			#print "here"
				time.sleep(1)
				x=browser.page_source
	#print x
			#print "no i wont print yo"
				soup=BeautifulSoup(x)
				x=soup.find('ul',{'class':'comment-list'})
				print x		
				comments=[]
	#print "y"
				for comm in x.children:
			#print comm
					temp="<author>"
					temp=temp+comm.find('span',{'class':'username'}).text
					temp=temp+"</author>\n"
					temp=temp+"<comment>"
					temp=temp+comm.contents[0].contents[1].contents[0].text
					temp=temp+"</comment>"
				#print temp
					comments.append(temp)
			#print "c"
				print len(comments)
				if(len(comments)>0):
					f=open("/home/daivik/IR/yahoo/Comments_"+str(cnt),"w")
					for comment in comments:
						try:
							print>>f,(comment.encode('utf8')+'\n')
						#print>>f,(comment[1].encode('utf8')+'\n')
						#print>>f,("_____________")
						except:
							pass
					f.close()
					f=open("/home/daivik/IR/yahoo/Article_"+str(cnt),"w")
					print>>f,(date.encode('utf8')+'\n')
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
	#writetofile()
	return


# now Firefox will run in a virtual display. 
# you will not see the browser.
if __name__=='__main__':
	display = Display(visible=0, size=(800, 100000))
	display.start()
	#global browser
	#browser = webdriver.Firefox()
	#baseurl="http://zeenews.india.com/news"
	#finished=[]
	#urls.append(baseurl)
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
