#!/usr/bin/env python
# from bs4 import BeautifulSoup
# import urllib2
# import os

# script_dir = os.path.dirname(__file__)
# f=open('htmls.txt','w')

# r = urllib2.urlopen('http://timesofindia.indiatimes.com/entertainment/hindi/bollywood/PIC-Shahid-Kapoor-and-Mira-Rajput-on-a-dinner-date/photostory/50816030.cms').read()
# soup = BeautifulSoup(r)
# fw = open('test.txt','w')
# print>>fw,soup
# fw.close()
# print type(soup)
# g=soup.prettify()
# letters = soup.find_all("p",{ "class":"short_comment" })
# f.close()
# print letters
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
def crawl_url(url, run_headless=True):
	if run_headless:
  		display = Display(visible=0, size=(1024, 768))
  		display.start()

	url = correct_url(url)
	print url
	global mp
	mp.append(url)
	i=0
	#browser = webdriver.Firefox()
	global browser
	try:
		browser.get(url)
		time.sleep(3)
		while i<20:
			try:
				i=i+1
				browser.find_element_by_class_name("fyre-stream-more-container").click()
				time.sleep(2)
			except:
				break	

		 # seconds
		# try:
		#     WebDriverWait(browser, delay).until(EC.presence_of_element_located(browser.find_element_by_tag_name("p")))
		#     print "Page is ready!"
		# except TimeoutException:
		#     print "Loading took too much time!"
		# browser = scrollDown(browser, 10)
		#print browser
		t = lxml.html.parse(url)
		title= t.find(".//title").text
		print title
		soup = BeautifulSoup(browser.page_source)
		rand=soup.find_all("div",{"class":"fyre-comment"})	

		# 
		print "lol"
		if len(rand) != 0 :
			f=open("/home/shreygarg/Desktop/foxnews/"+title,'w')
			for comm in rand:
				print>>f,comm.p
			f.close()
		# print >>f,rand
	except:
		return	
	print "sad"	
	for link in (soup.find_all('a')):
		s=link.get("href")
		if s:
			if ("intcmp=subnav" not in s) and (("www.foxnews.com/entertainment/"  in s) or ("http://www.foxnews.com/politics/"  in s)) and mp.count(s)<1:
				crawl_url(s)

		# if s.startswith('//www.foxnews.com/entertainment/') or s.startswith("http://www.foxnews.com/entertainment/") or s.startswith('www.foxnews.com/entertainment/')and ( s!='http://www.foxnews.com/entertainment/index.html?intcmp=subnav') and mp.count(s)<1:
		# 	crawl_url(s)
	#global total
	#total=total+1
	#if total>5:
	#	return
	# connection = urllib.urlopen(url)
	# dom =  lxml.html.fromstring(connection.read())
	# print dom
	# for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
	# 	print "yo"+link


	browser.quit()

if __name__=='__main__':
	url = 'http://www.foxnews.com'
 	crawl_url(url)
# import urllib2
# from bs4 import BeautifulSoup
# fish_url = 'http://timesofindia.indiatimes.com/entertainment/hindi/bollywood/PIC-Shahid-Kapoor-and-Mira-Rajput-on-a-dinner-date/photostory/50816030.cms'
# page = urllib2.urlopen(fish_url)
# html_doc = page.read()
# soup = BeautifulSoup(html_doc)
# f=soup.prettify()

# letters = soup.find_all("p")

# print(letters[0])
