import requests, re, json, time, random
from lxml import etree
from qiutan.db import DB
from multiprocessing import Pool
from multiprocessing import Manager


class Spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Referer': 'http://zq.win007.com/cn/League/2013-2014/36.html',
            # 'Cookie': ' UM_distinctid=16a4e92d0c388-0a8e39accabd4d-5a40201d-1fa400-16a4e92d0c4116; detailCookie=null; CNZZDATA1261430177=299713168-1556095567-http%253A%252F%252Fwww.win007.com%252F%7C1556154968'
        }
        self.now = time.strftime('%Y%m%d%H', time.localtime(int(time.time())))

    # 把球队信息存进字典
    troops = {}
    def get_all_qtan_info(self,url,queue):
        base_url = 'http://zq.win007.com/jsData/matchResult/201{}-201{}/s36.js?version={}'
        for i in range(4, 9):
            url = base_url.format(i, i + 1, self.now)
            queue.put((self.qiudui_info, url))

        url_list = 'http://zq.win007.com/jsData/teamInfo/team36.js?version={}'
        url_list = url_list.format(self.now)
        response_list = requests.get(url=url_list, headers=self.headers)
        pattern_list = 'var arrTeam = (.*?);'
        team_list_score = self.spiderman(response=response_list, pattern=pattern_list)

        troops_list = []
        for num_s in team_list_score:
            troops_list.append(num_s[0])
        for i in troops_list:
            id = i
            base_url = 'http://zq.win007.com/jsData/teamInfo/teamDetail/tdl{}.js?version={}'
            url = base_url.format(id, self.now)
            queue.put((self.player,url))

    def qiudui_info(self,url,queue):
        mysqldb = DB()
        for i in range(3, 9):
            response = requests.get(url=url, headers=self.headers)
            print('201%i' % i, '-', '201%i' % (+i + 1))

            # print(response.text)
            pattern = 'var arrTeam = (.*?);'
            team_list = self.spiderman(response, pattern)
            # team_list = eval(team_list)
            # print(team_list, type(team_list))
            for num in team_list:
                self.troops.setdefault(num[0], num[1])

            # 清洗比分信息
            for d in range(1, 39):
                score_info = 'jh\["R_{}"\] = (.*?);'.format(d)
                team_list_score = self.spiderman(response, pattern=score_info)
                # team_list_score = eval(team_list_score)
                # print(team_list_score)
                # print(team_list)
                # sid=None
                for sc in team_list_score:
                    sid = sc[0]
                    time = sc[3]
                    score = sc[6]
                    ban_score = sc[7]
                    concede_points = str(sc[10]) + '/' + str(sc[11])
                    dx = sc[12] + '/' + sc[13]

                    host_id = self.troops[sc[4]]
                    guest_id = self.troops[sc[5]]
                    # print(self.troops,type(self.troops))
                    print(sid, d, time, host_id, score, guest_id, ban_score, concede_points, dx)
                    # print(type(sid), type(rank), type(time), type(host_id), type(score), type(guest_id), type(ban_score),
                    #       type(concede_points), type(dx))

                    insert_sql = 'INSERT INTO qiutan_test2(rank_id, rank, `time`, host_id, score, guest_id, concede_points, dx, ban_score)' \
                                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    data = (sid, d, time, host_id, score, guest_id, concede_points, dx, ban_score)
                    mysqldb.update(insert_sql, data)

                    url = 'http://bf.win007.com/Count/{}cn.htm'.format(sid)
                    queue.put((self.situation, url))
                    # self.situation(base_url_cn)
            print('----' * 30)
            import time
            time.sleep(random.randrange(3))
        # self.player()

    def spiderman(self, response, pattern):
        score_match = re.search(pattern, response.text)
        list_score = score_match.group(1)
        # team_list = eval(list_score)
        list_score = list_score.replace(',,,', ',"","",')
        list_score = list_score.replace(' ', '.')
        list_score = list_score.replace("'", '"')

        list_score = json.loads(list_score)
        return list_score

    def situation(self, url):
        print('函数3')
        mysqldb = DB()
        # url = 'http://bf.win007.com/Count/1552471cn.htm'
        # for i,j in self.troops.items():
        response = requests.get(url=url, headers=self.headers)
        html = etree.HTML(response.text)

        # 1
        qd_name = html.xpath('//div[@class="content"][3]/table/tr[1]//span/text()')
        qd_name = '\n'.join([item.strip() for item in qd_name if item.strip() != ''])
        print(qd_name)
        for n in range(3, 21):
            num = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[1]/text()'.format(n))
            num = '\n'.join([item.strip() for item in num if item.strip() != ''])

            name = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[2]/a/text()'.format(n))
            name = '\n'.join([item.strip() for item in name if item.strip() != ''])

            wz = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[3]/text()'.format(n))
            wz = '\n'.join([item.strip() for item in wz if item.strip() != ''])

            sm = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[4]/text()'.format(n))
            sm = '\n'.join([item.strip() for item in sm if item.strip() != ''])

            sz = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[5]/text()'.format(n))
            sz = '\n'.join([item.strip() for item in sz if item.strip() != ''])

            cq = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[6]/text()'.format(n))
            cq = '\n'.join([item.strip() for item in cq if item.strip() != ''])

            dr = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[7]/text()'.format(n))
            dr = '\n'.join([item.strip() for item in dr if item.strip() != ''])

            cqcs = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[8]/text()'.format(n))
            cqcs = '\n'.join([item.strip() for item in cqcs if item.strip() != ''])

            cqc = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[9]/text()'.format(n))
            cqc = '\n'.join([item.strip() for item in cqc if item.strip() != ''])

            cg = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[10]/text()'.format(n))
            cg = '\n'.join([item.strip() for item in cg if item.strip() != ''])

            hq = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[11]/text()'.format(n))
            hq = '\n'.join([item.strip() for item in hq if item.strip() != ''])

            zd = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[16]/text()'.format(n))
            zd = '\n'.join([item.strip() for item in zd if item.strip() != ''])

            stjq = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[17]/text()'.format(n))
            stjq = '\n'.join([item.strip() for item in stjq if item.strip() != ''])

            pf = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[30]/text()'.format(n))
            pf = '\n'.join([item.strip() for item in pf if item.strip() != ''])

            sj = html.xpath('//div[@class="content"][3]/table/tr[{}]/td[31]//@title'.format(n))
            sj = '\n'.join([item.strip() for item in sj if item.strip() != ''])
            print(num, name, wz, sz, sm, cq, dr, cqcs, cqc, cg, hq, zd, stjq, pf, sj)
        # 2
        qd_name = html.xpath('//div[@class="content"][4]/table/tr[1]//span/text()')
        qd_name = '\n'.join([item.strip() for item in qd_name if item.strip() != ''])
        print('----' * 30)
        print(qd_name)
        for n in range(3, 21):
            num = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[1]/text()'.format(n))
            num = '\n'.join([item.strip() for item in num if item.strip() != ''])

            name = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[2]/a/text()'.format(n))
            name = '\n'.join([item.strip() for item in name if item.strip() != ''])

            if name!='':
                wz = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[3]/text()'.format(n))
                wz = '\n'.join([item.strip() for item in wz if item.strip() != ''])

                sm = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[4]/text()'.format(n))
                sm = '\n'.join([item.strip() for item in sm if item.strip() != ''])

                sz = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[5]/text()'.format(n))
                sz = '\n'.join([item.strip() for item in sz if item.strip() != ''])

                cq = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[6]/text()'.format(n))
                cq = '\n'.join([item.strip() for item in cq if item.strip() != ''])

                dr = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[7]/text()'.format(n))
                dr = '\n'.join([item.strip() for item in dr if item.strip() != ''])

                cqcs = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[8]/text()'.format(n))
                cqcs = '\n'.join([item.strip() for item in cqcs if item.strip() != ''])

                cqc = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[9]/text()'.format(n))
                cqc = '\n'.join([item.strip() for item in cqc if item.strip() != ''])

                cg = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[10]/text()'.format(n))
                cg = '\n'.join([item.strip() for item in cg if item.strip() != ''])

                hq = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[11]/text()'.format(n))
                hq = '\n'.join([item.strip() for item in hq if item.strip() != ''])

                zd = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[16]/text()'.format(n))
                zd = '\n'.join([item.strip() for item in zd if item.strip() != ''])

                stjq = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[17]/text()'.format(n))
                stjq = '\n'.join([item.strip() for item in stjq if item.strip() != ''])

                pf = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[30]/text()'.format(n))
                pf = '\n'.join([item.strip() for item in pf if item.strip() != ''])

                sj = html.xpath('//div[@class="content"][4]/table/tr[{}]/td[31]//@title'.format(n))
                sj = '\n'.join([item.strip() for item in sj if item.strip() != ''])
                print(num, name, wz, sz, sm, cq, dr, cqcs, cqc, cg, hq, zd, stjq, pf, sj)
            else:
                continue

            insert_sql = 'INSERT INTO qiutan_people2(team_name, num, `name`, `position`, sm, sz, cq, dr, cqgr, cqc,' \
                         'cg, hq, zd, stjq, pf, sj)' \
                         'VALUES (%s, %s, %s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            data = (qd_name, num, name, wz, sz, sm, cq, dr, cqcs, cqc, cg, hq, zd, stjq, pf, sj)
            mysqldb.update(insert_sql, data)



    def player(self,url):
        mysqldb = DB()
        response = requests.get(url=url, headers=self.headers)
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
        print('----' * 30)

        style_list = str(style_list)
        score_data_list = str(score_data_list)

        insert_sql = 'INSERT INTO qiutan_score2(`name`, `time`, city, home, address, style, score_date)' \
                     'VALUES (%s, %s, %s, %s, %s, %s, %s)'
        data = (name, time, city, home, address, style_list, score_data_list)
        mysqldb.update(insert_sql, data)

        import time
        time.sleep(1)

    def run_all(self):
        # qiutan = self.qiudui_info()
        pool = Pool(5)
        #找到共享内存的内容
        queue=Manager().Queue()

        url = 'http://zq.win007.com/jsData/matchResult/2013-2014/s36.js?version={}'

        queue.put((self.get_all_qtan_info, url))

        while True:
            try:
                (func,tmp_url)=queue.get()
                pool.apply_async(func=func,args=(tmp_url,queue))
            except Exception as e:
                print(e)
                break

        pool.close()
        pool.join()
        print("主进程终止")


if __name__ == '__main__':
    sp = Spider()
    sp.run_all()

