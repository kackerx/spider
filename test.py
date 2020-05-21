import requests

res = requests.get(
    "https://mgtv-bbqn.oss-cn-beijing.aliyuncs.com/1/2005220055440861/44240.jpeg"
).content

print(res)
