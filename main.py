import requests
from urllib import parse
from urllib import request
import os
import re
from bs4 import BeautifulSoup

# 解析入口页面
startPath = "http://www.cbpm.cn/cn/rmbpic/rmbpic1/"

resp = requests.get(startPath)
soup = BeautifulSoup(resp.content, "html.parser")
#  取出相应栏目的连接地址数据
channel_list = soup.find_all("a", style="color:#333")
# 遍历栏目
for channel in channel_list:
    href = channel.get("href")
    # 获取栏目标题
    dirName = channel.contents[0].replace("\n", "")
    # if(dirName != '普通纪念币'):
    #     continue
    # 获取保存路径
    savePath = os.path.dirname(__file__)+"/data/"
    path = savePath+dirName.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isInExists = os.path.exists(path)
    # 判断结果
    if not isInExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path+' 创建成功')

    href = parse.urljoin(startPath, href)
    # print("请求路径：" + href)
    respIn = requests.get(href)
    soupIn = BeautifulSoup(respIn.content, "html.parser")
    scriptIn = soupIn.find_all("script", language='javascript')
    if len(scriptIn) > 0:
        scriptStr = scriptIn[0].text
        # 找到包含总页数的脚本
        p = re.findall('countPage = (\d+)', scriptStr)
        if len(p) == 1:
            countPage = int(p[0])
            for i in range(0, countPage):
                pageHref = ''
                if i == 0:
                    pageHref = parse.urljoin(href, "index.html")
                else:
                    pageHref = parse.urljoin(href, "index_"+str(i)+".html")

                print("爬取页面：" + pageHref)
                # 分页数据
                respPage = requests.get(pageHref)
                soupPage = BeautifulSoup(respPage.content, "html.parser")
                imageDivs = soupPage.find_all("div",class_='imgTxt')
                imagesAs = soupPage.find_all("a",class_='sampleMoney')
                if len(imageDivs) == len(imagesAs):
                    for j in range(0, len(imagesAs)):
                        # 创建文件夹
                        imgDirName = imageDivs[j].text.replace("\n", "").replace(" ","")
                        imgPath = path+"/"+imgDirName.strip()
                        imgPath = imgPath.rstrip("\\")
                        # 判断路径是否存在
                        isExists = os.path.exists(imgPath)
                        # 判断结果
                        if not isExists:
                            # 如果不存在则创建目录
                            # 创建目录操作函数
                            os.makedirs(imgPath)
                            print(imgPath+' 创建成功')
                        imagesAHref = imagesAs[j].get("href")
                        imagesAHref = parse.urljoin(href, imagesAHref)
                        respImg = requests.get(imagesAHref)
                        soupImg = BeautifulSoup(respImg.content, "html.parser")
                        imagesDivImgs = soupImg.find_all("div", class_="col-xs-12 currencyInfo")
                        for imageI in range(0,len(imagesDivImgs)):
                            if dirName != '普通纪念币':
                                imagesDivImg = imagesDivImgs[imageI]
                                imageImg = imagesDivImg.find("img")
                                imageImgHref = imageImg.get("src")
                                endIndex = imagesAHref.rindex("/")
                                parPath = imagesAHref[0:endIndex+1]
                                imageImgHref = parse.urljoin(parPath, imageImgHref)
                                startIndex = imagesAHref.rindex("/")
                                name = imageImgHref[endIndex+1:]
                                isImgExists = os.path.exists(imgPath+"/"+name)
                                if not isImgExists:
                                    request.urlretrieve(imageImgHref, imgPath+"/"+name)
                                    print(imgPath+"/"+name)
                            else:
                                imagesDivImg = imagesDivImgs[imageI]
                                imageImgs = imagesDivImg.find_all("img")
                                for imageImg in imageImgs:
                                    imageImgHref = imageImg.get("src")
                                    endIndex = imagesAHref.rindex("/")
                                    parPath = imagesAHref[0:endIndex+1]
                                    imageImgHref = parse.urljoin(parPath, imageImgHref)
                                    startIndex = imagesAHref.rindex("/")
                                    name = imageImgHref[endIndex+1:]
                                    isImgExists = os.path.exists(imgPath+"/"+name)
                                    if not isImgExists:
                                        request.urlretrieve(imageImgHref, imgPath+"/"+name)
                                        print(imgPath+"/"+name)
    else:
        meta_list = soupIn.find_all("meta")
        fifthPath = parse.urljoin(startPath,href)
        for meta in meta_list:
            meta_centent = str(meta.get("content"))
            meta_url = re.findall('url=(.*)', meta_centent)
            if len(meta_url) > 0:
                fifthPath = parse.urljoin(fifthPath, meta_url[0])
                respFifth = requests.get(fifthPath)
                soupFifth = BeautifulSoup(respFifth.content, "html.parser")
                meta_list_fifth = soupFifth.find_all("meta")
                for meta_fifth in meta_list_fifth:
                    meta_centent_fifth = str(meta_fifth.get("content"))
                    meta_url_fifth = re.findall('url=(.*)', meta_centent_fifth)
                    if len(meta_url_fifth) > 0:
                        fifthNfPath = parse.urljoin(fifthPath, meta_url_fifth[0])
                        respFifthNf = requests.get(fifthNfPath)
                        soupFifthNf = BeautifulSoup(respFifthNf.content, "html.parser")
                        scriptFifthNf = soupFifthNf.find_all("script", language='javascript')
                        if len(scriptFifthNf) > 0:
                            scriptStr = scriptFifthNf[0].text
                            # 找到包含总页数的脚本
                            p = re.findall('countPage = (\d+)', scriptStr)
                            if len(p) == 1:
                                countPage = int(p[0])
                                for i in range(0, countPage):
                                    pageHref = ''
                                    if i == 0:
                                        pageHref = parse.urljoin(fifthNfPath, "index.html")
                                    else:
                                        pageHref = parse.urljoin(fifthNfPath, "index_"+str(i)+".html")

                                    print(pageHref)
                                    # 分页数据
                                    respPage = requests.get(pageHref)
                                    soupPage = BeautifulSoup(respPage.content, "html.parser")
                                    imageDivs = soupPage.find_all("div",class_='imgTxt')
                                    imagesAs = soupPage.find_all("a",class_='sampleMoney')
                                    if len(imageDivs) == len(imagesAs):
                                        for j in range(0, len(imagesAs)):
                                            # 创建文件夹
                                            imgDirName = imageDivs[j].text.replace("\n", "").replace(" ","")
                                            imgPath = path+"/"+imgDirName.strip()
                                            imgPath = imgPath.rstrip("\\")
                                            # 判断路径是否存在
                                            isExists = os.path.exists(imgPath)
                                            # 判断结果
                                            if not isExists:
                                                # 如果不存在则创建目录
                                                # 创建目录操作函数
                                                os.makedirs(imgPath)
                                                print(imgPath+' 创建成功')
                                            imagesAHref = imagesAs[j].get("href")
                                            imagesAHref = parse.urljoin(fifthNfPath, imagesAHref)
                                            respImg = requests.get(imagesAHref)
                                            soupImg = BeautifulSoup(respImg.content, "html.parser")
                                            imagesDivImgs = soupImg.find_all("div", class_="col-xs-12 currencyInfo")
                                            for imageI in range(0,len(imagesDivImgs)):
                                                imagesDivImg = imagesDivImgs[imageI]
                                                imageImg = imagesDivImg.find("img")
                                                imageImgHref = imageImg.get("src")
                                                endIndex = imagesAHref.rindex("/")
                                                parPath = imagesAHref[0:endIndex+1]
                                                imageImgHref = parse.urljoin(parPath, imageImgHref)
                                                startIndex = imagesAHref.rindex("/")
                                                name = imageImgHref[endIndex+1:]
                                                isImgExists = os.path.exists(imgPath+"/"+name)
                                                if not isImgExists:
                                                    request.urlretrieve(imageImgHref, imgPath+"/"+name)
                                                    print(imgPath+"/"+name)




