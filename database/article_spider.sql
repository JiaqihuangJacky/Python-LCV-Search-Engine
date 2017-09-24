/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.237
Source Server Version : 50718
Source Host           : 192.168.1.237:3306
Source Database       : article_spider

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2017-09-21 19:00:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `add_time` datetime DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `id` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for jobbole_article
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article` (
  `title` varchar(200) NOT NULL DEFAULT '',
  `url` varchar(300) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(300) DEFAULT NULL,
  `praise_nums` int(11) DEFAULT '0',
  `comment_nums` int(11) DEFAULT '0',
  `tags` varchar(100) DEFAULT NULL,
  `content` longtext,
  `url_object_id` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for zhihu_answer
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_answer`;
CREATE TABLE `zhihu_answer` (
  `zhihu_id` bigint(20) NOT NULL DEFAULT '0',
  `url` varchar(300) NOT NULL,
  `question_id` bigint(20) NOT NULL DEFAULT '0',
  `author_id` varchar(100) DEFAULT NULL,
  `content` longtext NOT NULL,
  `parise_num` int(11) NOT NULL DEFAULT '0',
  `comments_num` int(11) NOT NULL DEFAULT '0',
  `create_time` date NOT NULL,
  `update_time` date NOT NULL,
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for zhihu_question
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_question`;
CREATE TABLE `zhihu_question` (
  `zhihu_id` bigint(20) NOT NULL DEFAULT '0',
  `topics` varchar(255) DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `answer_num` int(11) NOT NULL DEFAULT '0',
  `comments_num` int(11) NOT NULL DEFAULT '0',
  `watch_user_num` int(11) NOT NULL DEFAULT '0',
  `click_num` int(11) NOT NULL DEFAULT '0',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
