# -*- coding: utf-8 -*-
import scrapy,time,json,re
from scrapy.linkextractors import LinkExtractor

from demo.items import QiutanInfoItem
from demo.items import QiutanPlayerItem
from demo.items import QiutanGameItem


class QiutanSpider(scrapy.Spider):
    name = 'qiutan'
    allowed_domains = ['zq.win007.com','bf.win007.com']
    # start_urls=['http://zq.win007.com/jsData/matchResult/2013-2014/s36.js?version=2019042919']
    now = time.strftime('%Y%m%d%H', time.localtime(int(time.time())))
    troops = {}
    def start_requests(self):
        base_url = 'http://zq.win007.com/jsData/matchResult/201{}-201{}/s36.js?version={}'
        for i in range(4, 9):
            # url = base_url.format(i, i + 1, self.now)
            # req=scrapy.Request(url=url, callback=self.parse)
            # req.headers[ 'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            # req.headers['referer'] = 'http://zq.win007.com/cn/League/2015-2016/36.html'
            # yield req

            url_list = 'http://zq.win007.com/jsData/teamInfo/team36.js?version={}'
            url_list = url_list.format(self.now)
            req = scrapy.Request(url=url_list, callback=self.parse_player_list)
            req.headers[  'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            req.headers['referer'] = 'http://zq.win007.com/cn/League/2015-2016/36.html'
            yield req


    def parse_player_list(self,response):
        pattern_list = 'var arrTeam = (.*?);'
        team_list_score = self.spiderman(response, pattern=pattern_list)
        troops_list = []
        for num_s in team_list_score:
            troops_list.append(num_s[0])
            # print(num_s)
        for i in troops_list:
            id = i
            base_url = 'http://zq.win007.com/jsData/teamInfo/teamDetail/tdl{}.js?version={}'
            url = base_url.format(id, self.now)
            # print(url)
            req = scrapy.Request(url=url, callback=self.parse_player)
            req.headers[ 'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
            req.headers['referer'] = 'http://zq.win007.com/cn/team/Summary/{}.html'.format(i)
            yield req

    def spiderman(self, response, pattern):
        score_match = re.search(pattern, response.text)
        list_score = score_match.group(1)
        # team_list = eval(list_score)
        list_score = list_score.replace(',,,', ',"","",')
        list_score = list_score.replace(' ', '.')
        list_score = list_score.replace("'", '"')

        list_score = json.loads(list_score)
        return list_score

    def parse(self, response):
        # print(response.text)
        # with open('01.html','wb') as f:
        #     f.write(response.boday)
        for i in range(3, 9):
            print('201%i' % i, '-', '201%i' % (+i + 1))
            # print(response.text)
            pattern = 'var arrTeam = (.*?);'
            team_list = self.spiderman(response, pattern)
            # print(team_list)
            for num in team_list:
                self.troops.setdefault(num[0], num[1])

                # 清洗比分信息
            for d in range(1, 39):
                score_info = 'jh\["R_{}"\] = (.*?);'.format(d)
                team_list_score = self.spiderman(response, pattern=score_info)
                item=QiutanInfoItem()
                for sc in team_list_score:
                    item['d']=d
                    item['sid'] = sc[0]
                    item['time'] = sc[3]
                    item['score'] = sc[6]
                    item['ban_score'] = sc[7]
                    item['concede_points'] = str(sc[10]) + '/' + str(sc[11])
                    item['dx'] = sc[12] + '/' + sc[13]

                    item['host_id'] = self.troops[sc[4]]
                    item['guest_id'] = self.troops[sc[5]]
                    # print(self.troops,type(self.troops))
                    print(item['sid'], item['d'], item['time'], item['host_id'], item['score'] , item['guest_id'],item['ban_score'], item['concede_points'], item['dx'] )

                    url = 'http://bf.win007.com/Count/{}cn.htm'.format(item['sid'])
                    req=scrapy.Request(url=url,callback=self.parse_game)
                    yield req

    def parse_player(self,response):
        pattern = 'var teamDetail = (.*?)];'
        res_match = re.search(pattern, response.text)
        list_str = res_match.group(1)
        list_str = list_str + ']'
        list_str = list_str.replace('<br />', '.')
        team_list = eval(list_str)

        name = team_list[1] + '/' + team_list[3]
        city = team_list[5] + '/' + team_list[7]
        home = team_list[8]
        time = team_list[12]
        address = team_list[15]

        # 球队特点
        pattern = 'var teamCharacter = (.*?);'
        team_list_s = self.spiderman(response, pattern)
        style_list = []
        for style in team_list_s:
            style_list.append(style[2:])

        print('队名:', name, '成立时间:', time, '所在城市:', city, '主场:', home, '联系地址:', address)

        print('球队特点:', style_list)
        # 数据统计板块
        pattern = 'var countSum = (.*?);'
        team_list_b = self.spiderman(response, pattern)
        score_data_list = team_list_b[0][2:]
        print('球队数据:', score_data_list)
        style_list = str(style_list)
        score_data_list = str(score_data_list)
        player_list=[]
        player_list.extend([name,time,city,home,address,style_list,score_data_list])
        player_list = ','.join([item.strip() for item in player_list if item.strip != ''])

        item=QiutanPlayerItem()
        item['player_list']=player_list

        yield item
        print('----' * 30)

    def parse_game(self,response):
        player_list = []
        player = response.xpath('//div[@class="content"]//tr[position()>2]//text()').extract()
        for i in player:
            i = i.strip()
            player_list.append(i)

        for i in player_list:
            if i == '':
                player_list.remove(i)
        player_list = ','.join([item.strip() for item in player_list if item.strip != ''])
        print(type(player_list),player_list)

        item = QiutanGameItem()
        item['score_list'] = player_list

        yield item