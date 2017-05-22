"""
@author: comwrg
@time  : 2017.05.21 18:28
"""
import qq
import HTMLParser


def getKwl(url):
    '''
    
    :param url: 
    :return: return kwl text
    '''
    url = url.lower()
    if url.startswith('https://y.qq.com'):
        obj = qq
    else:
        return False

    info = obj.getList(url)
    kwl = ''
    for item in info:
        kwl += '    <so name="%s" artist="%s" album=""></so>\r\n' % (item[0], item[1])
    kwl = '<so>\r\n%s</so>' % kwl

    kwl = HTMLParser.HTMLParser().unescape(kwl)
    kwl = kwl.encode('gb2312', errors='ignore')
    return kwl

if __name__ == '__main__':
    getKwl('https://y.qq.com/n/yqq/playlist/3363492195.html')