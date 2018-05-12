from m5stack import *
import random
import urequests
import ujson
import json
from jpfont import jpfont
import uos
import gc
import time
import YahooHeadline

class nanika:
    
    def __init__(self):
        self.wordList = ["それな","そやな","しらんがな","まじか…","ＳＯＲＥＮＡ","ＳＯＹＡＮＡ","わかる","うける","はつみみ","あー、あれね","どゆこと？",
                "なるほどー","完全に理解","しってた","そっちかー","はじまったな","そっすね","それだ！","ええーっ！？","何だってー！",
                "株の買い時！","最の高では？","と、いうと？","神！","ふーん","わかるわかる","なんでや！","ワンチャン","ションボリ","もう限界では",
                "まだいける！","がんばるぞい"]
        #self.sakuraList = ["/sd/sakura01.jpg","/sd/sakura01.jpg","/sd/sakura01.jpg","/sd/sakura01.jpg","/sd/sakura01.jpg","/sd/sakura01.jpg","/sd/sakura02.jpg"]
        self.sakuraList = ["/sd/nisenise01.jpg"]
        uos.mountsd()
        self.jpfontObj = jpfont()
        random.seed(int(time.time()))

        #Yahooヘッドライン取得（XML）
        self.maxCategoty = YahooHeadline.getCategoryCount()
        self.nowCategory = 4
        self.titleTextList = YahooHeadline.getYahooHeadline(self.nowCategory)
        self.nowTitleIndex = 0

        #最大 13x8
        lcd.clear()
        lcd.image(0, 0, random.choice(self.sakuraList))
        lcd.setCursor(0, 0)
        lcd.setColor(lcd.BLACK)
        self.nextNews()

        buttonA.wasPressed(self.on_AwasPressed)
        buttonB.wasPressed(self.on_BwasPressed)
        buttonC.wasPressed(self.on_CwasPressed)
    
        self.autoNewsCount = 0
        self.autoNews()
    
    def printNews(self, newsTitle): 
        rowCount = int(len(newsTitle) / 7) + 1;
        #lcd.print("4")
        if rowCount <= 3:
            offsetY = 1
        else:
            offsetY = 0
        totalRowIndex = 0
        lcd.roundrect(6,24,175,134, 5, 0xF1FDEF, 0xF1FDEF)
        lcd.triangle(181, 104, 181, 108, 185, 108,  0xF1FDEF, 0xF1FDEF)
    
        for rowIndex in range(rowCount):
            rowTitle = newsTitle[7 * rowIndex:7 * rowIndex + 7]
            self.jpfontObj.printString(rowTitle.strip(), 5, (totalRowIndex + offsetY) * 12 + 15)
            totalRowIndex = totalRowIndex + 1
    
        lcd.roundrect(2, 184, 158, 47, 5, 0xF1FDEF, 0xF1FDEF)
        lcd.triangle(160, 210, 160, 214, 164, 214,  0xF1FDEF, 0xF1FDEF)
        self.jpfontObj.printString(random.choice(self.wordList), 4, 98)
        gc.collect()

    def nextNews(self):
        self.autoNewsCount = 0
        lastNewsFlag = False
        if len(self.titleTextList) ==0 :
            return
        self.printNews(self.titleTextList[self.nowTitleIndex])
        self.nowTitleIndex = self.nowTitleIndex + 1
        if self.nowTitleIndex >= len(self.titleTextList):
            self.nowTitleIndex = 0
            lastNewsFlag = True
        return lastNewsFlag
        
    def prevCategory(self):
        lcd.image(0, 0, random.choice(self.sakuraList))
        self.autoNewsCount = 0
        self.nowCategory = self.nowCategory - 1
        if self.nowCategory < 0:
            self.nowCategory = self.maxCategoty - 1           
        self.titleTextList = YahooHeadline.getYahooHeadline(self.nowCategory)
        self.nowTitleIndex = 0
        self.nextNews()
    
    def nextCategory(self):
        lcd.image(0, 0, random.choice(self.sakuraList))
        self.autoNewsCount = 0
        self.nowCategory = self.nowCategory + 1
        if self.nowCategory >= self.maxCategoty:
            self.nowCategory = 0
        self.titleTextList = YahooHeadline.getYahooHeadline(self.nowCategory)
        self.nowTitleIndex = 0
        self.nextNews()

    def on_AwasPressed(self): #カテゴリ戻り
        self.prevCategory()

    def on_BwasPressed(self): #次のニュース表示
        self.nextNews()
    
    def on_CwasPressed(self): #カテゴリ進み
        self.nextCategory()

    def autoNews(self):
        lastNewsFlag = False
        while True:
            time.sleep(1)
            self.autoNewsCount = self.autoNewsCount + 1
            if self.autoNewsCount > 5:
                if lastNewsFlag == True:
                    self.nextCategory()
                    lastNewsFlag = False
                else:
                    lastNewsFlag = self.nextNews()