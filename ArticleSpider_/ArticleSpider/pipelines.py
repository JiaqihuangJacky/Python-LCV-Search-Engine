# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs #This is used to avoid coding problems
import json #using json functions

#import the pipleline to get the image addresses
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import MySQLdb #connect to the database
import MySQLdb.cursors
from w3lib.html import remove_tags #remove all the tages


#this pipeline it process the item
class ArticlespiderPipeline(object):
    #process the item
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    #define json's file export
    #w is to write,
    def __init__(self):
        #codecs packages to open the files, encoding it using utf-8 to use chinese
        #characters.utf-8 to write the chinese characters
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    #process the item
    #ensure_ascii must be false, otherwise, the chinese character will be wrong
    def process_item(self, item, spider):
        #convert the data the dict, the ensure_ascii == false,
        #using false, otherwise, we are unable to write the chinese
        #characters.
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #then, we write to the file using write function
        self.file.write(lines)
        #return to deal with the next pipeline
        return item
    #close the file using spider_closed function
    def spider_closed(self, spider):
        self.file.close()

class MysqlPipeline(object):
    #write to the mysql
    def __init__(self):
        # host, user, password, dbname, charset's utf-8
        # using the unique codes
        # cursor to control the database
        # entering all of them by the user's id
        self.conn = MySQLdb.connect('192.168.1.237', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
        # manipulate the database
        self.cursor = self.conn.cursor()

    # using the sql to control the database
    # insert the data into the jobbole_article's database
    # passing to the title,url,create_data and fav_nums
    def process_item(self, item, spider):
        # passing 4 variables
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        # fill in the item's title, url,create_date, and fav_nums
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))

        # commit all the mysql languages
        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print (insert_sql, params)
        cursor.execute(insert_sql, params)



class JsonExporterPipleline(object):
    #define json's file export
    #using scrapy provided json export json files
    def __init__(self):
        #using scrapy provied json export's json file
        #open the file using binary file
        self.file = open('articleexport.json', 'wb')
        #using exporter open file using utf-8
        #ensuring we can use unquie character
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        #using exporter start to export
        self.exporter.start_exporting()

    #close the spider and finish exporting the file
    def close_spider(self, spider):
        #stop / finish export the item
        self.exporter.finish_exporting()
        #close the file
        self.file.close()

    #send the item into the exporter's item
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


#this pipeline it process the font images
#image.py can help us download the images
#and convert images, filter them
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item


class ElasticSearchPipeline(object):
    #write the da>ta into the ES
    def process_item(self, item, spider):
        item.save_to_es()
        return item