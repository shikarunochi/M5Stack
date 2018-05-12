import random
import m5cloud
import gc
import urequests

yahooHeadlineURLList=[
        "https://news.yahoo.co.jp/pickup/rss.xml",
        "https://news.yahoo.co.jp/pickup/domestic/rss.xml",
        "https://news.yahoo.co.jp/pickup/world/rss.xml",
        "https://news.yahoo.co.jp/pickup/entertainment/rss.xml",
        "https://news.yahoo.co.jp/pickup/computer/rss.xml",
        "https://news.yahoo.co.jp/pickup/local/rss.xml",
        "https://news.yahoo.co.jp/pickup/domestic/rss.xml",
        "https://news.yahoo.co.jp/pickup/sports/rss.xml",
        "https://news.yahoo.co.jp/pickup/science/rss.xml"
        ]

tabooWords=["殺", "軍", "死"] #突っ込みによって不謹慎になりそうなのを外す

def getYahooHeadline(categoryIndex):
    if categoryIndex < len(yahooHeadlineURLList):
        categoryURL = yahooHeadlineURLList[categoryIndex]
    else:
        categoryURL = random.choice(yahooHeadlineURLList)
    
    #Yahooヘッドライン取得（XML）
    yahooHeadLineResponse = urequests.get(categoryURL)
    yahooHeadLine = yahooHeadLineResponse.text
    
    titleTextList = []
    titleCount = 0
    startIndex = 0
    #<title>と</title>の間を取得。最初のtitleはニュースカテゴリ名だけど気にせず読む。
    while titleCount < 10: #念のためMAX10まで
        if not m5cloud.idle():
            break
        yahooHeadLine = yahooHeadLine[startIndex:-1]#前回検索対象となった部分以降のみ取得
        titleStartIndex = yahooHeadLine.find("<title>")
        titleEndIndex = yahooHeadLine.find("</title>")
        if titleStartIndex == -1:
            break
        titleStartIndex = titleStartIndex + 7 #<title>の分をずらす
        titleText = yahooHeadLine[titleStartIndex:titleEndIndex]
        #不謹慎フィルター
        tabooFind = False
        for tabooword in tabooWords:
            if titleText.find(tabooword) != -1:
                tabooFind = True
                break
        if tabooFind == False:
            titleTextList.append(titleText)

        startIndex = titleEndIndex + 1 #以降、この後ろから探す
        titleCount = titleCount + 1

    gc.collect()
    return titleTextList

def getCategoryCount():
    return len(yahooHeadlineURLList)