# -*- coding: utf-8 -*-

__author__ = 'bobby'

from scrapy.cmdline import execute

import sys
import os # used for path

#get the article path
#setting up the path must be in the project path
#must be in the projec D:\LinuxShare\ArticleSpider
#sys.path.append("D:\LinuxShare\ArticleSpider")
#print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "lagou"])


