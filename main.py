import requests
import time


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
    new_url = "https://bdapi.gameyw.netease.com:443/ky59/v1/g37_charts/oneuid"
    new_params = {
        "server": "all",
        "roleid": url_list[a],
        "_": nowtime,
    }
    new_html = requests.get(url=new_url, params=new_params).json()
    record = new_html["result"]["extra"]["bl"]
    for u in record:
        print("\t对手名称：" + u["d_role_name"])
        print("\t对局时间：" + t(u["battle_time"]))
        if u["total_battle_time"] != 0:
            print("\t上阵阴阳师：" + change(u["battle_list"][0]["shishen_id"]))
            print("\t对手阴阳师：" + change(u["d_battle_list"][0]["shishen_id"]))
        print("\t对局用时：" + consuming(u["total_battle_time"]))
        print("\t对局结果：" + result(u["battle_result"]))
        print("----------------------------------------")
    input("按回车键返回上一页")


def information(a):
    new_url = "https://bdapi.gameyw.netease.com:443/ky59/v1/g37_charts/oneuid"
    new_params = {
        "server": "all",
        "roleid": a,
        "_": nowtime,
    }
    new_html = requests.get(url=new_url, params=new_params).json()["result"]["extra"]
    return str(int(new_html["count_win"] / new_html["count_all"] * 100)) + "%"


url_list = []
top_100 = []

# for y in range(1, 11):
for y in range(1, 2):
    url = "https://bdapi.gameyw.netease.com:443/ky59/v1/g37_charts/topuids"
    params = {
        "server": "all",
        "page": y,
        "_": nowtime,
    }
    html = requests.get(url=url, params=params).json()
    top = html["result"]
    for i in range(len(top)):
        url_list.append(top[i]["role_id"])
        top_100.append("排名第" + str((y - 1) * 10 + i + 1) + " " + top[i]["small_extra"]["role_name"] + " 胜率" + information(top[i]["role_id"]))
while True:
    print("斗技排行top100")
    for i in top_100:
        print(i)
    print("----------------------------------------")
    num = int(input("输入排名查询对局数据,0为退出\n"))
    if num == 0:
        break
    elif 1 <= num <= 100:
        query(num - 1)
