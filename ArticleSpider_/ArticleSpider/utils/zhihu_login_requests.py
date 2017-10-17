__author__ = 'bobby'

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re

#represent a certain connection, inrease the speed
session = requests.session()
#this allows us to use save() method
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

#try to load all the information
try:
    session.cookies.load(ignore_discard=True)
except: #display the error message
    print ("cookie cannot be loaded")

#setting up the agent
agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
#constant header for zhihu
header = {
    "HOST":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent
}


def is_login():

    #via personal center page's return status to
    #check if it is login in status
    inbox_url = "https://www.zhihu.com/question/56250357/answer/148534773"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    #200 represent successful status
    if response.status_code  != 200:
        return False
    else:
        return True

#get the xsrf from the website
def get_xsrf():
    #get xsrf code
    response = requests.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


#get all the session and restore all the information into
#the index_page.html
def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    #encoding the text into utf-8 unique code
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print ("ok")


def zhihu_login(account, password):
    #zhihu login in
    if re.match("^1\d{10}", account):
        print("Phone login in")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf,
            "phone_num": account,
            "password": password
        }

    else:
        if "@" in account:
            # check username is email
            print("Email Login in")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password
            }


    response_text = session.post(post_url, data=post_data, headers=header)


    #restore the data into local
    session.cookies.save()

zhihu_login("18782902568", "admin123")
#get_index()
is_login()