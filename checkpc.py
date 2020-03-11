#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding:gbk
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
        except Exception e:
            print(e)
            
 

if __name__ == '__main__':

    ProcessName = 'QQBrowser.exe'
    ProcessName2 = "chrome.exe"
    iename="MicrosoftEdgeSH.exe"
    ienamesh="MicrosoftEdgeSH.exe"
    sogou="SogouExplorer.exe"
    ie10="MicrosoftEdgeCP.exe"
    bz="BilibiliUwpApp.exe"
    today_week = datetime.datetime.now().weekday()+1
    while True:
        if today_week>=1 and today_week<=5:
            hour = time.localtime().tm_hour
            if hour <= 19:
                time.sleep(random.randint(0,90))
                countProcessMemoey(ProcessName2,200480)
                countProcessMemoey(iename,200480)
                countProcessMemoey(ProcessName,100480)
                countProcessMemoey(ienamesh,200480)
                countProcessMemoey(sogou,200480)
                countProcessMemoey(ie10,100480)
                if hour <12 or hour >14:
                    countProcessMemoey(bz,1000)
            if hour >=23:
                os.system("shutdown -s -f -t 0")
                
        time.sleep(60)
        
   
