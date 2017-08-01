# coding=utf-8
'''
@author: comwrg
@time  : 2017.05.21 18:28
'''
import requests
from bs4 import BeautifulSoup

def getList(url):
    '''
    
    :param url: 
    :return: [(歌名, 歌手, 专辑), ...]
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print r.text

    songnameList = soup.find_all('span', class_='songlist__songname_txt')
    # [<span class="songlist__songname_txt"><a href="javascript:;" title="趁早">趁早</a></span>,
    songnameList = map(lambda x:x.text, songnameList)

    singerList = soup.find_all('div', class_='songlist__artist')
    # [<a href="javascript:;" title="张惠妹" class="singer_name">张惠妹</a>, ...

    def f(x):
        s = ''
        for i in x:
            s += i.string.strip()
        return s


    singerList = map(f, singerList)
    #print singerList

    albumList = soup.find_all('div', class_='songlist__album')
    # [<div class="songlist__album">
    # <a href="javascript:;" title="不顾一切">不顾一切</a>
    # </div>,
    albumList = map(lambda x:x.text.strip(), albumList)
    #print len(songnameList), len(singerList), len(albumList)
    return [(songnameList[x], singerList[x], albumList[x]) for x in range(len(songnameList))]



if __name__ == '__main__':
    print(getList('https://y.qq.com/n/yqq/playlist/3363492195.html'))
