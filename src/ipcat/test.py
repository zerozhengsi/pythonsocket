#coding=utf-8
import urllib2    
import threading
  
url = 'http://192.168.229.251/test'  
  
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
  
headers = { 'User-Agent' : user_agent }  
def test():  
    req = urllib2.Request(url, None, headers)    
    response = urllib2.urlopen(req)    
    the_page = response.read()
    print the_page
    
all_thread = []
for i in range(10):
    t = threading.Thread(target=test)
    all_thread.append(t)
    t.start()
    
for t in all_thread:
    t.join()

