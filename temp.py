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
def writetofile(link,fcount):
	browser.get(link)
	al=browser.find_element_by_css_selector('li.all')
	al.click()
	time.sleep(2)
	try:
		more=browser.find_element_by_css_selector('div.comments-expand')
		more.click()
	except:
		pass
	finally:
		pass
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
	#sp1=BeautifulSoup(comm,'xml')
	print "here"
	f=open("Comments_"+str(fcount),"w")
	for comment in comments:
		print>>f,(comment.encode('utf8')+'\n')
	f.close()
	f=open("Article_"+str(fcount),"w")
	for part in story:
		print>>f,(part.string.encode('utf8')+'\n')
	f.close()
	return
#display = Display(visible=0, size=(800, 600))
#display.start()

# now Firefox will run in a virtual display. 
# you will not see the browser.
if __name__=='__main__':
	global browser
	browser = webdriver.Firefox()

	baseurl='http://www.nytimes.com'
	urls=deque()
	finished=[]
	urls.append(baseurl)
	maxcount=49
	count=0
	while((len(urls)>0)and(count<=maxcount)):
		url=urls.pop()
		page = urllib.urlopen(url)
		soup = BeautifulSoup(page.read())
		print count
		for link in soup.find_all('a'):
			strin=link.get('href')
			if(strin):
				if(strin.startswith(baseurl+"/20")):
					urls.append(strin)
					finished.append(strin)
					count=count+1
					if(count==50):
						break
#print finished
	cnt=0
	for url in finished:
		cnt=cnt+1
		print cnt
		print url
		try:
			writetofile(url+"?&target=comments?hp&target=comments#commentsContainer",cnt)
		except:
			print "shiiiit"
			browser.quit()
			browser=webdriver.Firefox()
	browser.quit()
#display.stop()
