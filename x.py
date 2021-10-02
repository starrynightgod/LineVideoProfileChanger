# -*- coding: utf-8 -*-
# Line頭貼影片更換 作者:蒼 
# 請勿拿去做任何營利用途


from Cang.linepy import *
from Cang.akad.ttypes import Message
from Cang.akad.ttypes import ContentType as Type
from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
from youtube_dl import YoutubeDL
import subprocess, youtube_dl, humanize, traceback
import subprocess as cmd
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit

client = LINE("YOUR_AUTJ_TOKEN")
#client = LINE("")
clientMid = client.profile.mid
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)
botStart = time.time()

msg_dict = {}


try:
    with open("Log_data.json","r",encoding="utf_8_sig") as f:
        msg_dict = json.loads(f.read())
except:
    print("Thanks to Cang")
    
def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def logout():
    client.auth.logoutZ()

def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))

def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                client.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]
            

def command(text):
    pesan = text.lower()
    cmd = text.lower()
    return cmd
	
def changeVideoAndPictureProfile(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = client.genOBSParams({'oid': clientMid, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4', 'name': 'Hello_World.mp4'})
        data = {'params': obs_params}
        r_vp = client.server.postContent('{}/talk/vp/upload.nhn'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return "Failed update profile"
        client.updateProfilePicture(pict, 'vp')
        return "Success update profile"
    except Exception as e:
        raise Exception("Error change video and picture profile %s"%str(e))

def clientBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return

        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")

        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE INTO GROUP")

        if op.type in [22, 24]:
            print ("[ 22 And 24 ] NOTIFIED INVITE INTO ROOM & NOTIFIED LEAVE ROOM")

        if op.type == 25:
            try:
                print ("[ 25 ] SEND MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
                        else:
                            cmd = command(text)
                            if cmd == "help":
                                helpmsg = "╔══[ LineVideoProfileChanger V3.1]\n"
                                helpmsg += "╠可用命令:\n"
                                helpmsg += "╠cvp 「影片連結」\n"
                                helpmsg += "╠cp (更換現有的影片)\n"
                                helpmsg += "╠══[ 使用方法 ]\n"
                                helpmsg += "╠cp：將影片放置在跟x.py同一目錄下(檔名為Video.mp4)\n"
                                helpmsg += "╠══[ 關於本bot ]\n"
                                helpmsg += "╠開源:꧁༺檸檬𓂀紅茶༻᭄ꦿ࿐\n"
                                helpmsg += "╠原作者:https://home.gamer.com.tw/homeindex.php?owner=vincent9579\n"
                                helpmsg += "╠開源作者:https://line.me/ti/p/HtfIAa_tsU\n"
                                helpmsg += "╚══[ 感謝使用 ]"
                                client.sendMessage(to,str(helpmsg))
                            elif msg.text.lower().startswith("cvp"):
                                sep = text.split(" ")
                                link = text.replace(sep[0] + " ","")
                                contact = client.getContact(sender)
                                client.sendMessage(to, "狀態: 下載中...")
                                print("正在下載中...需耗時數分鐘")
                                pic = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
                                os.system('youtube-dl --format mp4 --output BotVideo.mp4 {}'.format(link))
                                pict = client.downloadFileURL(pic)
                                vids = "BotVideo.mp4"
                                changeVideoAndPictureProfile(pict, vids)
                                client.sendMessage(to, "成功替換頭像影片")
                                print("成功替換頭像影片 刪除影片完畢")
                                os.remove("BotVideo.mp4")         
                            elif msg.text.lower().startswith("cp"):
                                contact = client.getContact(sender)
                                client.sendMessage(to, "狀態: 更換中...")
                                print("需耗時數分鐘")
                                pic = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
                                pict = client.downloadFileURL(pic)
                                vids = "Video.mp4"
                                changeVideoAndPictureProfile(pict, vids)
                                client.sendMessage(to, "成功替換頭像影片")
                                print("成功替換頭像影片 刪除影片完畢")
                                os.remove("Video.mp4")         
                            elif msg.text.lower().startswith("logout"):
                                print("正在登出")
                                client.sendMessage(to, "登出中....")
                                logout()
                                print("登出完畢")
                                sys.exit(0)
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
                
        if op.type == 26:
            try:
                print ("[ 26 ] RECIEVE MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)

while True:
    try:
        delete_log()
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clientBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as error:
        logError(error)
        
def atend():
    print("Saving")
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
    print("BYE")
atexit.register(atend)
