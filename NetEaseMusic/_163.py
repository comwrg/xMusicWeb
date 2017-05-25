# coding=utf-8
'''
@author: comwrg
@license: MIT
@time : 2017/05/25 14:12
@desc : 
'''
import requests, json

def getList(url):
    '''

    :param url: 
    :return: [(歌名, 歌手, 专辑), ...]
    '''
    id = url[url.find('id=')+len('id='):]
    url = 'http://music.163.com/api/playlist/detail?id='+id
    r = requests.get(url)
    data = json.loads(r.text)
    l = []
    for track in data['result']['tracks']:
        songname = track['name']
        artistsname = track['artists'][0]['name']
        albumname = track['album']['name']
        l.append((songname, artistsname, albumname))
    return l



if __name__ == '__main__':
    print getList('http://music.163.com/#/playlist?id=98176052')