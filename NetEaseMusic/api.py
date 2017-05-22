# coding=utf-8
'''
@author: comwrg
@license: MIT
@time : 2017/05/22 09:39
@desc : 
'''
import base64
import hashlib
import json
import os

import binascii

import requests
from Crypto.Cipher import AES

# copy from https://github.com/darknessomi/musicbox/blob/master/NEMbox/api.py

modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'
default_timeout = 10

def encrypted_id(id):
    magic = bytearray('3go8&$8*3*3h0k(2)2', 'u8')
    song_id = bytearray(id, 'u8')
    magic_len = len(magic)
    for i, sid in enumerate(song_id):
        song_id[i] = sid ^ magic[i % magic_len]
    m = hashlib.md5(song_id)
    result = m.digest()
    result = base64.b64encode(result)
    result = result.replace(b'/', b'_')
    result = result.replace(b'+', b'-')
    return result.decode('utf-8')

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return binascii.hexlify(os.urandom(size))[:16]


def encrypted_request(text):
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    #print data
    return data

class NetEaseMusicApi():
    # 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36',  # NOQA
            'cookie':
            '_ntes_nnid=a7bf79773a3128c4733932a33e6f13b5,1493340796082; _ntes_nuid=a7bf79773a3128c4733932a33e6f13b5; usertrack=c+5+hlkCpZsyqjG6CU7kAg==; _ga=GA1.2.1572173646.1493345694; vjuids=-bf07d3ee.15c2b52874a.0.0b92410ebd9be; vjlast=1495375448.1495375448.30; vinfo_n_f_l_n3=94ce1beaf653d826.1.0.1495375447909.0.1495375465913; _ngd_tid=WAS7RCF7olmXo8tlartLNqsYzcOv%2F2Xb; JSESSIONID-WYYY=8K81msY4AErPPRT6l2Gxjjx7a6%2B%2F1ny6HoQD328x7KyJxcPBBJewRCRnygt7Z9s2BMg6VuY4MCDi7Hk4OIDTWXTEC%5COsQ9b4bNjkXY6s2Pxcfc0UZ7BHmgsRZk2fKy3pg4Ht9Ji8dq%5CtZzCMtnlRF5g179VgGZlPZgxffEEHjbFIAVb%2F%3A1495419325430; _iuqxldmzr_=32; __remember_me=true; MUSIC_U=e329119d102f8d1294e68465ab9716c137d6a6154acc3bd7ff6e5f821c068c47fd62e64b9aed029ac5261a4e7bdcd8b541049cea1c6bb9b6; __csrf=048a1c4dc2ec8d9ec8ba432750b75128; __utma=94650624.284725872.1493340797.1495410960.1495415785.9; __utmb=94650624.47.10.1495415785; __utmc=94650624; __utmz=94650624.1495372005.6.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        }
        self.cookies = {'appver': '1.5.2'}
        self.playlist_class_dict = {}
        self.session = requests.Session()
        self.session.cookies.set('appver', '1.5.2')


    def httpRequest(self,
                    method,
                    action,
                    query=None,
                    urlencoded=None,
                    callback=None,
                    timeout=None):
        connection = json.loads(
            self.rawHttpRequest(method, action, query, urlencoded, callback, timeout)
        )
        return connection

    def rawHttpRequest(self,
                       method,
                       action,
                       query=None,
                       urlencoded=None,
                       callback=None,
                       timeout=None):
        if method == 'GET':
            url = action if query is None else action + '?' + query
            connection = self.session.get(url,
                                          headers=self.header,
                                          timeout=default_timeout)

        elif method == 'POST':
            connection = self.session.post(action,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)



        #print self.session.cookies.items()
        connection.encoding = 'UTF-8'
        return connection.text

    def login_phone(self, phone, pwd):
        url = 'https://music.163.com/weapi/login/cellphone'
        body = {
            'phone': phone,
            'password': pwd,
            'rememberLogin': 'true'
        }

        return self.httpRequest('POST', url, encrypted_request(body))

    def search(self, s, stype=1, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        return self.httpRequest('POST', action, data)

    def daily_signin(self, type):
        action = 'http://music.163.com/weapi/point/dailyTask'
        text = {'type': type}
        data = encrypted_request(text)
        return self.httpRequest('POST', action, data)

    def create(self, name):
        '''
        
        创建歌单
        
        507: "歌单数量超过上限！",
        405: "你操作太快了，请休息一会再试！",
        406: "你操作太快了，请休息一会再试！"
        :return: 
        '''
        url = 'http://music.163.com/weapi/playlist/create?csrf_token=048a1c4dc2ec8d9ec8ba432750b75128'
        text = {'name': name}
        data = encrypted_request(text)
        return self.httpRequest('POST', url, data)

    def track(self, pid, tracks, op='add'):
        url = 'http://music.163.com/weapi/playlist/manipulate/tracks?csrf_token=048a1c4dc2ec8d9ec8ba432750b75128'
        # pid, 歌单编号
        #
        text = {
            'op':op,
            'pid':pid,
            #'tracks':tracks,
            'trackIds': str(tracks),
            #'csrf_token':''
        }
        data = encrypted_request(text)
        return self.httpRequest('POST', url, data)

if __name__ == '__main__':
    na = NetEaseMusicApi()
    #print na.login_phone('13301489219', 'comwrg.com')
    print na.search('为你写诗')
    #print na.track('736223407',[347230, 347231])
    #print na.create('5')['id']
