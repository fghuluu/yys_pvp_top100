import requests
import time
import os


def nowtime():
    return int(round(time.time() * 1000))


def change(a):
    if a == 10:
        a = "晴明"
    elif a == 11:
        a = "神乐"
    elif a == 12:
        a = "比丘尼"
    return a


def t(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def result(a):
    if a == "0":
        return "失败"
    else:
        return "胜利"


def consuming(a):
    minute = a // 60
    s = a % 60
    return str(minute) + "分" + str(s) + "秒"


def query(a):
    record = url_list[a]["bl"]
    for u in record:
        print("\t名称：" + u["role_name"])
        print("\t对手名称：" + u["d_role_name"])
        print("\t对局时间：" + t(u["battle_time"]))
        if u["total_battle_time"] != 0:
            print("\t上阵阴阳师：" + change(u["battle_list"][0]["shishen_id"]))
            print("\t对手阴阳师：" + change(u["d_battle_list"][0]["shishen_id"]))
        print("\t对局用时：" + consuming(u["total_battle_time"]))
        print("\t对局结果：" + result(u["battle_result"]))
        print("----------------------------------------")
    input("按回车键返回上一页")


def record_yys(a):
    record = url_list[a]["bl"]
    global qm
    global qm_win
    global sl
    global sl_win
    global bqn
    global bqn_win
    for u in record:
        if u["total_battle_time"] != 0:
            if u["battle_list"][0]["shishen_id"] == 10:
                qm += 1
                if u["battle_result"] == 1:
                    qm_win += 1
            if u["battle_list"][0]["shishen_id"] == 11:
                sl += 1
                if u["battle_result"] == 1:
                    sl_win += 1
            if u["battle_list"][0]["shishen_id"] == 12:
                bqn += 1
                if u["battle_result"] == 1:
                    bqn_win += 1


def information(a):
    new_url = "https://bdapi.gameyw.netease.com:443/ky59/v1/g37_charts/oneuid"
    new_params = {
        "server": "all",
        "roleid": a,
        "_": nowtime,
    }
    new_html = requests.get(url=new_url, params=new_params).json()["result"]["extra"]
    return new_html


def score(a):
    if a < 3000:
        return str(a)
    else:
        return str(int((a - 3000) / 30))+"星"


url_list = []
top_100 = []
game = 0
qm = 0
qm_win = 0
sl = 0
sl_win = 0
bqn = 0
bqn_win = 0
for y in range(1, 11):
    # for y in range(1, 2):
    url = "https://bdapi.gameyw.netease.com:443/ky59/v1/g37_charts/topuids"
    params = {
        "server": "all",
        "page": y,
        "_": nowtime,
    }
    html = requests.get(url=url, params=params).json()
    top = html["result"]
    for i in range(len(top)):
        url_list.append(information(top[i]["role_id"]))
        win = str(int(top[i]['small_extra']["count_win"] / top[i]['small_extra']["count_all"] * 100)) + "%"
        top_100.append("排名第" + str(top[i]["rank"]) + " " + top[i]["small_extra"]["role_name"] + " 当前" + score(top[i]["score"]) + " 胜率" + win + " 数据来源时间：" + top[i]["insert_time"])
        game += top[i]["small_extra"]["count_all"]
        record_yys(i)
        os.system("cls")
        print("正在爬取数据，当前进度" + str((y - 1) * 10 + i + 1) + "%")
os.system("cls")
while True:
    print("斗技排行top100")
    for i in top_100:
        print(i)
    print("----------------------------------------")
    print("总记录对局" + str(game))
    print("晴明上阵局数为" + str(qm) + "胜率为" + str(int(qm_win / qm * 100)) + "% 神乐上阵局数为" + str(sl) + "胜率为" + str(int(sl_win / sl * 100)) + "% 比丘尼上阵局数为" + str(bqn) + "胜率为" + str(int(bqn_win / bqn * 100)) + "%")
    print("上阵局数敌方不做记录")
    num = int(input("输入排名查询对局数据,0为退出\n"))
    if num == 0:
        break
    elif 1 <= num <= 100:
        query(num - 1)
