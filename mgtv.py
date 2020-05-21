import requests

url = "https://mgtv-bbqn.oss-cn-beijing.aliyuncs.com/1/2005220055440861/44240.jpeg"

payload = ""

with open("./test.png", "rb") as f:
    payload = f.read()

headers = {
    "connection": "keep-alive",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "x-oss-user-agent": "aliyun-sdk-js/5.2.0 Chrome 81.0.4044.122 on OS X 10.15.5 64-bit",
    "authorization": "OSS STS.NUWRXB9zujsZx9719JFZvnLDm:61yyLQ3cZ8sYaNPRZGE+NVWYRqQ=",
    "x-oss-date": "Thu, 21 May 2020 16:56:43 GMT",
    "x-oss-security-token": "CAISwQJ1q6Ft5B2yfSjIr5biGeL21KVU3bGxeh+G1TkfStVagYnvjzz2IHpKeXVrAOAXsPs0mmhT6fgZlol/GsdJGhWcZ5ott5gLrFv/M9Wb6pDo4LJYhMevRWWYVEYrQjR4qKOrIunGc9KBNnrT9EYqs6mYGBymW1u6S9Lr7bdsctUQWCShcDNCH604DwB+qcgcRxyzUPG2KUzSn3b3BkhlsRYGqQEZ06mkxdCG4RfzlUDzzvRvx778OZ+5dcJhTtMdEd6+x75xbbGTknwSuR1F6LkzhqZd/3Ce+YvFWwQLuU3ebreIroU/clY+JIpCQvUU8aSty6Qp4bOKy96skCwgZ78FD37tI6m729bBFe+TMdI0SK32IXyl0KrUbMeo71h9MSNFa1gUI4F+dCRqbBs3UXTfJbO5vVrAewGzmlA2e1bdAvAagAFAMQIDB00u9mGAbvZszDvj/VYZNXDADFLPwq5zTmVyyg4NAobD5vX3fE1gmRR9sJ51lWiaJCnjnN1a9syiMYPlxtJ9JMhqSPkmIy1O9Yjg6yRDMpZs+Db4NthTMJjWJ0GNQfb9oXTT7+vdunVXg0CA7ffEhVhoQ5yM+MTKeJ+4uA==",
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

response = requests.request("PUT", url, data=payload, headers=headers)

print(response.text)
