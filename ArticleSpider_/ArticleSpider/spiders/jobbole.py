# -*- coding: utf-8 -*-
import re #to strip
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader #loader in scrapy
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #call this function for download
    def parse(self, response):
        #get all the url and return to scrapy and download and update
        #get all article's url, after download and send it to parse
        #extract will create an array
        #response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract() will give us array
        #response.css("#archive .floated-thumb .post-thumb a::attr(href)") gives us a nodes
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            #call back function to call get the article's information
            #urljoin make the response.url + post_url

            #get nodes' the image
            image_url = post_node.css("img::attr(src)").extract_first("")

            #get nodes's url
            post_url = post_node.css("::attr(href)").extract_first("")

            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},callback=self.parse_detail)
            #get the next page and let scrapy to download

        #This is used to get the next url
        #Using attr the get the url
        #extract first is used for the error checking, and "" is default
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")

        #if we have this value then we join the url together
        #send the next page to scrapy to download
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)



    #get ariticle's certain information / div
    def parse_detail(self, response):

        #make an instance call article_item
        article_item = JobBoleArticleItem()

        #send to the pipeline.py, let it receive it
        #using item loader to load the items
        #getting all item via loadering item
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        # assgin the loader into the item
        article_item = item_loader.load_item()

        yield article_item


