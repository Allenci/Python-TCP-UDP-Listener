import socket
import json
import pymysql
import re
import time
import traceback
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_hostname = socket.gethostname()
local_fqdn = socket.getfqdn()
ip_address = socket.gethostbyname(local_hostname)
# print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
server_address = (ip_address, 12345)
db = pymysql.connect("localhost", "ur_admin", "ur_pwd", "field_1")
# print ('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)
print ('等待連線中...')
connection, client_address = sock.accept()
print ('已連線 IP :', client_address)
cursor = db.cursor()
while True:
    try:
        data = connection.recv(1024)
        # dataTo = str(data, encoding="utf-8")
        msg = data.decode('gbk')
        msg = msg.replace(" ", "")
        msg = msg.replace("\x00", "")

        if msg != '':
            msgToJson = json.loads(msg)
        else:
            print("已斷開連線...")
            break

        # print ("收到資料 :",dataTo, "|| 資料型別 :", type(dataTo))

        chOn = []
        data_int = []
        idIndex = 0
        serial = msgToJson["Serial"]
        for id in msgToJson["Data"]:
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            idToInt = int(msgToJson["Data"][idIndex]['ID'])
            idToStr = str(idToInt)
            data_str = msgToJson["Data"][idIndex]["value"]
            data_int = [int(i) for i in data_str]
            chOn.append(idToInt)
            sql = 'INSERT INTO data (Time, serial, xhot_id, high_temp, lower_temp, pres_id, conn_status, temp_status) VALUES ("%s","%s","%d","%d","%d","%d","%d","%d")' % (
            nowTime, serial, idToInt, data_int[0], data_int[1], data_int[2], data_int[3], data_int[4])
            cursor.execute(sql)
            db.commit()
            idIndex += 1
            # print(chOn)
            # print(data_int)
            print("目前開啟的 Channel :", chOn)
            print("資料 :", data_int)
            # print('已寫入', cursor.rowcount, '筆資料')
    except Exception as e:
        # print("錯誤資訊 :" + str(e))
        print(traceback.format_exc())

#再次重新啟動自己, 因為TCP重新連線造成msg的接收錯誤 而迴圈 break 之後, 再把自己重新啟動, 等待重新連線
os.startfile('pyTCP.py')
