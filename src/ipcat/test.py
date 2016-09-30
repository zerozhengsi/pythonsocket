#coding=utf-8
import urllib2    
  
url = 'http://www.xici.net.co/nn/1'  
  
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
  
headers = { 'User-Agent' : user_agent }    
req = urllib2.Request(url, None, headers)    
response = urllib2.urlopen(req)    
the_page = response.read()
print the_page

