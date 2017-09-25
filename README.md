# Data Search Engine
Apr 2017 – Apr 2017<br />
Project description:<br />
•	Provided a tag rendering a Custom Search Engine input field and a view displaying search results.<br />
•	Web-crawling from well-known website of real data in python.<br />
•	Designed Scrapy-Redis distributed crawler development and database. <br />
•	Processed data into Elasticsearch engine, and used Django framework to build web application. <br />

﻿# Description:
 This projec is used to elastic search to search a certain prefix, and then display all the
 information we have found. Ex: you type "java, then I will display all the result that contains this
 keywords
 
 # The search engine has:
 Hot search list(The most frequency search)
 Seach history
 The number of results, pages, and times
 The number of total data in the Database
 The information will be restored in the elasticSearch head
 using the syntax of Kibana.
 
 
 # Codes Description: 
 /ArticleSpider # This is where we write the python project to extract all the data from website
 /LcvSearch #This is django website to search data according to what you have typed
 /demo #This is the image / demo of my project
 /database #This has the data base (Navicat) in .sql formate
 
# The web crawle:
 https://www.zhihu.com
 http://www.jobbole.com/
 https://www.lagou.com/
 
 # DataBase:
 Navicate
 
 # Requirements
 Python Version:3.50
 elasticsearch:5.11
 kibana-5.1.2-windows-x86
 Redis 4.0
 elasticsearch-head
 https://github.com/mobz/elasticsearch-head 
