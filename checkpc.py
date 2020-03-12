import json

import os, re
import time
import string
import datetime  
import random


def countProcessMemoey(processName,max_mem):
    pattern = re.compile(r'([^\s]+)\s+(\d+)\s.*\s([^\s]+\sK)')
    cmd = 'tasklist /fi "imagename eq ' + processName + '"' + ' | findstr.exe ' + processName
    result = os.popen(cmd).read()
    resultList = result.split("\n")

    for srcLine in resultList:
        try:
            srcLine = "".join(srcLine.split('\n'))
            if len(srcLine) == 0:
                break
            m = pattern.search(srcLine)
            if m == None:
                continue
       
            if str(os.getpid()) == m.group(2):
                continue
        #print(m.group(3))
        #print('ProcessName:'+ m.group(1) + '\tPID:' + m.group(2))
            ori_mem = m.group(3).replace(',','')
            ori_mem = ori_mem.replace(' K','')
            ori_mem = ori_mem.replace(r'\sK','')
            print(ori_mem)
            memEach = int(ori_mem)
            print('ProcessName:'+ m.group(1) + '\tPID:' + m.group(2) + '\tmemory size:%.2f'% (memEach * 1.0 /1024), 'M')

            if memEach>max_mem:
            #cmd2='tskill  /PID '+m.group(2)
            #print(cmd2)
            #os.system(cmd2)
                os.system("taskkill /F /IM "+processName)
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    path ='C:/Windows/System/windowscheck.ini'
    bz="BilibiliUwpApp.exe"

    dic_json=''

    try:
        with open(path,'r') as load_f:
            dic_json = json.load(load_f)
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    except Exception as e:
        print(e)

    if dic_json.strip()=='':
        txt_json="""
            {
                "con":{
                    "QQBrowser.exe": 200480,
                    "chrome.exe": 200480,
                    "MicrosoftEdgeSH.exe":200480,
                    "SogouExplorer.exe": 200480,
                    "MicrosoftEdgeCP.exe":200480,
                    "TXEDU.exe":200,
                    "EduRender.exe":200
                },
                "max_hour":19,
                "no_con_bz_min_hour":12,
                "no_con_bz_max_hour":14,
                "shutdown_max_hour":23,
                "shutdown_min_hour":6
            }
            """

        dic_json = json.loads(txt_json)

    print(dic_json)
    max_hour=int(dic_json['max_hour'])
    no_con_bz_min_hour=int(dic_json['no_con_bz_min_hour'])
    no_con_bz_max_hour = int(dic_json['no_con_bz_max_hour'])
    shutdown_max_hour=int(dic_json['shutdown_max_hour'])
    shutdown_min_hour =int(dic_json['shutdown_min_hour'])
    print(shutdown_min_hour)
    for key in dic_json['con']:
        if isinstance(dic_json['con'][key],dict)==False:
            print("****key--：%s value--: %s"%(key,dic_json['con'][key]))
    while True:
        today_week = datetime.datetime.now().weekday()+1
        hour = time.localtime().tm_hour
        print(hour)
        if hour <12 or hour >14:
            print('studay')
        if today_week>=1 and today_week<=5:
            time.sleep(random.randint(0,90))
        else:
            time.sleep(random.randint(300,900))
            
        if hour <= max_hour:
            for key in dic_json['con']:
                if isinstance(dic_json['con'][key],dict)==False:  
                    print("****key--：%s value--: %s"%(key,dic_json['con'][key]))
                    countProcessMemoey(key,int(dic_json['con'][key]))
                
            if hour <no_con_bz_min_hour or hour >=no_con_bz_max_hour:
                print('check bz')
                countProcessMemoey(bz,1000)
        elif hour==19:
            if time.localtime().tm_min>40:
                time.sleep(random.randint(0,300))
                os.system("shutdown -s -f -t 0")
        elif hour==20:
            if time.localtime().tm_min>50:
                time.sleep(random.randint(0,300))
                os.system("shutdown -s -f -t 0")
        elif hour==21:
            if time.localtime().tm_min>40:
                time.sleep(random.randint(0,300))
                os.system("shutdown -s -f -t 0")
        elif hour==22:
            if time.localtime().tm_min>30:
                time.sleep(random.randint(0,300))
                os.system("shutdown -s -f -t 0")
        else:
            time.sleep(random.randint(300,900))
            for key in dic_json['con']:
                if isinstance(dic_json['con'][key],dict)==False:
                    print("****key--：%s value--: %s"%(key,dic_json['con'][key]))
                    countProcessMemoey(key,int(dic_json['con'][key]))

        if hour >=shutdown_max_hour or hour <shutdown_min_hour:
            os.system("shutdown -s -f -t 0")
                
        time.sleep(180) 
    
       
           

