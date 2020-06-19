import execjs
from random import choice
from distance import SlideCrack
import random
import json
import requests

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "captcha.yunpian.com",
    "Pragma": "no-cache",
    "Referer": "https://www.yunpian.com/product/captcha",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}


def load_js():
    """
    加载js文件
    """
    with open("yunk.js", "r") as f:
        js = f.read()
    ctx = execjs.compile(js)
    return ctx


def get_cb(ctx):
    """
    cb
    """
    return ctx.call("get_cb")


def _encrypt_data(ctx, data):
    return ctx.call("encrypt_data", data)


def init_slider(ctx):
    url = "https://captcha.yunpian.com/v1/jsonp/captcha/get"
    # 浏览器信息
    # data = '{"browserInfo":[{"key":"userAgent","value":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"},{"key":"language","value":"zh-CN"},{"key":"hardware_concurrency","value":12},{"key":"resolution","value":[1792,1120]},{"key":"navigator_platform","value":"MacIntel"}],"mobile":"","nativeInfo":{},"username":"","options":{"sdk":"https://www.yunpian.com/static/official/js/libs/riddler-sdk-0.2.2.js"},"fp":"cf328f0709b3876769376750c43fbdcc","address":"https://www.yunpian.com","yp_riddler_id":"65c0ac64-6655-4a26-8bed-3f8350a0a31a"}'
    data = """
        {
            address: "https://www.yunpian.com",
            //浏览器指纹
            browserInfo: [{
                    key: "userAgent",
                    value: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
                },
                {
                    key: "language",
                    value: "zh-CN"
                },
                {
                    key: "hardware_concurrency",
                    value: 4
                },
                {
                    key: "resolution",
                    value: [1920, 1080]
                },
                {
                    key: "navigator_platform",
                    value: "Win32"
                },
            ],
            fp: "4dd3d0b50fafd97371c355f2c5655df3",
            mobile: "",
            nativeInfo: {},
            options: {
                sdk: "https://www.yunpian.com/static/official/js/libs/riddler-sdk-0.2.2.js"
            },
            username: "",
            yp_riddler_id: "",
        }    
    """
    encrypt_data = _encrypt_data(ctx, data)
    params = {
        "cb": get_cb(ctx),
        "i": encrypt_data["i"],
        "k": encrypt_data["k"],
        "captchaId": "974cd565f11545b6a5006d10dc324281",
        # "token": "d0e988d377c243808536a8c490378c94",
    }

    ret = (
        requests.get(url, params=params, headers=headers)
        .text.replace("ypjsonp(", "")
        .replace(")", "")
    )

    ret_json = json.loads(ret)
    if ret_json["msg"] == "ok":
        return {
            "captcha_url": ret_json["data"]["bg"],
            "slider_url": ret_json["data"]["front"],
            "token": ret_json["data"]["token"],
        }


def get_distance(slider_url, captcha_url):
    # 下载图片
    with open("captcha.png", "wb") as f:
        f.write(requests.get(captcha_url).content)

    with open("slider.png", "wb") as f:
        f.write(requests.get(slider_url).content)

    sc = SlideCrack("slider.png", "captcha.png", "res.png")
    return sc.discern()


# 获取鼠标轨迹
def get_potions(offset):
    arrays = []
    downtime = random.randint(1, 20)  # 模拟滑块位移的时间差
    buttonx = random.randint(1100, 1154)  # 模拟鼠标按下滑块时的page.X值
    buttony = random.randint(1954, 1990)  # 模拟鼠标按下滑块时的page.Y值
    array1 = [buttonx, buttony, downtime]
    arrays.append(array1)
    for i in range(offset):  # offset是识别出的滑块距离，假设每次移动1px最多有offset个鼠标移动数组
        if arrays[-1][0] <= offset + buttonx:  # 判断滑块移动是否超过了offset
            if arrays[-1][0] <= buttonx + int(
                (offset / 6) * 5
            ):  # 模拟人在滑动最后减速，在此判断是否剩最后的1/6距离，如果是则减速
                arrays.append(
                    [
                        arrays[-1][0] + random.choice([2, 3, 4, 5]),
                        buttony + random.choice([1, -1, 2, -2, 0, 0]),
                        arrays[-1][2] + random.randint(1, 20),
                    ]
                )

            else:
                arrays.append(
                    [
                        arrays[-1][0] + random.choice([1, 1, 1, 0]),
                        buttony + random.choice([1, -1, 2, -2, 0, 0]),
                        arrays[-1][2] + random.randint(1, 20),
                    ]
                )
        else:
            break

    # 下面是复现js的逻辑，对鼠标轨迹数组长度判断并处理
    if len(arrays) < 50:
        return arrays

    newarrays = [arrays[0]]
    lastarray = arrays[-1]
    r = int(len(arrays) / 50)

    if r < 2:
        return arrays

    for i in range(1 + r, len(arrays) - 2, r):
        newarrays.append(arrays[i])
    newarrays.append(lastarray)
    return newarrays


def crack():
    headers = {
        "Host": "captcha.yunpian.com",
        "Referer": "https://www.yunpian.com/product/captcha",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
        "Host": "captcha.yunpian.com",
        "Connection": "close",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
    }
    url = "https://captcha.yunpian.com/v1/jsonp/captcha/verify?"
    # 加载js
    ctx = load_js()
    # 获取滑块
    init_data = init_slider(ctx)
    # 获取滑动距离
    distance = get_distance(init_data["slider_url"], init_data["captcha_url"])
    distance = int(distance * (310 / 480)) - 5
    # 产生轨迹
    trace = get_potions(distance)
    # trace = [[808,1973,2],[808,1973,143],[812,1973,144],[817,1973,152],[824,1973,160],[833,1973,170],[846,1973,177],[855,1973,187],[866,1973,193],[868,1973,201],[873,1973,209],[879,1973,218],[882,1973,227],[883,1973,233],[885,1973,243],[886,1973,249],[886,1973,258],[886,1973,281],[886,1973,322],[887,1973,345],[887,1973,426],[887,1972,432],[887,1972,449],[887,1972,473]]
    # trace = choice(points)
    data = f'"{{"points":{trace} ,"distanceX":{distance / 310},"fp":"4dd3d0b50fafd97371c355f2c5655df3","address":"https://www.yunpian.com","yp_riddler_id":""}}"'
    data = {
        "points": trace,
        "distanceX": distance / 310,
        "fp": "4dd3d0b50fafd97371c355f2c5655df3",
        "address": "https://www.yunpian.com",
        "yp_riddler_id": "",
    }
    # 轨迹加密
    print(data)
    encrypt_data = ctx.call("encrypt_data", str(data))
    params = {
        "cb": get_cb(ctx),
        "i": encrypt_data["i"],
        "k": encrypt_data["k"],
        "token": init_data["token"],
        "captchaId": "974cd565f11545b6a5006d10dc324281",
    }
    print(params)
    # 发送加密验证
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    resp = requests.get(url, headers=headers, params=params, verify=False).text
    res = json.loads(resp.replace("ypjsonp(", "").replace(")", ""))
    print("-" * 10)
    print(res)


if __name__ == "__main__":
    crack()

