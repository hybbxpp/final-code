# -*- coding: utf-8 -*-

BOT_NAME = 'leedsdig'

SPIDER_MODULES = ['leedsdig.spiders']
NEWSPIDER_MODULE = 'leedsdig.spiders'

MYSQL_URI = "127.0.0.1"
MYSQL_DATABASE = "medicine"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'leedsdig.pipelines.MysqlPipeline': 300,
}

