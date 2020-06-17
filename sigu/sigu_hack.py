import requests

url = "https://jx.126c.cn/sigu_jx.php"


data = {
    "url": "asHiRg0uc6H6Ma6Ly93d3cubWd0di5jb20vYi8xNjc0NDcvMzYyMzQ0NS5odG1s",
    "key": "yPUKmavZxpd//plPRPxuOyf0bbqH8yP4bS+DrpcXEiw=",
    "key2": "4v5h4l674k4b50415b5l5f655b5l54694v4c54685b5h5b4h",
    "key3": "4n685l40504g5l4051565k4g5c5j5l695c4g5k644l5i5c4i",
    "token": "MwjoAc5aMoDnkizmOaTgce0bMiDdce16O6T6UyMQO0O0OO0O0O",
    "type": "",
}

headers = {
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
}

response = requests.request("POST", url, data=data, headers=headers)

print(response.text)
