# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 00:11:15 2018

@author: GIN
"""
import jieba
import csv
import numpy as np

jieba.set_dictionary('dict.txt.big')#繁體專用
gooddict = []
baddict = []
comparedict = []
mostdict = []
verydict = []
moredict = []
ishdict = []
lessdict = []
constant = 5#作為算分基準
count = 0
usrdict = []
usrdictpos = []
findlist = []
writelist = {}#寫入用

def opendict(path):
    newlist = []
    with open(path,'r',encoding = 'utf-8') as f:
        for data in f.readlines():
            data = data.strip()
            newlist.append(data)
    return newlist

def analyzedata(wordlist):
    tempdata = []
    goodtemp = []
    badtemp = []
    goodcount = 0
    badcount = 0
    prevword = ''
    #wordlist = jieba.cut(content,cut_all=False)
    for word in wordlist:
        if word in gooddict:
            badcount = 0
            if prevword in mostdict:
                goodcount = 25
            elif prevword in verydict:
                goodcount = 20
            elif prevword in moredict:
                goodcount = 15
            elif prevword in ishdict:
                goodcount = 10
            elif prevword in lessdict:
                goodcount = 7
            elif prevword in baddict:
                goodcount =0
                badcount = 0
            else:
                goodcount = 5
        elif word in baddict:
            goodcount = 0
            if prevword in mostdict:
                badcount = 25
            elif prevword in verydict:
                badcount = 20
            elif prevword in moredict:
                badcount = 15
            elif prevword in ishdict:
                badcount = 10
            elif prevword in lessdict:
                badcount = 7
            elif prevword in baddict:
                goodcount = 5
                badcount = -5
            elif prevword in gooddict:
                goodcount =-5
                badcount = 5
            else:
                badcount = 5
        elif word in usrdict:
            badcount = 60
            goodcount = 0
        elif word in usrdictpos:
            badcount = 0
            goodcount = 60
        else:
            badcount = 0
            goodcount = 0
        goodtemp.append(goodcount)
        badtemp.append(badcount)
        prevword = word
    tempdata.append(goodtemp)
    tempdata.append(badtemp)
    return tempdata
def givedata(scorelist):
    templist = []
    scorearray = np.array(scorelist)
    pos = np.sum(scorearray[0])
    neg = np.sum(scorearray[1])
    avgpos = np.mean(scorearray[0])
    avgneg = np.mean(scorearray[1])
    stdpos = np.std(scorearray[0])
    stdneg = np.std(scorearray[1])
    templist.append(pos)
    templist.append(neg)
    templist.append(avgpos)
    templist.append(avgneg)
    templist.append(stdpos)
    templist.append(stdneg)
    return templist
gooddict = opendict('positive.txt')
baddict = opendict('negative.txt')
comparedict = opendict('adventure.txt')

mostdict = comparedict[comparedict.index('1. “極其|extreme / 最|most”	69')+1:comparedict.index('2. “很|very”	42')-1]#讀取比較慈
verydict = comparedict[comparedict.index('2. “很|very”	42')+1:comparedict.index('3. “較|more”	37')-1]
moredict = comparedict[comparedict.index('3. “較|more”	37')+1:comparedict.index('4. “稍|-ish”	29')-1]
ishdict = comparedict[comparedict.index('4. “稍|-ish”	29')+1:comparedict.index('5. “微|insufficiently”	12')-1]
lessdict = comparedict[comparedict.index('5. “微|insufficiently”	12')+1:comparedict.index('6. “超|over”	30')-1]

#1.使用者input資料
"""
data =  input('>>> 輸入資料: ')
print('確認開啟:',data)
"""

#data = 'course98.csv'
file2 = open('test.csv','w', newline='')#newline能解除多一航空白的問題
'''
testdata1 = '用了幾天又來評價的，手機一點也不卡，玩榮耀的什麼的不是問題，充電快，電池夠大，玩遊戲可以玩幾個小時，待機應該可以兩三天吧，很贊'
testdata2 = '不知道怎麼講，真心不怎麼喜歡，通話時聲音小，新手機來電話竟然卡住了接 不了，原本打算退，剛剛手機摔了，又退不了，感覺不會再愛，圖元不知道是我不懂還是 怎麼滴 感覺還沒z11mini好，哎要我怎麼評價 要我如何喜歡努比亞 太失望了'
#usrdict = opendict('usrdict.txt')
sentence1 =  testdata1.strip()
wordlist1 = jieba.lcut(sentence1,cut_all=False)
gglist = wordlist1[:]
tempdata1 = givedata(analyzedata(wordlist1))
print(tempdata1)
print(gglist)
'''

choice = int(input('>>>輸入功能選擇 1為關鍵字過濾、2為資料分析:'))
if choice == 2:
   fieldname2 = ['內容','正值','負值','平均正','平均負','標準正','標準負']
   writelist['內容'] = '內容'
   writelist['正值'] = '正值'
   writelist['負值'] = '負值'
   writelist['平均正'] = '平均正'
   writelist['平均負'] = '平均負'
   writelist['標準正'] = '標準正'
   writelist['標準負'] = '標準負'
   writer = csv.DictWriter(file2,fieldname2)
   writer.writerow(writelist)
   writelist.clear()
   usrdict = opendict('usrdict.txt')#read the special word
   usrdictpos = opendict('usrdictpos.txt')#read the special word
   with open('course98.csv','r') as f:
       for testfile in csv.DictReader(f):
           count= count + 1
           if(count>50000):
               print("here")
               break
           else:          
               sentence = testfile['第四部份對本科目的任何意見和建議']
               if sentence != '':
                   sentence = sentence.strip()
                   wordlist = jieba.lcut(sentence,cut_all=False)
                   tempdata = givedata(analyzedata(wordlist))
                   writelist['內容'] = sentence
                   writelist['正值'] = tempdata[0]
                   writelist['負值'] = tempdata[1]
                   writelist['平均正'] = tempdata[2]
                   writelist['平均負'] = tempdata[3]
                   writelist['標準正'] = tempdata[4]
                   writelist['標準負'] = tempdata[5]
                   writer.writerow(writelist)
                   writelist.clear()
  
elif choice == 1:
    fieldnames = ['學年度','學期','開課系號','開課序號','第一部份授課老師','第二部分綜合評估','第三部份學生自我評量','第四部份對本科目的任何意見和建議','教師代碼','學號','課程代號']
    writer = csv.DictWriter(file2,fieldnames)
    makechoice = input('>>>輸入欲尋找關鍵字(輸入exit離開):')
    while makechoice  != 'exit':
        decision = int(input('>>>輸入此關鍵字屬性，1為正向，2為負向，3為無所謂'))
        if decision == 1:
            usrdictpos.append(makechoice)
            findlist.append(makechoice)
        elif decision == 2:
            usrdict.append(makechoice)
            findlist.append(makechoice)
        elif decision == 3:
            findlist.append(makechoice)
        else:
            print('wrong input')
            continue
        makechoice = input('>>>輸入欲尋找關鍵字(輸入exit離開):')
    file3 = open('usrdict.txt','a',encoding = 'utf-8')#寫入關鍵字詞點
    file4 = open('usrdictpos.txt','a',encoding = 'utf-8')#寫入關鍵字詞點
    for word in usrdict:
        file3.write(word+'\n')
    for word in usrdictpos:
        file4.write(word+'\n')
    file3.close()
    file4.close()
    
    with open('course98.csv','r') as f:
        for testfile in csv.DictReader(f):
            count= count +1
            if(count>50000):
                print("here")
                break
            else:
                sentence = testfile['第四部份對本科目的任何意見和建議']
                if sentence !='':  
                    words = jieba.lcut(sentence,cut_all=False)
                    for word in words:
                        if word in findlist:
                            writer.writerow(testfile)
                            break

file2.close()
