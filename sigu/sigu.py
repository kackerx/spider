from faker import Factory
import requests

f = Factory.create()

headers = {"user-agent": f.user_agent()}

url = "https://jx.126c.cn/?url=https://www.mgtv.com/b/167447/3623445.html"


res = requests.get(url, headers=headers, allow_redirects=False)


print(res.text)

# url2 = "https://zl.126c.cn/zl_api.php"

# import json

# data = {"url": "https://v.qq.com/x/cover/dxd1v76tmu0wjuj.html"}
# re = requests.post(url2, data=data).json()
# print(re)
