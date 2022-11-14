# CVE-2019-20361-EXPLOIT
There was a flaw in the WordPress plugin, Email Subscribers &amp; Newsletters before 4.3.1, that allowed SQL statements to be passed to the database in the hash parameter (a blind SQL injection vulnerability).
This script is a "sanized-version" of original script avalible on exploit-db.com created by @KBA@SOGETI_ESEC
,the original version was sanized on RaidForums.com


![re4](https://user-images.githubusercontent.com/80862953/111556854-63d06780-8783-11eb-98f0-a4a6b48e98ec.png)


<h3>COMMAND</h3>

<p> > $ git clone https://github.com/jerrylewis9/CVE-2019-20361-EXPLOIT.git <br>
> $ cd CVE-2019-20361-EXPLOIT <br>
> $ chmod +x noodles.sh <br>
> $ bash noodles.sh "url"</p>


<h3>PREREQUISITE</h3>
        
**sqlmap** (https://github.com/sqlmapproject/sqlmap)


#The script recognize sqlmap, not sqlmap.py or similiar, so move sqlmap to bin directory.


