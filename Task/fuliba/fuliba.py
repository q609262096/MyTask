# -*- coding: utf8 -*-

import requests
import re
import time
import os


fuliba_cookie = ''
# 通知服务
BARK_PUSH = ''                   # bark服务,自行搜索; secrets可填;形如jfjqxDx3xxxxxxxxSaK的字符串
SCKEY = ''                  # Server酱的SCKEY; secrets可填

if "FULIBA_COOKIE" in os.environ:
    """
    判断是否运行自GitHub action,"welfareBA_COOKIE" 该参数与 repo里的Secrets的名称保持一致
    """
    print("执行自GitHub action")
    fuliba_cookie = os.environ["FULIBA_COOKIE"]
    if "BARK_PUSH" in os.environ and os.environ["BARK_PUSH"]:
        BARK_PUSH = os.environ["BARK_PUSH"]
        print("BARK 推送打开")
    if "SCKEY" in os.environ and os.environ["SCKEY"]:
        SCKEY = os.environ["SCKEY"]
        print("serverJ 推送打开")

def serverJ(title, content):
    print("\n")
    sckey = SCKEY
    if "SCKEY" in os.environ:
        """
        判断是否运行自GitHub action,"SCKEY" 该参数与 repo里的Secrets的名称保持一致
        """
        sckey = os.environ["SCKEY"]

    if not sckey:
        print("server酱服务的SCKEY未设置!!\n取消推送")
        return
    print("serverJ服务启动")
    data = {
        "text": title,
        "desp": content.replace("\n", "\n\n")+"\n\n"
    }
    response = requests.post(f"https://sc.ftqq.com/{sckey}.send", data=data)
    print(response.text)


def bark(title, content):
    print("\n")
    bark_token = BARK_PUSH
    if "BARK_PUSH" in os.environ:
        bark_token = os.environ["BARK_PUSH"]
    if not bark_token:
        print("bark服务的bark_token未设置!!\n取消推送")
        return
    print("bark服务启动")
    response = requests.get(
        f"""https://api.day.app/{bark_token}/{title}/{content}""")
    print(response.text)

def start():
    try:
        s = requests.session()
        message = time.strftime('%Y.%m.%d', time.localtime(time.time()))+'\n'
        # 福利吧地址
        flb_url = 'www.wnflb2020.com'

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept - Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'cache-control': 'max-age=0',
                   'Host': flb_url,
                   'Upgrade-Insecure-Requests': '1',
                   'Cookie': fuliba_cookie,
                   'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Mobile Safari/537.36'}

        # 访问PC主页
        Integration_response = s.get('https://' + flb_url + '/forum.php?mobile=no', headers=headers).text

        # 获取积分
        #Integration_response = s.get('https://' + flb_url + '/forum.php?mobile=no', headers=headers).text
        integral = re.search(r'<a.*? id="extcreditmenu".*?>(.*?)</a>', Integration_response).group(1)
        UserName = re.search(r'title="访问我的空间">(.*?)</a>',Integration_response).group(1)


        # 获取签到链接
        Checkin_url = re.search(r'}function fx_checkin(.*?);', Integration_response).group(1)
        Checkin_url = Checkin_url[47:-2] + '&infloat=yes&handlekey=fx_checkin&inajax=1&ajaxtarget=fwin_content_fx_checkin'

        # 签到
        Checkin_response = s.get('https://' + flb_url + '/' + Checkin_url, headers=headers).text
        Checkin_result = re.search(r"showDialog\(\'(.*?)\'",Checkin_response).group(1)
        if '签名出错-2,请重新登陆后签到1!' == Checkin_result:
            message += "今日已签到，重复签到！\n"
        else:
            message += Checkin_result+'\n'
        print(Checkin_result)

        # 获取个人信息 福利、分享、金币、精华、爱心
        Info_url = 'https://www.wnflb2020.com/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu'
        Info_response = s.get(Info_url,headers=headers).text
        welfare = re.search(r'<span id="hcredit_1">(.*?)</span>', Info_response).group(1)
        share = re.search(r'<span id="hcredit_2">(.*?)</span>', Info_response).group(1)
        gold = re.search(r'<span id="hcredit_3">(.*?)</span>', Info_response).group(1)
        essence = re.search(r'<span id="hcredit_4">(.*?)</span>', Info_response).group(1)
        love = re.search(r'<span id="hcredit_5">(.*?)</span>', Info_response).group(1)
        result = "用户名:"+UserName+"\n"+integral+"\n福利:" + welfare + "\n分享:" + share + "\n金币:" + gold + "\n精华:" + essence + "\n爱心:" + love
        print(result)
        message += result

    except Exception as e:
        print("签到失败，请检查Cookie或者签到链接是否失效！" + str(e))
        message = "签到失败，请检查Cookie或者签到链接是否失效！" + str(e)
    bark("⏰ 福利吧签到", message)
    serverJ("⏰ 福利吧签到", message)


if __name__ == '__main__':
    start()
