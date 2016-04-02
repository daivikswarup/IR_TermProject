#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2

def crawl_url(url,k,array):
	print url


	proxy = urllib2.ProxyHandler({'http':'10.3.100.207:8080'})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	response = urllib2.urlopen(url)
	page_source = response.read()
	soup = BeautifulSoup(page_source)		
	article_body = soup.find("div",{"class":"content__article-body from-content-api js-article__body", "itemprop":"articleBody" , "data-test-id":"article-review-body"})
	if article_body:
		print "article found" 
		subparts = article_body.find_all('p')
		publishtime = soup.find("time",{"itemprop":"datePublished"}).get('datetime')
		print len(subparts)
		
		u = soup.find("div",{"class":"preload-msg discussion__loader"})
		base = 'http://www.theguardian.com/'
		if u and (publishtime[3] == '6'):
			f = open('article' + str(k), 'w')
			headline = soup.find("h1",{"class":"content__headline js-score" }).text.encode('utf8')
			print>>f,"Headline::::"  + headline + '\n\n\n'
			print>>f,'DateTime::::' + publishtime +'\n\n\n'
			for i in subparts:
				print>>f,i.encode('utf8')+'\n'
			print>>f,'\n\n'
			link = base + u.a.get('href')
			print "looking for comments @" + link
			comment_response = urllib2.urlopen(link)
			comment_soup = BeautifulSoup(comment_response.read())
			comments = comment_soup.find_all("div",{"class":"d-comment__inner d-comment__inner--top-level"})
			for i in comments:
				user = i.find("span",{"class":"d-comment__author"}).get('title')
				time = i.find("time",{"class":"js-timestamp"}).get('datetime')
				com = i.find("div",{"class":"d-comment__body"}).p
				if com:
					com = str(i.find("div",{"class":"d-comment__body"}).p.text.encode('utf8'))
					print>>f,"Author::::"+user.encode('utf8')+'\n'+"DateTime::::"+time+'\n'+com+'\n\n\n'
			f.close()

			
			
	print "getting links"		
	f2 = open('files','w+')
	for link in (soup.find_all('a')) :
		s = link.get("href")
		if s:
			
			if ( not "rssfeeds" in s and not "newshome" in s and not "currentquote" in s and not "marketstats" in s and not "mutual_funds" in s and not "twitter" in s and "http://www.theguardian.com/sport/" in s and not "google.co" in s ):
				if not s in array : 
					array.append(s)
					print>>f2,s +'\n'
	f2.close()	


if __name__=='__main__':
	array = []
	k=0
	url = 'http://www.theguardian.com/sport'
	
	crawl_url(url,k,array)
	
	while( k< len(array)):
		url = array[k]
		crawl_url(url,k,array)
		k=k+1
	
