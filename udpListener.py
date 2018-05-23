import socket
import json
import pymysql
import re
import time
import traceback

udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP
bindAdress =('192.168.0.133',12345)
udpSocket.bind(bindAdress)
db = pymysql.connect("localhost", "ur_admin", "ur_pwd", "field_1")
cursor = db.cursor()
print('正在監聽位址:',bindAdress)
print('-------------------------------------------------------------')
while True:
    try:
        recvDate,recvAddr = udpSocket.recvfrom(1024)
        msg = recvDate.decode('gbk')
        msg = msg.replace(" ", "")
        msg = msg.replace("\x00", "")
        msgToJson = json.loads(msg)
        # ----------------------------------------------------#
        # chOn 這個 list 物件儲存目前所有開啟的 Channel
        # 接著從chOn判斷哪幾個有開, 去寫入對應的SQL
        # ----------------------------------------------------#
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
            sql = 'INSERT INTO data (Time, serial, xhot_id, high_temp, lower_temp, pres_id, conn_status, temp_status) VALUES ("%s","%s","%d","%d","%d","%d","%d","%d")' % (nowTime, serial, idToInt, data_int[0], data_int[1], data_int[2], data_int[3], data_int[4])
            # cursor.execute(sql)
            # db.commit()
            idIndex += 1
            # print(chOn)
            # print(data_int)
        print("目前開啟的 Channel :",chOn)
        print("資料 :",data_int)
        # print('已寫入', cursor.rowcount, '筆資料')
    except Exception as e:
        #print("錯誤資訊 :" + str(e))
        print(traceback.format_exc())
