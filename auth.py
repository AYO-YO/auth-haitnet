"""
@author: 赵春旭
@name: 一键认证
@version: v1.3
"""

import os
import socket
import time

import requests


def get_ip():
    """
    获取本机ip地址
    :return: 若成功获取河南工学院局域网ip则返回，否则则返回默认ip
    """
    s = socket.socket()
    try:
        s.connect(('211.69.15.33', 9999))  # 建立链接，捕捉活动ip
        ip = s.getsockname()[0]
        if ip:
            print(f'ip确认成功，ip为...{ip}')
            return ip
        else:
            print('ip确认失败，返回默认ip 8.8.8.8')
            return '8.8.8.8'
    except Exception as e:
        print('请求ip失败，请检查wifi连接后重试')
        exit(0)


path = './haitNet_user.txt'
is_new = False
try:
    with open(path) as f:
        s = f.read().strip().split()
    userId = s[0]
    userPwd = s[1]
    swfs = s[2]
    print(f'{userId}  {userPwd}  {swfs}')
except FileNotFoundError:
    is_new = True
    print('欢迎您使用本认证系统，请完成初始化操作...')
    print(f'完成本次初始化操作之后，您的认证信息将被写入{path}，若您修改了密码，请删除本文件，再次运行程序，程序将再次进行初始化...')
    userId = input('请输入您的学号：')
    userPwd = input('请输入您的密码：')
    swfs = '@local'
    while True:
        fs = input('请选择您的上网方式(输入数字)：\n'
                   '1.中国移动\n'
                   '2.中国联通\n'
                   '3.中国电信\n')
        match fs:
            case '1':
                swfs = '@gxyyd'
                break
            case '2':
                swfs = '@gxylt'
                break
            case '3':
                swfs = '@gyxdx'
                break
            case _:
                print('输入值有误，请重新输入：')
    with open(path, 'wt') as w:
        w.write(f'{userId}\n{userPwd}\n{swfs}')
        w.flush()
        print('初始化完成！')
userIp = get_ip()  # 本机的ip地址
isReOpenExp = False  # 是否重启任务管理器，是：True; 否：False

userName = userId + swfs
url = 'http://211.69.15.33:9999/portalAuthAction.do'
header = {
    'Host': '211.69.15.33:9999',
    'Connection': 'keep-alive',
    'Content-Length': '638',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://211.69.15.33:9999',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': f'http://211.69.15.33:9999/portalReceiveAction.do?wlanuserip={userIp}&wlanacname=HAIT-SR8808',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': 'JSESSIONID=23287C3422D0571138FCD1E6891C97F1.worker3'
}

data = {'wlanuserip': userIp,
        'wlanacname': 'HAIT-SR8808',
        'chal_id': '',
        'chal_vector': '',
        'auth_type': 'PAP',
        'seq_id': '',
        'req_id': '',
        'wlanacIp': '172.21.8.73',
        'ssid': '',
        'vlan': '',
        'mac': '',
        'message': '',
        'bank_acct': '',
        'isCookies': '',
        'version': '0',
        'authkey': '88----89',
        'url': '',
        'usertime': '0',
        'listpasscode': '0',
        'listgetpass': '0',
        'getpasstype': '0',
        'randstr': '5099',
        'domain': '',
        'isRadiusProxy': 'true',
        'usertype': '0',
        'isHaveNotice': '0',
        'times': '12',
        'weizhi': '0',
        'smsid': '',
        'freeuser': '',
        'freepasswd': '',
        'listwxauth': '0',
        'templatetype': '1',
        'tname': 'gxy_pc_portal',
        'logintype': '0',
        'act': '',
        'is189': 'false',
        'terminalType': '',
        'checkterminal': 'true',
        'portalpageid': '23',
        'listfreeauth': '0',
        'viewlogin': '1',
        'userid': userName,
        'authGroupId': '',
        'smsoperatorsflat': '',
        'useridtemp': userName,
        'passwd': userPwd,
        'operator': swfs,
        }

# wifi的操作
wifi = pywifi.PyWiFi()
i_face = wifi.interfaces()[0]


def wifi_info() -> bool:
    """
    判断wifi是否链接
    :return: True or False
    """
    if i_face.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
        return True
    return False


def contest():
    """进行认证\n
    认证成功->True\n
    其他设备在线->2秒后重新执行验证程序\n
    认证失败->False 并打印 网站源码"""
    req = requests.post(url, headers=header, data=data)
    if '<title>离线页面</title>' in req.text:
        return True
    elif url in req.url:
        print('已强制其他设备下线，2s后重新连接')
        time.sleep(2)
        contest()
    else:
        print(req.text)
        return False


def reDns():
    """
    刷新DNS
    :return: void
    """
    flush_dns = 'ipconfig /flushdns'
    os.system(flush_dns)
    return 'DNS已刷新'


def pingTest(url='www.baidu.com', n=1):
    """
    连通性测试
    :param url: ping target ip or url
    :param n: Test times
    """
    ping_cmd = 'ping -n %d %s' % (n, url)
    os.system(ping_cmd)


i = 1
while i <= 5:
    if wifi_info():  # wifi为连接状态，开始认证
        print('Wifi已连接，正在尝试认证...')
        print('正在进行第%d次连接...' % i)
        if contest():  # 进行认证
            print('认证成功...')
            print(reDns())  # 刷新dns
            time.sleep(1)
            pingTest()  # 测试外网连通性
            time.sleep(1)
            print('认证完成，程序将在3秒后退出')
            if is_new:
                SQLTest.insertSQL(userId, userPwd, swfs, userIp)
            time.sleep(3)
            break
        else:
            print('认证失败，请查看返回信息：')
    else:
        print('WiFi未连接，请手动连接WiFi后，按回车键重新尝试连接')
        temp = input()
    i += 1
if i == 6:
    print('失败次数过多，请重新运行程序')
