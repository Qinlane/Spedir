# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QiutanInfoItem(scrapy.Item):
    d=scrapy.Field()
    sid=scrapy.Field()
    time=scrapy.Field()
    score = scrapy.Field()
    ban_score =scrapy.Field()
    concede_points=scrapy.Field()
    dx =scrapy.Field()

    host_id =scrapy.Field()
    guest_id = scrapy.Field()

    def get_insert_sql_and_teamdata(self):
        insert_sql = 'INSERT INTO qiutan_test(rank_id, rank, `time`, host_id, score, guest_id, concede_points, dx, ban_score)' \
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        data = (self['sid'], self['d'], self['time'], self['host_id'], self['score'], self['guest_id'], self['concede_points'], self['dx'], self['ban_score'])
        return insert_sql,data

class QiutanPlayerItem(scrapy.Item):
    player_list=scrapy.Field()

    def get_insert_sql_and_teamdata(self):
        insert_sql = 'INSERT INTO qiutan_player(player_list)VALUES(%s)'
        data = (self['player_list'])
        return insert_sql, data

class QiutanGameItem(scrapy.Item):
    score_list=scrapy.Field()

    def get_insert_sql_and_teamdata(self):
        insert_sql = 'INSERT INTO qiutan_games(score_list)VALUES(%s)'
        data = (self['score_list'])
        return insert_sql, data


# CREATE TABLE qiutan_games (id INT PRIMARY KEY AUTO_INCREMENT,
# score_list VARCHAR(1000)
# )DEFAULT CHARSET=utf8mb4;