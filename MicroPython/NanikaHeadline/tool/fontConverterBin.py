import sys
import binascii

args = sys.argv

fileName = args[1]
fontFile = open(fileName, 'r')

fontBinaryFile = open("fontData.bin", 'wb')
fontIndexFile = open("fontIndex.txt", 'w')
fontCodeFile = open("fontCode.csv", 'w')
fontCodeFileBin = open("fontCode.bin", 'wb')

fontChar = ""
fontCode = ""
fontDataCount = 0
findBitmap = False
fontBitmap = bytearray([])
fontOrderHash = {} #キー：Unicode 値：フォントファイルでのOffset
index = 0;
for line in fontFile:

	#フォントデータ読み込みモードの場合、13行読み込む。13行読み込み完了時にソース出力
	if fontDataCount > 0:
		fontLineData = int("0x" + line[:-1], 0)
		hData = int(fontLineData >> 8) #上位バイト
		lData = fontLineData & 0x00FF  #下位バイト
		fontBitmap.append(hData)
		fontBitmap.append(lData)
		
		fontDataCount = fontDataCount + 1
		if fontDataCount > 13:
			fontBinaryFile.write(fontBitmap)
			fontDataCount = 0
			fontCodeFile.write(str(index - 1) + "," + fontChar + "," + fontCode + "," + hex(ord(fontChar)) + "," + str(ord(fontChar)) + "\r")

	#STARTCHARが来たらJISコードで文字に変換して保持
	if line.find("STARTCHAR") != -1:
		fontCode = line[12:16]
		try:
			fontChar = binascii.unhexlify("1b2442" + fontCode).decode('iso-2022-jp')
			fontOrderHash[ord(fontChar)] = index
			findBitmap = True #次に見つけたBITMAPをフォントデータとして取り込む
			fontIndexFile.write('"' + fontChar + '",')
			index = index + 1
			if index % 10 == 0:
				fontIndexFile.write('\r')
		except:
			#print("#" + fontCode + ":変換不可")
			fontChar = ""
			continue

	#BITMAPが来たらそこから13行がフォントデータ
	if line.find("BITMAP") != -1:
		if findBitmap == True:
			fontBitmap = bytearray([])
			fontDataCount = 1
			findBitmap = False

for fontOrder in range(1,65535):
	if fontOrderHash.get(fontOrder):
		fontOffset = fontOrderHash[fontOrder]
	else:
		fontOffset = 0
	fontOffsetBin = bytearray([])
	hData = int(fontOffset >> 8) #上位バイト
	lData = fontOffset & 0x00FF  #下位バイト
	fontOffsetBin.append(hData)
	fontOffsetBin.append(lData)
	fontCodeFileBin.write(fontOffsetBin)
		

fontFile.close()
fontBinaryFile.close()
fontIndexFile.close()
fontCodeFile.close()
fontCodeFileBin.close()