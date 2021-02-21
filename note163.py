import requests
import sys
import json
import time
import urllib3
import os

urllib3.disable_warnings()

# note.youdao.com 有道云笔记签到

user=""
passwd=""

if(user=="",passwd==""):
    user = input("账号:")
    passwd = input("密码:")

    
def noteyoudao(YNOTE_SESS: str, user: str, passwd: str):
    s = requests.Session()
    checkin_url = 'http://note.youdao.com/yws/mapi/user?method=checkin'
    cookies = {
        'YNOTE_LOGIN': 'true',
        'YNOTE_SESS': YNOTE_SESS
    }
    r = s.post(url=checkin_url, cookies=cookies, )
    if r.status_code == 200:
        # print(r.text)
        info = json.loads(r.text)
        total = info['total'] / 1048576
        space = info['space'] / 1048576
        t = time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime(info['time'] / 1000))
        print(f'{user}签到成功，本次获取{space}M, 总共获取{total}M, 签到时间{t}')
        pushplus('有道云笔记签到成功',f'本次获取{space}M, 总共获取{total}M, 签到时间{t}')
    # cookie 登录失效，改用用户名密码登录
    else:
        login_url = 'https://note.youdao.com/login/acc/urs/verify/check?app=web&product=YNOTE&tp=ursto' \
                    'ken&cf=6&fr=1&systemName=&deviceType=&ru=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2Flo' \
                    'ginCallback.html&er=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&vc' \
                    'ode=&systemName=Windows&deviceType=WindowsPC&timestamp=1517235699501'
        parame = {
            'username': user,
            'password': passwd
        }

        r = s.post(url=login_url, data=parame, verify=False)
        x = [i.value for i in s.cookies if i.name == 'YNOTE_SESS']
        if x.__len__() == 0:
            YNOTE_SESS = "-1"
            print(user+"登录失败")
            print(r.history)
            print(s.cookies)
            return
        else:
            print(user+'登录成功，更新YNOTE_SESS,重新签到')
            YNOTE_SESS = x[0]
            noteyoudao(YNOTE_SESS, user, passwd)
            return YNOTE_SESS

def pushplus(title,content,template='html'):#改成你要的正文内容
    PUSHPLUS_TOKEN = os.environ["PUSHPLUS_TOKEN"] #在pushpush网站中可以找到
    if isinstance(PUSHPLUS_TOKEN,str) and len(PUSHPLUS_TOKEN)>0:
        print('检测到PUSHPLUS_TOKEN，准备推送',title,content)        
        url = 'http://pushplus.hxtrip.com/send'
        data = {
            "token":PUSHPLUS_TOKEN,
            "title":title,
            "content":content,
            "template":template
        }
        body=json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type':'application/json'}
        requests.post(url,data=body,headers=headers)
if __name__ == "__main__":
    noteyoudao("",user,passwd)

