# Data Search Engine
Project description:<br />
•	Provided a tag rendering a Custom Search Engine input field and a view displaying search results.<br />
•	Web-crawling from well-known website of real data in python.<br />
•	Designed Scrapy-Redis distributed crawler development and database. <br />
•	Processed data into Elasticsearch engine, and used Django framework to build web application. <br />

﻿# Description:
 This projec is used to elastic search to search a certain prefix, and then display all the<br />
 information we have found. Ex: you type "java, then I will display all the result that contains this<br />
 keywords.<br />
 
 ## Screen Shot
#Suggest view
![home](https://user-images.githubusercontent.com/21152514/30788271-6e78c462-a14e-11e7-8f9d-709766b7966b.png) <br />
 #Search View
 ![search](https://user-images.githubusercontent.com/21152514/30788272-6e7945e0-a14e-11e7-8d7c-af719a25c4be.png) <br />
 
 ## The search engine has:
 Hot search list(The most frequency search)<br />
 Seach history<br />
 The number of results, pages, and times<br />
 The number of total data in the Database
 The information will be restored in the elasticSearch head <br />
 using the syntax of Kibana <br />
 
 
 ## Codes Description: 
 /ArticleSpider # This is where we write the python project to extract all the data from website <br />
 /LcvSearch #This is django website to search data according to what you have typed <br />
 /demo #This is the image / demo of my project <br />
 /database #This has the data base (Navicat) in .sql formate <br />
 
 ## The web crawle:
 https://www.zhihu.com <br />
 http://www.jobbole.com/ <br />
 https://www.lagou.com/ <br />
 
 ## DataBase:
 Navicate
 
 ## Requirements
 Python Version:3.50 <br />
 elasticsearch:5.11 <br />
 kibana-5.1.2-windows-x86 <br />
 Redis 4.0 <br />
 elasticsearch-head <br />
 https://github.com/mobz/elasticsearch-head <br />
 IDE: PyCharm<br />
 Django-admin --version 1.11.3<br />
