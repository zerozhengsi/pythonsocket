#coding=utf-8
'''
Created on 2016年7月8日

@author: Administrator
'''
import httplib
import time
import urllib
import threading

inFile = open('proxy.txt', 'r')
outFile = open('available.txt', 'w')

lock = threading.Lock()

def test():
    while True:
        lock.acquire()
        line = inFile.readline().strip()
        lock.release()
        if len(line) == 0: break
        protocol, proxy = line.split('=')
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': ''}
        try:
            conn = httplib.HTTPConnection(proxy, timeout=3.0)
            conn.request(method='POST', url='http://e.meituan.com/m/account/login', body='login=ttttttttttttttttttttttttttttttttttttt&password=bb&remember_username=1&auto_login=1', headers=headers )
            res = conn.getresponse()
            ret_headers = str( res.getheaders() ) 
            html_doc = res.read().decode('utf-8')
            print html_doc.encode('gbk')
            if ret_headers.find(u'/m/account/login/') > 0:
                lock.acquire()
                print 'add proxy', proxy
                outFile.write(proxy + '\n')
                lock.release()
            else:
                print '.',
        except Exception, e:
            print e

all_thread = []
for i in range(50):
    t = threading.Thread(target=test)
    all_thread.append(t)
    t.start()
    
for t in all_thread:
    t.join()

inFile.close()
outFile.close()