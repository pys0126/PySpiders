import os
import time

import execjs
import requests
import re


def run_js(id: str, sign: str):
    js = execjs.compile('''
            const CryptoJS = require('crypto-js');
            function decrypt(_0xc9495b, _0x260a1a) {
                var _0x278ce1 = {};
                _0x278ce1['GgyDg'] = function(_0x3cbfea, _0x1fd6b9) {
                    return _0x3cbfea % _0x1fd6b9;
                }
                var _0x178791 = _0x278ce1, _0x1bfc3f = '';
                for (var i = 2; i < 18; i++) {
                    _0x1bfc3f += _0x178791['GgyDg'](_0x178791['GgyDg'](_0xc9495b, i), -0x1 * -0x1302 + 0xd1 * 0x13 + -0x227c)['toString']();
                }
                return HexStr = CryptoJS['enc']['Hex']['parse'](_0x260a1a),
                        Base64Str = CryptoJS['enc']['Base64']['stringify'](HexStr),
                        key = CryptoJS['MD5'](CryptoJS['enc']['Utf8']['parse'](_0xc9495b + _0xc9495b % (-0x125 * -0x13 + -0x59 * 0x26 + 0x440 * -0x2)))['toString']()['substr'](-0xa50 + 0x13 * 0x17b + 0x9d * -0x1d, 0xb4b + 0x1adf + 0x1 * -0x261a),
                        key = CryptoJS['enc']['Utf8']['parse'](key),
                        decrypt = CryptoJS['AES']['decrypt'](Base64Str, key, {
                            'iv': CryptoJS['enc']['Utf8']['parse'](_0x1bfc3f),
                            'mode': CryptoJS['mode']['CBC'],
                            'padding': CryptoJS['pad']['Pkcs7']
                        }),
                        JSON['parse'](decrypt['toString'](CryptoJS['enc']['Utf8']));
            }''')
    result = js.call("decrypt", id, sign)
    return result


def parms(url: str, headers):
    id = url.split("/")[-1]
    res = requests.get(url, headers=headers)
    title = re.findall(r'<title>(.*?)</title>', res.text, re.S)[0]
    sign = re.findall(r'<!--cacheSign:(.*?)-->', res.text, re.S)[0]
    return id, sign, title


def start(photo_url: str, headers):
    id, sign, title = parms(photo_url, headers)
    urls = [f"https://p.iimzt.com/{imgs}" for imgs in run_js(id=id, sign=sign)]
    item = 0
    for img_url in urls:
        item += 1
        img_res = requests.get(url=img_url, headers=headers)
        try:
            os.makedirs(f"./{title}")
        except Exception as e:
            pass
        with open(f"./{title}/{str(item)}.jpg", 'wb') as f:
            f.write(img_res.content)
        print(f"已保存: ./{title}/{str(item)}.jpg")


if __name__ == "__main__":
    start_time = time.time()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'referer': 'https://mmzztt.com/photo/'
    }
    url = "https://mmzztt.com/photo/58585"
    start(photo_url=url, headers=headers)
    stop_time = time.time()
    print(stop_time - start_time)
