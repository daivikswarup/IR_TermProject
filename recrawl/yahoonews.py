from __future__ import with_statement # Required in 2.5
import signal
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from pyvirtualdisplay import Display
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

browser = webdriver.Firefox()
#url = "https://news.yahoo.com/n-korea-leader-orders-nuclear-arsenal-standby-kcna-223744330.html"
url = "https://uk.news.yahoo.com/explosive-device-under-vehicle-belfast-083850972.html"
browser.get(url)
x=browser.page_source
soup=BeautifulSoup(x)
storydiv=soup.find('div',{'class':'body yom-art-content clearfix'})
story=""
for para in storydiv.find_all('p'):
    story=story+para.text
#browser.execute_script("window.scrollBy(0, 1000);")
time.sleep(3)
#browser.execute_script("window.scrollBy(0, -500);")
time.sleep(3)
#print(story)
butt = browser.find_element_by_id('collapsed-comments-show')
#browser.execute_script("window.scrollBy(0, -2000);")
#browser.execute_script("window.scrollTo(0, 0);")
time.sleep(5)
#b1=browser.find_element_by_id('yui_3_18_1_1_1457095093546_1455')
browser.maximize_window()
butt.click()
