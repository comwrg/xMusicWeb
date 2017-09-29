# coding=utf-8
'''
@author: comwrg
@time  : 2017.05.21 18:28
'''
import requests
import re

def getList(url):
    '''
    
    :param url: 
    :return: [(歌名, 歌手, 专辑), ...]
    '''
    id = re.search(r'playlist/(\d*)\.html', url).group(1)

    r = requests.get('https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid={id}&format=json'.format(id=id),
                     headers={
                         "Referer": "https://y.qq.com/n/yqq/playlist/{id}.html".format(id=id)
                     })
    songlist = r.json()['cdlist'][0]['songlist']

    songnameList = []
    singerList = []
    albumList = []
    for song in songlist:
        # get song name
        songnameList.append(song['songname'])

        # get singer
        singers = [singer['name'] for singer in song['singer']]
        singerList.append('/'.join(singers))

        # get album
        albumList.append(song['albumname'])

    return [(songnameList[x], singerList[x], albumList[x]) for x in range(len(songnameList))]



if __name__ == '__main__':
    print(getList('https://y.qq.com/n/yqq/playlist/3363492195.html'))
