#!/usr/bin/env python

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib
import lxml.html
import time
total=0

browser = webdriver.Firefox()
mp = []
def correct_url(url): 
	if not url.startswith("http://") and not url.startswith("https://"):
  		url = "http:" + url
 	return url

def scrollDown(browser, numberOfScrollDowns):
	body = browser.find_element_by_tag_name("body")
 	while numberOfScrollDowns >=0:
  		body.send_keys(Keys.PAGE_DOWN)
  		numberOfScrollDowns -= 1
 	return browser
def crawl_url(url, k,array,n,dictionary,flag,run_headless=True):
	if run_headless:
  		display = Display(visible=0, size=(1024, 768))
  		display.start()

	url = correct_url(url)
	print url
	global mp
	mp.append(url)
        dict
	global browser 	
	try:
		browser.get(url)
		time.sleep(5)
		
		browser = scrollDown(browser, 30)
		print browser
		'''
		i=0
		while i<5:
			try:
				i=i+1
				print 'hi'
				browser.find_element_by_class_name("gig-comments-more").click()
				time.sleep(2)
			except:
				print 'exitsad'
				break	
		'''
		soup = BeautifulSoup(browser.page_source)		
		print 'hi1'
		if flag ==1 or flag ==0 :
			f = open('files','w')
			for link in (soup.find_all('a')) :
				s = link.get("href")
				if s and ('life-style/' in s or 'science/' in s) and not s in dictionary and not 'http' in s:
					dictionary[s] = 1
					s = 'independent.co.uk'+s
					print>>f,s
					print>>f,'\n'
					array.append(s)
			f.close()
		rand=soup.find_all("div",{"class":"gig-comment-body"})
		print len(rand)
		#rand=soup.find_all("div",{"class":"cmtText"})
		print "hi"
		article_body = soup.find("div",{"class":"main-content-column"})
		j=0
		if article_body :
			temp = article_body.find_all("p")
			print len(temp)
		
		if rand and article_body:
			if len(rand) > 4:
				
				f1 = open('articleindependent_tech'+str(k),'w') 
				for i in temp:
					print 'begin' 
					print>>f1,i
					print 'exit'
				f1.close()
				
					
				f = open('commentindependent_tech'+str(k),'w')
				for i in rand:
					try :
						print "beginning"
						print>>f,i.text
						print>>f,'\n'
						print 'exiting'
					except:
						print 'error occured'
						continue
				f.close()
		
		
	except:
		return	
	

if __name__=='__main__':
	array = []
	k=0
	n=1
	dictionary = {}
	h=36
	#url = 'http://economictimes.indiatimes.com/news/economy/agriculture/budget-2016-president-pranab-mukherjees-speech-hints-at-focus-on-farm-sector/articleshow/51119405.cms'
	#url = 'http://www.independent.co.uk/news/uk/politics/sketch-it-was-project-fear-in-slough-for-a-reassuringly-unpumped-prime-minister-a6891741.html'
	url = 'http://www.independent.co.uk/life-style/gadgets-and-tech'
	#browser = webdriver.Firefox()
	crawl_url(url,k,array,n,dictionary,1)
	while( k< len(array)):
		url = array[k]
		#crawl_url(url,h,array,n,dictionary,1)
		crawl_url(url,h,array,n,dictionary,0)
		k=k+1
		h=h+1
	browser.quit()
