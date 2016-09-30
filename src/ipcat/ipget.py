#coding=utf-8
'''
Created on 2016年7月8日

@author: Administrator
'''
from bs4 import BeautifulSoup
import urllib2
 
 
of = open('proxy.txt' , 'w')

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    
  
headers = { 'User-Agent' : user_agent }    
  
 
for page in range(1, 10):
    req = urllib2.Request('http://www.xici.net.co/nn/' + str(page), None, headers)  
    html_doc = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html_doc)
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        ip = tds[1].text.strip()
        port = tds[2].text.strip()
        protocol = tds[5].text.strip()
        if protocol == 'HTTP' or protocol == 'HTTPS':
            of.write('%s=%s:%s\n' % (protocol, ip, port) )
            print '%s=%s:%s' % (protocol, ip, port)
 
of.close()