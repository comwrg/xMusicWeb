"""
@author: comwrg
@time  : 2017.05.21 18:28
"""
from . import qq, _163
import HTMLParser


def getKwl(url):
    '''
    
    :param url: 
    :return: return kwl text
    '''

    info = getList(url)
    if info == False:
        return False

    kwl = ''
    for item in info:
        kwl += '    <so name="%s." artist="%s" album=""></so>\r\n' % (item[0].replace('"', ''), item[1])
    kwl = '<so>\r\n%s</so>' % kwl

    kwl = HTMLParser.HTMLParser().unescape(kwl)
    kwl = kwl.encode('gb2312', errors='ignore')
    return kwl

def getList(url):
    '''
    
    :param url: 
    :return:[(songname, artistname, albumname), ..] 
    '''

    url = url.lower()
    url_nohttp = url[:]
    url_nohttp = url_nohttp.replace('https://', '')
    url_nohttp = url_nohttp.replace('http://' , '')
    if url_nohttp.startswith('y.qq.com'):
        obj = qq
    elif url_nohttp.startswith('music.163.com'):
        obj = _163
    else:
        return False
    return obj.getList(url)

def diff(url1, url2):
    '''
    
    :param url1: 
    :param url2: 
    :return: 
    
    '''
    l1 = getList(url1)
    l2 = getList(url2)

    def diff(l, l_base):
        '''
        
        :param l: 
        :param l_base: 
        :return:
        '''
        diff = []
        for data1 in l:
            isFind = False
            for data2 in l_base:
                if data1 == data2:
                    isFind = True
                    break

            if not isFind:
                diff.append(data1)
        return diff

    return diff(l1, l2), diff(l2, l1)

if __name__ == '__main__':
    # print getList('https://y.qq.com/n/yqq/playlist/3363492195.html')
    print(diff(
        'https://y.qq.com/n/yqq/playlist/3363492195.html',
        'http://music.163.com/#/playlist?id=98176052'
    ))