import requests
from bs4 import BeautifulSoup
import os
from urllib import parse
import re

startPath = "http://www.cbpm.cn/cn/rmbpic/rmbpic1/"

class ImgParse:
    # 获取栏目
    def getChannel(self):
        channelResp = requests.get(startPath)
        channelSoup = BeautifulSoup(channelResp.content, "html.parser")
        #  取出相应栏目的连接地址数据
        channelList = channelSoup.find_all("a", style="color:#333")
        return channelList

    # 获取下一页
    def getNextPage(self,soup,channelHref):
        meta_list = soup.find_all("meta")
        for meta in meta_list:
            meta_centent = str(meta.get("content"))
            meta_url = re.findall('url=(.*)', meta_centent)
            if len(meta_url) > 0:
                channelHref = parse.urljoin(channelHref,meta_url[0])
                channelPageResp  = requests.get(channelHref)
                channelPageSoup = BeautifulSoup(channelPageResp.content, "html.parser")
                return self.getNextPage(channelPageSoup,channelHref)
            else:
                return soup.find_all("script", language='javascript')

    # 获取栏目对应的页面
    def getChannelPages(self, channel):
        channelRelativeHref = channel.get("href")
        channelHref = parse.urljoin(startPath, channelRelativeHref)
        channelPageResp  = requests.get(channelHref)
        channelPageSoup = BeautifulSoup(channelPageResp.content, "html.parser")
        channelPageScript = channelPageSoup.find_all("script", language='javascript')
        if(len(channelPageScript) == 0):
            channelPageScript = self.getNextPage(channelPageSoup,channelHref)

        print(channelPageScript)


    # 按照栏目件目录
    def createChannelDir(self, channel):
        dirName = channel.contents[0].replace("\n", "")
        savePath = os.path.dirname(__file__)+"/data1/"
        savePath = savePath+dirName.strip()
        # 去除尾部 \ 符号
        savePath = savePath.rstrip("\\")
        # 判断路径是否存在
        isInExists = os.path.exists(savePath)
        # 判断结果
        if not isInExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(savePath)
            print(savePath+' 创建成功')







def main():
    imgParse = ImgParse()
    channelList = imgParse.getChannel()
    # 按照栏目解析
    for channel in channelList:
        # 建存放目录
        imgParse.createChannelDir(channel)
        # 解析栏目页面
        imgParse.getChannelPages(channel)


if __name__ == '__main__':
    main()
