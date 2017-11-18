import unittest
from NetEaseMusic import *


class Test_xMusicWeb(unittest.TestCase):
    def test_qq(self):
        l = qq.getList('https://y.qq.com/n/yqq/playlist/3363492195.html')
        self.assertEqual(len(l), 159)

if __name__ == '__main__':
    unittest.main()
