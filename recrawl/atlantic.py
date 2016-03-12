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
#from selenium.webdriver.support import expected_conditions as EC
from collections import deque
import io
import urllib
import time
from threading import Timer
#import thread, time, sys
#import stopit



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
  baseurl="http://www.theatlantic.com/politics"
  urls.append(baseurl)
  while(len(urls)>0):
    url=urls.pop()
    try:
      with time_limit(300):
        print url
        try:
          browser.set_page_load_timeout(300)
          browser.get(url)
        except:
          pass
        time.sleep(5)
        x=browser.page_source
        soup=BeautifulSoup(x)
        try:
          print "here"
          for link in soup.find_all('a'):
            strin=link.get('href')
            if(not strin.endswith('#disqus_thread')):
                if(not strin.endswith('/')):
                  strin=strin+'/'
                strin=strin+'#disqus_thread'
            if(strin and not strin in dict):
              dict[strin]=1
              if((strin.startswith('/politics/'))):
                urls.append('http://www.theatlantic.com'+strin)
        except :
          print "error"
        print "h2"
        headline=soup.find('h1',{'class':'hed'})
        headline=headline.text
        storydiv=soup.find('div',{'class':'article-body'})
        story=""
        for para in storydiv.find_all('p'):
          story=story+para.text
        fram=soup.find('iframe',{'id':'dsq-app2'})
        print fram
        newurl=fram.get("src")
        browser.set_page_load_timeout(120)
        browser.get(newurl)
        count=0
        time.sleep(4)
        try:
          with time_limit(60):
            print 1
            while(count<10):
              print 2
              count=count+1
              try:
                more=browser.find_element_by_css_selector('div.load-more')
                more.click()
                time.sleep(1)
                print 3
              except:
                print "error"
                break
              finally:
                pass
        except:
          pass
        time.sleep(1)
        print 'h3'
        x=browser.page_source
        soup=BeautifulSoup(x)
        x=soup.findAll('div',{'class':'post-body'})
        comments=[]
        name=''
        for comm in x:
          try:
            print 'a'
            z=comm.find('a',{'data-role':'username'})
            print 'a'
            name=z.text
            z=comm.find('span',{'class':'post-meta'})
            print 'a'
            z=z.find('a')
            timeof=z.get('title')
            temp=name+"::"+timeof+"::"+"<comment>"
            print 'a'
            for tex in comm.findAll('p'):
                print 'b'
                z=tex.text
                print 'b'
                z=z.replace('\n','')
                print 'b'
                temp=temp+z
            temp=temp+"</comment>"
            print 'c'
            comments.append(temp)
            print 'comm'
          except:
            pass
        if(len(comments)>0):
          f=open("/home/daivik/IR/recrawl/atlantic/Article_"+str(cnt),"w")
          print>>f,(headline.encode('utf8')+'\n\n')
        #f=open("C:/users/Anindya Bhandari/Downloads/IR/atlantic/General/Article_"+str(cnt),"w")
          print>>f,(story.encode('utf8')+'\n\n')
          #f.close()
          #f=open("C:/users/Anindya Bhandari/Downloads/IR/atlantic/General/Article_"+str(cnt),"w")
          for comment in comments:
              try:
                  print>>f,(comment.encode('utf8')+'\n')
              except:
                  pass
          f.close()
          cnt=cnt+1;
        #f.close()
    except Exception as e:
      print "Timed out!"
      print e.message
  return
if __name__=='__main__':
  display = Display(visible=0, size=(800, 10000))
  display.start()
  writetofile()

  browser.quit()
  display.stop()
