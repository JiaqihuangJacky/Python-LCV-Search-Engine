# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ArticleSpider.items import LagouJobItem, LagouJobItemLoader

#using CrawlSpider to get all the data from lagou.com
class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        # get the match 'category.php', (but it does not match 'subsection.php')'s link
        # if not callback then means follow's default is true
        Rule(LinkExtractor(allow=('www.lagou.com/zhaopin/Java/',), )),

        # get the match 'item.php' s link, and then use spider's parse_item to analyze
        Rule(LinkExtractor(allow=('www.lagou.com/jobs/',)), callback='parse_job'),
    )

    def parse_job(self, response):
        #get lagou's website data
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name span::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("salary", ".salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")

        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("company_name", "#job_company dt a div h2::text")
        lagou_item = item_loader.load_item()
        print("here")
        pass
#       return lagou_item
