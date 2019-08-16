from urllib import request
from bs4 import BeautifulSoup
import os,re,requests,time,datetime,json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
}

path = 'G:\Study\html+JavaScript\WeChatCrawl/'
# 读取文件
def ReadFile(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        all_the_text = f.readlines()

        return all_the_text

# 时间戳
def Timestamp():
    newtime = time.strftime('%Y%m%d%H', time.localtime(int(time.time())))
    return newtime

# 构建请求头
def DownLoadHtml(url):
    # 构建请求头
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text
        htmltxt = json.loads(html)
        return htmltxt
    else:
        return None

# 下载文章页
def GetArtic(html):

    dict = html["general_msg_list"]
    dict = json.loads(dict)
    imgindex = 0
    for x in dict['list']:
        if x['app_msg_ext_info']:
            imgindex += 1
            # print(x['app_msg_ext_info'])
            xurl = x['app_msg_ext_info']['content_url']
            title = x['app_msg_ext_info']['title']
            title = title.replace('?','').replace('/',',').replace('|', '').replace(' ', '')
            response = requests.get(xurl,headers=headers)
            file_name = path+'rawlist/{}'.format(imgindex)+'/'
            # 判断路径目录是否存在
            if not os.path.exists(file_name):
                os.makedirs(file_name)
            savepath = file_name + title
            if not os.path.exists(file_name+'/images/'):
                os.makedirs(file_name+'/images/')
            imgsavepath = file_name+'/images/'

            with open(savepath+'.html','wb') as f:
                f.write(response.content)
            print(xurl)
            print('页面保存成功',title)
            DownImg(xurl,title,imgsavepath)

def DownImg(url,title,savepath):
    response = requests.get(url, headers=headers)
    htmltxt = response.text
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
            imgsavepath = os.path.join(savepath,imgname)
            # 下载图片
            r = requests.get(url=realUrl, headers=headers)
            with open(imgsavepath, 'wb') as f:
                f.write(r.content)
            # 修改网页中图片的相对路径
            img.attrs["src"] = "./images/" + imgname
            print(img.attrs["src"])
            print('保存成功！',imgname)
        else:
            img.attrs["src"] = ""

if __name__ == '__main__':
    read = ReadFile('G:\Study\html+JavaScript\WeChatCrawl/rawlist/url.txt')
    for url in read:
        html = DownLoadHtml(url)
        GetArtic(html)
    # url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzU4ODQzODE3Nw==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=MjU0MDI3NTU4NA%3D%3D&key=386bceb81f3ee3d0ed8ac15b0252b771d356fca96282f22852084ec827c9b90e8f7baded641d08593118994a2d864dbcb64ad2873c14d58ad74aa63c275c8dc6293016260f0d9da61e7c2e867d2ece55&pass_ticket=GnhPSGnyWOTzUS5xpkDeLe3x0FlQuUNKAAJbnL2WkVlxGPm5oDLa4gzk1pgOVOBP&wxtoken=&appmsg_token=1022_6GZa7sEvTTImDFjU9OxU7ik_Ia1HnKFhTWHJuw~~&x5=0&f=json'
    # url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzU4ODQzODE3Nw==&f=json&offset=21&count=10&is_ok=1&scene=124&uin=MjU0MDI3NTU4NA%3D%3D&key=ca93523d7743ba820dc47f0d903c87424088309be3e5283476a7eca440890296f3134f1369978cf89325ff4d0801730e88e56078beace57194941b91cb830f24f367c8e9b336748af90901a5cc24befe&pass_ticket=GnhPSGnyWOTzUS5xpkDeLe3x0FlQuUNKAAJbnL2WkVlxGPm5oDLa4gzk1pgOVOBP&wxtoken=&appmsg_token=1022_tgxTxK2dg6jBfVc9nEH2T6gHDsICE8kItLw--Q~~&x5=0&f=json'
    # html = DownLoadHtml(url)
    # GetArtic(html)

