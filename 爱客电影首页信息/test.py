import asyncio
import aiohttp
from lxml import html
import re


res = []


async def get_queue(session: aiohttp.ClientSession, queue: asyncio.Queue):
    type_url = "http://www.aiaiaike.com/type/1.html"
    async with session.get(type_url) as resp:
        sel = html.fromstring(await resp.text())
        lis = sel.xpath('//li[@class="vbox"]')

        for li in lis:
            li_url = li.xpath("./a/@href")[0]
            title = li.xpath("./a/@title")[0]
            img_url = li.xpath("./a/@style")[0].replace(r"background-image: url(", "")
            res = re.search("/(\d+)\.html", li_url)
            url_id = res.group(1)
            # queue.put_nowait(f"http://www.aiaiaike.com/play/{url_id}.html")
            queue.put_nowait(
                {
                    "title": title,
                    "img": img_url,
                    "play_url": f"http://www.aiaiaike.com/play/{url_id}.html",
                }
            )


async def get_res(session: aiohttp.ClientSession, queue: asyncio.Queue):
    while True:
        try:
            res_data = queue.get_nowait()
            play_url = res_data["play_url"]
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
            }
            resp = await session.get(play_url, headers=headers)
            html_str = await resp.text("utf-8", "ignore")
            res = re.search('scrolling="no" src="(.*?)"', html_str, re.S)

            url = res.group(1).replace("wap123", "dapi")

            resp = await session.get(url)
            res = await resp.text()

            res = re.search('scrolling="no" src="(.*?)"', res, re.S)

            # ip
            if res:
                api_url = res.group(1)
            else:
                return

            resp = await session.get(api_url)
            api_res = await resp.text()

            url = re.search("'url':'(.*?)'", api_res, re.S)

            iurl = url.group(1)

            url = "https://qq.79da.com/api.php"

            import time

            data = {
                "url": iurl,
                "referer": "aHR0cDovL2FwaS50aWFueGlhbmxlLmNvbS9qeC9kYXBpLnBocD9pZD1xS3AxbmFLaHFhYWpsbktwMDgxcVphS3FaQU8wTzBPTzBPME8maGVpZ2h0PTM2MHB4",
                "ref": "0",
                "time": f"{int(time.time())}",
                "type": "",
                "other": "a",
                "ios": "0",
            }

            headers = {
                "authority": "qq.79da.com",
                "pragma": "no-cache",
                "cache-control": "no-cache",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "x-requested-with": "XMLHttpRequest",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://qq.79da.com",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
            }

            resp = await session.post(url, data=data, headers=headers)
            response = await resp.text()

            import json

            url = json.loads(response)

            url = url["url"]
            title = res_data["title"]
            img = res_data["img"]

            # print([url, title, img])
            return {"url": url, "title": title, "img": img}

        except asyncio.QueueEmpty as e:
            return


async def main():
    global res
    async with aiohttp.ClientSession() as session:
        queue = asyncio.Queue()
        await get_queue(session, queue)
        tasks = [asyncio.ensure_future(get_res(session, queue)) for _ in range(10)]

        await asyncio.gather(*tasks)
        for task in tasks:
            res.append(task.result())


asyncio.run(main())
