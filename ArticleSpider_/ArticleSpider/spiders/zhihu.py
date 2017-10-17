# -*- coding: utf-8 -*-
import json
import scrapy
import re
import time
import datetime
import scrapy
# using python 2 and 3
try:
    import urlparse as parse
except:
    from urllib import parse


from PIL import Image # image PTL open methond will open the file
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    }

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                print("match")
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                print("No match")
                pass
                #yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        # get all the questions items
        if "QuestionHeader-title" in response.text:
            print("Using new version")
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath("title", '//h1[@class="QuestionHeader-title"]/text()')
            item_loader.add_xpath("content", '//div[@class="QuestionHeader-detail"]//span')
            item_loader.add_value('url', response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_xpath('answer_num', '//h4[@class="List-headerText"]/span/text()')  # r'(^\d+).*'
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_xpath('watch_user_num', '//div[@class="NumberBoard-value"]/text()')
            item_loader.add_xpath('topics', '//div[@class="Popover"]/div/text()')
            question_item = item_loader.load_item()

        else:
            # old version item
            print("Using old version")
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            # we need to use xpath, since we need to use or relationship
            # the data is in a or in the span so we need to sue xpath
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # we need to use xpath again since we need to use or relationship
            # for this extraction
            item_loader.add_xpath("watch_user_num",
                                  "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()

        yield scrapy.Request(url=self.start_answer_url.format(question_id, 3,20), headers=self.headers, callback=self.parse_answer)
        yield question_item


    #在这里处理question 的 answer
    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json['paging']['is_end']
        next_url = ans_json['paging']['next']

        for answer in ans_json['data']:

            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()
            yield answer_item
        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    # callback will use the login function
    def start_requests(self):
        #current time * 100 and convert int to string
        t = str(int(time.time() * 1000))
        #get the validation image's link
        captcha_url = "https://www.zhihu.com/captcha.gif?r=%s&type=login" % (t)
        return [scrapy.Request(captcha_url, headers=self.headers, callback=self.get_captcha)]

    #we get the Verification code and open
    def get_captcha(self, response):
        if response.status == 200:
            #open a file call xx.jpg and save the image
            #binary open wb, and write the content into the image
            with open('captcha.jpg', 'wb') as f:
                f.write(response.body)
                f.close()
            try:
                with Image.open('captcha.jpg') as im:
                    #display the image
                    im.show()
                    im.close()
            #error
            except:
                pass
            return [scrapy.Request(url = "http://www.zhihu.com/", headers=self.headers, callback=self.login)]

    def login(self, response):
        # get xsrf's value
        response_text = response.text
        match_obj = re.findall(r'.*name="_xsrf" value="(.*?)"/>', response.text)
        xsrf = ''
        captcha = input("Enter the validation code：\n>")

        if match_obj:
            xsrf = match_obj[0]
        if xsrf:
            return [scrapy.FormRequest(
                url="https://www.zhihu.com/login/email",
                formdata={
                    #enter all the login in information
                    '_xsrf': xsrf,
                    'email': "jasonchenoh@gmail.com",
                    'password': "admin123",
                    'captcha': captcha
                },
                headers=self.headers,
                callback=self.check_login
            )]

    def check_login(self, respone):
        # check if login in successfuly
        text_json = json.loads(respone.text)
        if 'msg' in text_json and text_json['msg'] == '登录成功':
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)
        else:
            print("Login in fail")
