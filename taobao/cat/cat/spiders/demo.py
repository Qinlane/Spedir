# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib import parse
from cat.items import TaobaoItem

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['https://s.taobao.com/']

    # start_urls = ['http://https://www.qidian.com//']
    # https://s.taobao.com/search?q= 关键字 &sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=44
    base_url = 'https://s.taobao.com/search?q={}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&s={}'

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Cookie' : 'cna=NFInFTPVqTgCATsqGLgFQ4d1; thw=cn; miid=1330477951655353058; hng=CN%7Czh-CN%7CCNY%7C156; t=2f5a15b9867db976cd3b5ffab30a173e; UM_distinctid=16bc1151750e9-00938359af5a5e-5a40201d-1fa400-16bc11517513a5; tracknick=lo386362711; tg=0; enc=m9nigdQKYVcP22qxvOZ7NJKOrAw8fPWMpTf2pQ809vtuOKvDytuvl%2FaugxKpBrTun152FqyQmAPXue3QDXcAhQ%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _cc_=V32FPkk%2Fhw%3D%3D; _m_h5_tk=aad9e635bc8b1a4b2014f61565147e25_1567333209178; _m_h5_tk_enc=cd33be0fcc49a9d7ed02e2c9e3313462; cookie2=17dff283a6b56cb6f378ed9b53b6be3e; _tb_token_=7e1fe3eb8eee6; v=0; unb=1100009087; uc3=nk2=D8yjt9N8%2BdmtdQY%3D&vt3=F8dBy3MGZEX%2FpOcsdxc%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&id2=UoCJiFcegFQGeg%3D%3D; csg=f2866fd5; lgc=lo386362711; cookie17=UoCJiFcegFQGeg%3D%3D; dnk=lo386362711; skt=e75c393fa895116a; existShop=MTU2NzM2MTkzNA%3D%3D; uc4=id4=0%40UOg1wHHWw%2BMlSQ7%2F7ZSLPe7fu79m&nk4=0%40De%2BJWoeevS5GaVqqCYlKEjMNjSMw%2Bg%3D%3D; _l_g_=Ug%3D%3D; sg=177; _nk_=lo386362711; cookie1=AnPC9YJQ3EMeayhak9khSoRHdIi5hgGbDwMWt6t9tA8%3D; alitrackid=login.taobao.com; mt=ci=23_1; swfstore=86185; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=UtASsssmeWzt&cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&pas=0&cookie14=UoTaH0Qh%2BCnhog%3D%3D&tag=8&lng=zh_CN; lastalitrackid=www.taobao.com; JSESSIONID=39F9F3C4F2CE80D1C09AFF0849CF39FF; l=cBQOdikPv-dPHr4CBOCNCuI8L17OSIRvIuPRwCmXi_5dY6Y6JFbOkkE28Fv6VjWd9VLB4wIEhpy9-etuiMgP9P--g3fP.; isg=BFpa87Iy0zmODF5awzqCsFDIqwC8I98CkR2stGTTBu241_oRTBsudSClp-NuLlb9; whl=-1%260%260%261567362711196',
            # 'referer': 'https://www.taobao.com/?spm=a230r.1.0.0.163217c5kg7C4c',
            # 'set-cookie' : 'JSESSIONID=38F75039F13EDA22CA52D74C9E18A72B; Path=/; HttpOnly',
        }
    }
    def start_requests(self):
        # 统一将常量放在setting.py文件
        # key_words = '女装'
        key_words = input('请输入商品关键字:')

        # key_words = parse.quote(key_words,' ').replace(' ','+')
        page_num = self.settings['PAGEM_NUM']
        one_page_count = self.settings['ONE_PAGEM_COUNT']
        for i in range(page_num):
            url = self.base_url.format(key_words,i*one_page_count)
            req = scrapy.Request(url=url,callback=self.parse, meta={'dont_redirect': True,'handle_httpstatus_list': [302]},)
            yield req


    def parse(self, response):
        p = 'g_page_config = ({.*?});'
        g_page_config = response.selector.re(p)[0]
        g_page_config = json.loads(g_page_config)
        auctions = g_page_config['mods']['itemlist']['data']['auctions']
        print(auctions)
        for auction in auctions:
            # 实例化item
            item = TaobaoItem()
            item['price'] = auction['view_price']
            item['sales'] = auction['view_sales']
            item['title'] = auction['raw_title']
            item['nick'] = auction['nick']
            item['loc'] = auction['item_loc']
            item['detail_url'] = auction['detail_url']

            yield item


