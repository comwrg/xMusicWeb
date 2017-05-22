# coding=utf-8
'''
@author: comwrg
@license: MIT
@time : 2017/05/22 18:08
@desc : 
'''

from setuptools import setup

setup(
   name='xMusicWeb',
   version='1.0',
   description='xMusicWeb',
   author='comwrg',
   author_email='xcomwrg@gmail.com',
   packages=['xMusicWeb'],  #same as name
   install_requires=['BeautifulSoup4', 'requests'], #external packages as dependencies
)