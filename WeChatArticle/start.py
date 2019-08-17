from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import os,re,requests,time,json,random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
}

path = 'G:\Study\Spedir\WeChatArticle/'

#文章类
class Article():
    def __init__(self,pubdate,savepath,imgsavepath,title):
        self.pubdate = pubdate
        self.savepath = savepath
        self.imgsavepath = imgsavepath
        self.title = title
# 读取文件
def ReadFile(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        all_the_text = f.readlines()

        return all_the_text

#时间戳转日期
def Timestamp_now(stampstr):
    dt = datetime.utcfromtimestamp(stampstr)
    dt = dt + timedelta(hours=8)
    newtimestr = dt.strftime("%Y%m%d_%H%M%S")
    return newtimestr

# 构建请求头
def jsondata(url):
    # 构建请求头
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text
        htmltxt = json.loads(html)
        return htmltxt
    else:
        return None


def DownLoadHtml(url):

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        htmltxt = response.text  # 返回的网页正文
        return htmltxt
    else:
        return None

# 下载文章页
def GetArtic(html):
    ArtList = []
    dict = html["general_msg_list"]
    dict = json.loads(dict)
    imgindex = 0
    for x in dict['list']:
        if x['app_msg_ext_info']:
            imgindex += 1
            comm_msg_info = x["comm_msg_info"]
            app_msg_ext_info = x['app_msg_ext_info']
            xurl = app_msg_ext_info['content_url']
            title = app_msg_ext_info['title']
            title = title.replace('?','').replace('/',',').replace('|', '').replace(' ', '')
            pubstamp =comm_msg_info["datetime"]
            pubdate = Timestamp_now(pubstamp)

            file_name = path+'rawlist/{}'.format(imgindex)+'/'
            # 判断路径目录是否存在
            if not os.path.exists(file_name):
                os.makedirs(file_name)
            savepath = file_name + title
            if not os.path.exists(file_name+'images/'):
                os.makedirs(file_name+'images/')
            imgsavepath = file_name+'images/'

            art = Article(pubdate,savepath,imgsavepath,title)
            ArtList.append(art)
            print(len(ArtList),pubdate,savepath,title)

            response = requests.get(xurl, headers=headers)
            with open(savepath+'.html','wb') as f:
                f.write(response.content)

            print('页面保存成功',title)
    return ArtList

def DownImg(title,savepath,imgsavepath):
        # 读取html文件
        with open(savepath+'.html','r',encoding='utf-8') as f:
            htmltxt = f.read()
        bs = BeautifulSoup(htmltxt, "lxml")  # 由网页源代码生成BeautifulSoup对象，第二个参数固定为lxml
        imgList = bs.findAll("img")
        imgindex = 0
        for img in imgList:
            imgindex+=1
            # 图片真实url
            realUrl = ""
            # 判断 img 标签里有没有data-src属性
            if "data-src" in img.attrs:
                realUrl = img.attrs["data-src"]
            elif "src" in img.attrs:
                realUrl = img.attrs['src']
            else:
                realUrl = ""
            # 如果url以//开头，则需要添加http：
            if realUrl.startswith("//"):
                realUrl = "http:" + realUrl
            # 判断img的格式
            if len(realUrl) > 0:
                # print('插图:',realUrl,imgindex)
                if "data-type" in img.attrs:
                    imgtype = img.attrs["data-type"]
                else:
                    imgtype = "png"
                # 图片名字和格式 title_1.png
                imgname = title + "_" + str(imgindex) + "." + imgtype
                imgpath = os.path.join(imgsavepath,imgname)
                # 下载图片
                r = requests.get(url=realUrl, headers=headers)
                with open(imgpath, 'wb') as f:
                    f.write(r.content)
                # 修改网页中图片的相对路径
                img.attrs["src"] = "./images/" + imgname
                print('插图:',imgname)
            else:
                img.attrs["src"] = ""



def DownHtmlMain(startpath):
    read = ReadFile(startpath)
    for url in read:
        html = jsondata(url)
        ArtList = GetArtic(html)
        ArtList.sort(key=lambda x: x.pubdate, reverse=True)  # 按日期倒序排列
        for art in ArtList:
            try:
                DownImg(art.title, art.savepath,art.imgsavepath)
            except:
                print('出现错误，跳过此项')
                continue
        time.sleep(random.random() * 3)


if __name__ == '__main__':
    startpath = 'G:\Study\Spedir\WeChatArticle/rawlist/url.txt'
    DownHtmlMain(startpath)

