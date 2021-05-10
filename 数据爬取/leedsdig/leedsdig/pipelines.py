# -*- coding: utf-8 -*-

from leedsdig.settings import MYSQL_URI, MYSQL_DATABASE
import pymysql.cursors

class MysqlPipeline(object):
    def __init__(self):
        self.mysql_url = MYSQL_URI
        self.mysql_db = MYSQL_DATABASE

    def open_spider(self, spider):
        self.mysql_conn = pymysql.connect(
            host = self.mysql_url,
            user = "root",
            db = self.mysql_db,
            password = "19990423zzy",
            charset = "utf8mb4",
            cursorclass = pymysql.cursors.DictCursor
        )

    def process_item(self, item, spider):

        try:
            with self.mysql_conn.cursor() as cursor:
                sql_search = "SELECT * FROM `medicine` WHERE `通用名称`=%s"
                
                with self.mysql_conn.cursor() as cursor:
                    cursor.execute(sql_search, ("通用名称"))
                    
                    textIsExist = cursor.fetchone()
                    
                    if textIsExist is None:
                        sql_write = "INSERT INTO `medicine` (`通用名称`, `主要功能`, `性状`) VALUES (%s, %s, %s)"
                        cursor.execute(sql_write, (item.get("通用名称", ""), item.get("主要功能", ""), item.get("性状","")))


            self.mysql_conn.commit()
        except Exception as e:
            pass

        return item

    def close_spider(self, spider):
        self.mysql_conn.close()
