# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from demo.db import DB

class DemoPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLPipeline(object):
    def __init__(self):
        self.helper= DB()

    def process_item(self,item,spider):
        if hasattr(item,'get_insert_sql_and_teamdata'):
            insert_sql,data=item.get_insert_sql_and_teamdata()
            self.helper.update(insert_sql,data)

        return item



