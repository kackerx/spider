
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# res = requests.put("https://www.hehedy.com", proxies=proxies, verify=False).resp
import requests

headers = {
    'Connection': 'keep-alive',
    'x-oss-user-agent': 'aliyun-sdk-js/5.2.0 Chrome 81.0.4044.138 on OS X 10.15.4 64-bit',
    'authorization': 'OSS STS.NUAKW11Nhqz677pfSGRw4yzFW:VgkZY/B44b3pGuH/jsYFUZdageI=',
    'x-oss-date': 'Thu, 21 May 2020 14:28:15 GMT',
    'x-oss-security-token': 'CAISwQJ1q6Ft5B2yfSjIr5b0AO2F3JFJxrjdNRHBglMSXvgYlr/ttTz2IHpKeXVrAOAXsPs0mmhT6fgZlokoEpUYHhKbZMYp58kMqVysOoDM58Xk5LVZ1MT1RmaaAUZGU1AHqKOrIunGc9KBNnrT9EYqs6mYGBymW1u6S9Lr7bdsctUQWCShcDNCH604DwB+qcgcRxyzUPG2KUzSn3b3BkhlsRYGqQEZ06mkxdCG4RfzlUDzzvRvx778OZ+5dcJhTtMdEd6+x75xbbGTknwSuR1F6LkzhqZd/3Ce+YvFWwQLuk/cabqNroZCBSY+JIpCQvUU8aSty6Qp4bOKy96skCwgZ78FD37tI6m729bBFe+TMdI0SK32IXyl0KrUbMeo71h9MSNFa1gUI4F+dCRqbBs3UXTfJbO5vVrAewGzmlA2e1bdAvAagAFTno490P8lL2Pt2PvbYBKucZYh1EpNXB1wWJ5fFKl3R81Dk7jSY7ufycxhgM1pXNxiwTVGf91U/UegACFnFJR3y4h59nWSecK7vZqkIbwLShAXqNZ7/X253F1ruiROOYKZdn2rgBf/nNdN8neFzNvwfnod+A3yq2LekRfPrjvOow==',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Content-Type': 'image/jpeg',
    'Accept': '*/*',
    'Origin': 'https://www.mgtv.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.mgtv.com/b/167447/3720067.html?fpa=se&lastp=so_result',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7',
}

data = '$as\xFF\xD9'

response = requests.put('https://mgtv-bbqn.oss-cn-beijing.aliyuncs.com/1/2005212228143EAA/23090.jpeg', headers=headers, data=data, proxies=proxies, verify=False)
