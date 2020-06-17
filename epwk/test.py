import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PHPSESSID=b96c38359cbf6699431ad4d0279bbb26e7e5ae1b",
    "Host": "www.epwk.com",
    "Origin": "https://www.epwk.com",
    "Pragma": "no-cache",
    "Referer": "https://www.epwk.com/login.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

session = requests.session()

resp = session.get(
    "https://www.epwk.com/index.php?do=ajax&view=user_status&index=login",
    headers=headers,
    timeout=5,
).json()

# arg: formhash
formhash = resp["data"]["formhash"]

data = {
    "formhash": formhash,
    "txt_account": "kingvstr@hotmail.comdf",
    "pwd_password": "9734f5071119d2c8ef17f8577e1e0e2c",
    "login_type": "3",
    "ckb_cookie": "0",
    "hdn_refer": "https://www.epwk.com/",
    "txt_code": "2264",
    "pre": "login",
    "inajax": "1",
}

resp = session.post(url="https://www.epwk.com/index.php?do=login", headers=headers, data=data).text

print(resp)
