# POC CVE-2020-24186-wpDiscuz-7.0.4-RCE

WordPress wpDiscuz 7.0.4 Remote Code Execution

- A Remote Code Execution vulnerability exists in the gVectors wpDiscuz plugin 7.0 through 7.0.4 for WordPress, which allows unauthenticated users to upload any type of file, including PHP files via the wmuUploadFiles AJAX action.

### Exploit Usage

#### Commands:
- Windows/Linux:
`$ sudo python3 wpDiscuz_RemoteCodeExec.py -u <Base_Host> -p <BlogPost_URL> `

![](https://github.com/hevox/CVE-2020-24186-wpDiscuz-7.0.4-RCE/blob/main/imgs/wordpressdiscuz.png.png)

- References:

  https://www.exploit-db.com/exploits/49967
  
  https://packetstormsecurity.com/files/163012/WordPress-wpDiscuz-7.0.4-Remote-Code-Execution.html

  https://nvd.nist.gov/vuln/detail/CVE-2020-24186
  
  https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-24186

