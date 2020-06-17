import json
import re
import requests


def get_token():
    url = "https://upload-ugc.bz.mgtv.com/upload/image/getStsToken"

    querystring = {
        "uuid": "389edfe9aedc4e48afc06487f8f90861",
        "ticket": "BQMI2SPLQHGI6J9C9KBG",
        "biz": "1",
        "num": "1",
        "callback": "jQuery18207917163912499288_1590069113392",
        "_support": "10000000",
        "_": "1590069189374",
    }

    headers = {
        "authority": "upload-ugc.bz.mgtv.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
        "cookie": "sessionid=1590069109726; __STKUUID=56977c5b-7bb9-4dce-9bfb-4504d3b03b35; mba_deviceid=d5de0866-2126-36b1-d6bc-d81dc685a555; mba_sessionid=294caf74-bb56-d608-7dde-aa0d052555d4; MQGUID=1263467303526383616; __MQGUID=1263467303526383616; pc_v6=v6; _source_=C; PLANB_FREQUENCY=XsaHekEI7nBda-UG; __random_seed=0.09710746912465718; __gads=ID=5a426adf65fcb414:T=1590069115:S=ALNI_MbjtIzVPfp7KjnKslTuXdr6aWe8yw; PM_CHKID=a344546caaf6da69; Account=dc375ff5ac67b0b1883e65bfd3559d4e; id=42654603; rnd=rnd; seqid=br38f9iu3du7jva4mt8g; uuid=4aca7ff2f5154817a3df0aa982463eaa; vipStatus=3; wei=a865a1e55fdf90da2f83f050331896bb; wei2=15feP2k4Rfa%2FqM4BfJISsLJKZFKvwrh4w1%2BW1fwqT45Mligens97x89Vm1uvTMachwFufmnqT6l%2F18AGkAHdRLHZw5e0eROSFcFNXRjr7q%2FUI75uFbjNzlV%2F6a7ZIfyMxIslEcHTPj%2FpQ%2BjW5IXPQ2W0%2BzhGw9jw3CK93aPsRlikrgRH0KsfHjf0JVqawOasWu38VIFfxNubmAl1mPYPpAg3lGyay3xAousApA; HDCN=BR38F9LCN4B2FBK8L4T0-265800768; mba_last_action_time=1590070587695; beta_timer=1590070588630; lastActionTime=1590070662696",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text


def upload_img(img_url):
    res = get_token()
    _str = re.search(".*?\((.*?)\);", res, re.S)
    json_res = json.loads(_str.group(1))["data"]
    accessKeyId = json_res["stsToken"]["accessKeyId"]
    accessKeySecret = json_res["stsToken"]["accessKeySecret"]
    securityToken = json_res["stsToken"]["securityToken"]
    keys = json_res["bucketInfo"]["keys"][0]

    data = {
        "accessKeyId": accessKeyId,
        "accessKeySecret": accessKeySecret,
        "securityToken": securityToken,
        "keys": keys,
    }
    res = requests.post("http://localhost:3000/getsign", data=data).json()

    auth = res["auth"]
    date = res["date"]

    url = f"https://mgtv-bbqn.oss-cn-beijing.aliyuncs.com/{keys}.jpeg"

    payload = requests.get(img_url).content

    # with open("./test.png", "rb") as f:
    #     payload = f.read()

    headers = {
        "connection": "keep-alive",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "x-oss-user-agent": "aliyun-sdk-js/5.2.0 Chrome 81.0.4044.122 on OS X 10.15.5 64-bit",
        "authorization": auth,
        "x-oss-date": date,
        "x-oss-security-token": securityToken,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
        "content-type": "image/jpeg",
        "accept": "*/*",
        "origin": "https://www.mgtv.com",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.mgtv.com/b/316458/3998946.html",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return url


if __name__ == "__main__":
    url = "https://www.op811.com/wp-content/uploads/2020/05/sp200522223607.jpg"
    print(upload_img(url))
