
import scrapy
import json
import re


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']

    def start_requests(self):
        base_url = 'https://www.douban.com/j/explore/rec_feed?start={}&max_id=None&count=30'
        for i in range(30,61,30):
            url = base_url.format(i)
            req = scrapy.Request(url=url, callback=self.parse)
            # 第一种方式
            req.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            yield req

    def parse(self,response):
        res_dict = json.loads(response.text)
        html_str = res_dict['html']

        pattern = 'https://www.douban.com/gallery/topic/(\d+)/'
        topic_id_list = re.findall(pattern,html_str)

        for topic_id in topic_id_list:
            base_url = 'https://m.douban.com/rexxar/api/v2/gallery/topic/{}/items?sort=hot&start=0&count=20&status_f'
            url = base_url.format(topic_id)
            req = scrapy.Request(url=url)
            req.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            yield req
            break

    def parse_topic(self,response):
            res_dict = json.loads(response.text)
            items_list = res_dict['items']

            for item in items_list:
                if 'url' in items_list:
                    url = item['traget']['url']
                    print('-------------------'*10)
                    # 为note添加一个request，处理存储的Mysql的情况
                    req = scrapy.Request(url,callback = self.parse_note)
                    req.headers[ 'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
                    yield req



            


