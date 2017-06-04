# coding=utf-8

__author__ = 'yangyz'
##水平有限，多多指教，哈哈

import re
from bs4 import BeautifulSoup
import requests
import time


##获取前30页步行街的发帖主题url
def get_hupuTitle_message():
    titleList = []
    baseUrl = "https://bbs.hupu.com/bxj-postdate-"
    for i in range(30):
        url = baseUrl + str(i + 1)
        respon = requests.get(url)
        respon.encoding = "utf-8"
        json_text = respon.text
        soup = BeautifulSoup(json_text, 'html.parser')
        list = soup.select('tr')
        for j in range(len(list)):
            if (j > 1):  # 从第三条消息开始
                soup1 = BeautifulSoup(str(list[j]), 'html.parser')
                soup_title = soup1.find(attrs={'class': 'p_title'})
                soup_author = soup1.find(attrs={'class': 'p_author'})
                titleUrl = re.search('\/(.*)html', str(soup_title)).group(1)
                title = soup_title.getText().strip().split("\n")[0].strip()
                author = ""
                date = ""
                if '2017' in soup_author.getText():
                    author = soup_author.getText().split("2017-")[0]
                    date = "2017-" + soup_author.getText().split("2017-")[1]
                if (len(titleUrl) > 12):  ##去掉影视区之类的
                    pass
                else:
                    if titleUrl in titleList:
                        pass
                    else:
                        titleList.append(titleUrl)  ##+"@"+title+"@"+author+"@"+date
    return titleList


##找出每个发帖主题里面的回帖用户，返回一个list，list中存一个发帖主题下的所有回帖jr的个人信息链接
def getHupuUsers(pageid):
    urlList = []
    url = "https://bbs.hupu.com/" + pageid + "html"
    resp = requests.get(url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    soup_pageCount = soup.find(attrs={'class': 'page clearfix'})
    pageCount = 1
    try:
        pageCount = re.search('html\"\>(\d*)\<\/a\> \<input', str(soup_pageCount)).group(1)  ##找出一共有多少页回帖
    except Exception as err:
        pass
    for c in range(int(pageCount)):  ##可能有很多页，也可能只有一页
        index = "-" + str(c) + "."
        url = "https://bbs.hupu.com/" + pageid.replace(".", index) + "html"
        resp = requests.get(url)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, 'html.parser')
        soup_user = soup.find_all(attrs={'class': 'j_u'})
        tpName = ""
        for k in range(len(soup_user)):
            if (k == 0):
                soup1 = BeautifulSoup(str(soup_user[k]), 'html.parser')
                tpName = soup1.img['alt']
            else:
                soup1 = BeautifulSoup(str(soup_user[k]), 'html.parser')
                if soup1.a['href'] in urlList:
                    pass
                else:
                    urlList.append(soup1.a['href'])
    return urlList


##根据url获取回帖jr的信息
def getUserDetail(userUrl):
    resp = requests.get(userUrl)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')
    soup_name = soup.find(attrs={'class': 'mpersonal'})
    soup_userInfo = soup.find(attrs={'class': 'personalinfo'})
    userName = ""  # 用户名 ##必须信息
    gender = ""  # 性别  ##选填信息
    address = ""  # 地址 ##选填信息
    NBATeam = ""  # NBA主队 ##选填信息
    CBATeam = ""  # CBA主队 ##选填信息
    ## 下面这些为必须信息  每个用户都有
    BBSRank = ""  # 论坛等级
    calorie = ""  # 卡路里
    onlineTime = ""  # 在线时间
    joinDate = ""  # 加入时间
    lastTimeLogin = ""  # 上次登录时间
    ###################################进入正则表达式匹配阶段##############
    userName = re.search('name\"\>(.*)\<\/div\>', str(soup_name)).group(1)
    ##性别
    try:
        gender = re.search('gender\"\>(.*)\<\/span\>(.*)f666', str(soup_userInfo)).group(1)
    except Exception as err:
        pass
    # 地址
    try:
        address = re.search('address\"\>(.*)\<\/span\>', str(soup_userInfo)).group(1)
    except Exception as err:
        pass
    # NBA主队
    try:
        NBATeam = re.search('NBA主队(.*)_blank\"\>(.*)\<\/a\>(.*)f666', str(soup_userInfo)).group(2)
    except Exception as err:
        pass
    # CBA主队
    try:
        CBATeam = re.search('CBA主队(.*)_blank\"\>(.*)\<\/a\>\<\/span\>', str(soup_userInfo)).group(2)
    except Exception as err:
        pass
    # 论坛等级
    try:
        BBSRank = re.search('论坛等级：\<\/span\>(.*)\<br\/\>', str(soup_userInfo)).group(1)
    except Exception as err:
        pass
    # 卡路里
    try:
        calorie = re.search('里：</span>(.*)\\n', str(soup_userInfo)).group(1)
    except Exception as err:
        pass
    # 在线时间
    try:
        onlineTime = re.search('在线时间：</span>(.*)小时', str(soup_userInfo)).group(1)
    except Exception as err:
        pass
    # 加入时间
    try:
        joinDate = re.search('加入时间：</span>(.*)\\n', str(soup_userInfo)).group(1)
    except Exception as err:
        pass
    # 上次登录时间
    try:
        lastTimeLogin = re.search('上次登录：</span>(.*)\\n', str(soup_userInfo)).group(1)
    except Exception as err:
        pass
    totalStr = userName.strip() + "@" + gender.strip() + "@" + address.strip() + "@" + NBATeam.strip() + "@" + CBATeam.strip() + "@" + BBSRank.strip() + "@" + calorie.strip() + "@" + onlineTime.strip() + "@" + joinDate.strip() + "@" + lastTimeLogin.strip()
    return totalStr


if __name__ == '__main__':
    titleList = get_hupuTitle_message()
    print("获取页面主题链接结束,共" + str(len(titleList)) + "条")
    x = 0
    for i in range(len(titleList)):
        try:
            urlList = getHupuUsers(str(titleList[i]))
            for i in range(len(urlList)):
                try:
                    totalStr = getUserDetail(str(urlList[i]))
                    totalList = totalStr.split("@")
                    ##如果想插入到数据库，这里已经写好sql
                    insertSql = """INSERT INTO hupuUsers(userName,gender,address,nbaTeam,cbaTeam,bbsRank,calorie,onlineTime,joinDate,lastTimeLogin)values(""" + "'" + \
                                totalList[0] + "'," + "'" + totalList[1] + "'," + "'" + totalList[2] + "','" + \
                                totalList[3] + "','" + totalList[4] + "'," + totalList[5] + "," + totalList[6] + "," + \
                                totalList[7] + ",'" + totalList[8] + "','" + totalList[9] + "'" + """)"""
                    print(insertSql)
                except:
                    print("用户信息解析失败")
            time.sleep(1)
        except:
                print("打开" + str(titleList[i]) + "失败")


