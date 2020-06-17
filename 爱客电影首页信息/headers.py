import re

s = """
formhash: 64e6fa
txt_account: kingvstr@hotmail.comdf
pwd_password: 9734f5071119d2c8ef17f8577e1e0e2c
login_type: 3
ckb_cookie: 0
hdn_refer: https://www.epwk.com/
txt_code: 2264
pre: login
inajax: 1
"""

import sys

x = sys.argv[1]

res = re.sub("(?P<key>.*?): (?P<val>.*?)\n", "'\\1': '\\2',\n ", x)
print(res)


# test = "Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
# ret = re.search("(?P<key>.*?): (.*?)$", test)

# print(ret.group(2))
