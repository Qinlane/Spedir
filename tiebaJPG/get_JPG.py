from urllib import request
import re,os

def get_html(url):
    # 构建请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    req=request.Request(url,headers=headers)

    #打开网页
    reqopen=request.urlopen(req)

    #读取页面源码
    htmlcode=reqopen.read().decode('utf-8')
    return htmlcode

# with open('jpgCode.html', 'w', encoding='utf-8') as f:
#     f.write(get_html('https://movie.douban.com/typerank?type_name=%E5%8A%A8%E7%94%BB%E7%89%87&type=25&interval_id=100:90'))
#     f.close()


if __name__ == '__main__':

    #除了换行外的其它任意字符  禁止贪婪  reg = r'src="(.+?\.jpg)" width'
    reg=r'src="(.+?\.jpg)" size'

    # reg=r'<img class="BDE_Image" pic_type="0" width="512" height="724" src="(.*?)" .*?">'
    #将正则表达模式编译成一个正则表达对象
    reg_img=re.compile(reg)
    #从头到尾进行检索，匹配所有符合规则的字符串，返回列表
    imglist=reg_img.findall(get_html('https://tieba.baidu.com/p/5633501922'))

    x=0
    for i in imglist:
        print(i)
        #将图片下载到本地
        request.urlretrieve(i,'C:/Users\Yukli\Pictures/FGO/%x.jpg' %x)
        x+=1

