import requests,os
from lxml import etree


class Spider(object):
    def __init__(self):
        # 构造请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Referer": "https://www.mzitu.com"
        }
    k=1
    path = 'G:\Study\Spedir\meizitu'
    num = 191264 #目标url 上的编号 例：https://www.mzitu.com/191199
    def start_request(self):
        # 1. 获取整体网页的数据
        for i in range(1, 204):
            print('==========正在抓取%s页==========' % i)
            base_url='https://www.mzitu.com/{num}/{i}'.format(num=self.num,i=i)
            # response = requests.get("https://www.mzitu.com/page/" + str(i) + "/", headers=self.headers)
            response = requests.get(base_url, headers=self.headers)
            if response:
                html = etree.HTML(response.content.decode())
                self.xpath_data(html)
                self.k += 1

            else:
                print('到最后一页了~')
                break


    def xpath_data(self, html):
        # 2. 抽取想要的数据 标题 图片 xpath
        # src_list = html.xpath('//ul[@id="pins"]/li/a/img/@data-original')
        # alt_list = html.xpath('//ul[@id="pins"]/li/a/img/@alt')
        src_list = html.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@src')
        alt_list = html.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@alt')
        title = html.xpath('/html/body/div[2]/div[1]/h2')
        # 判断路径目录是否存在

        for src,alt in zip(src_list,alt_list):
            file_name = alt+'-'+str(self.k)+ '.jpg'
            response = requests.get(src, headers=self.headers)
            print('正在抓取图片：' + file_name)
            # 3. 存储数据 jpg with open
            try:
                savepath = self.path + '/' + alt + '/'
                if not os.path.exists(savepath):
                    os.makedirs(savepath)
                with open(savepath+file_name, 'wb') as f:
                    f.write(response.content)
            except:
                print('发生错误')

if __name__ == '__main__':
    spider = Spider()
    spider.start_request()
