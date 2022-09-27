#!/usr/bin/env python3

import os
import cgi
from templates import login_page
from templates import secret_page
from templates import after_login_incorrect
import secret

def parse_cookies(cookie_string):
    result = {}
    if cookie_string == "":
        return result

    cookies = cookie_string.split(";")
    for cookie in cookies:
        split_cookie = cookie.split("=")
        result[split_cookie[0].strip()] = split_cookie[1]
    
    return result

cookies = parse_cookies(os.environ["HTTP_COOKIE"])

form = cgi.FieldStorage()

username = form.getfirst("username")
password = form.getfirst("password")

header = ""
header += "Content-Type: text/html\r\n"

body = ""


if 'username' in cookies and 'password' in cookies and ('logged' in cookies and cookies['logged'] == "true"):
    if cookies['username'] == secret.username and cookies['password'] == secret.password:
        username = cookies['username']
        password = cookies['password']

if (username is not None and password is not None) or ('logged' in cookies and cookies['logged'] == "true"):
# if username is not None:
    if username == secret.username and password == secret.password:
        body += secret_page(username, password)
        header += "Set-Cookie: logged=true; Max-Age=60\r\n"
        header += "Set-Cookie: cookie=nom\r\n"
        header += f"Set-Cookie: username={username}; Max-Age=60\r\n"
        header += f"Set-Cookie: password={password}; Max-Age=60\r\n"
        body += "<h1>A terrible secret</h1>"
    else:
        body += after_login_incorrect()
else:
    body += login_page()

print(header)
print()
print(body)


