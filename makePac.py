import os
from PIL import Image, ImageTk, ImageDraw

############################################################################### 
# パックマンの画像生成プログラム
############################################################################### 

# キャラクタサイズ
VRM_WIDTH = 5
VRM_HEIGHT = 4

# スクリプトのパス
basePath = os.path.abspath(os.path.dirname(__file__))


############################################################################### 
# テキスト描画
# 引数		img 貼り付け先のImageデータ
#  			x テキスト座標系のx座標
#			y テキスト座標系のy座標
#			str 表示する文字データの配列（文字の場合は、文字コードに対応した文字を表示する）
############################################################################### 
def writeText(img, x, y, s):
	# 文字を描画
	for i in range(len(s)):
		if isinstance(s, str):
			o = ord(s[i]) - 32
		else:
			o = s[i] - 32

		if o >= 0 and o <= len(img_font):
			img.paste(img_font[o], (gPos(x + i), gPos(y)), img_font[o])


############################################################################### 
# 指定されたパスの画像をロードして2倍に拡大したImageを返却する
# 引数		filepath 画像データのフルパス
# 戻り値	2倍に拡大したImageデータ
############################################################################### 
def loadImage(filePath):

	img = Image.open(filePath).convert("RGBA")
	return img


############################################################################### 
# テキスト座標系からグラフィック座標系に変換する
# 引数      value 変換する値
# 戻り値    変換後の値
############################################################################### 
def gPos(value):

	return value * 8


# BG生成
img_bg = Image.new("RGBA", (VRM_WIDTH * 8, VRM_HEIGHT * 8), (0, 0, 0))

# イメージをロード
img_fonts = loadImage(basePath + os.sep + "Images" + os.sep + "p8font.png")
img_font = []
for h in range(0, img_fonts.height, 8):
	for w in range(0, img_fonts.width, 8):
		img = img_fonts.crop((w , h, w + 8, h + 8))
		img_font.append(img)

offScreen = img_bg.copy()
writeText(offScreen, 0, 0, (0x20, 0xE5, 0x87, 0x84, 0x20))
writeText(offScreen, 0, 1, (0x20, 0x96, 0x20, 0x93, 0xED))
writeText(offScreen, 0, 2, (0x20, 0xED, 0x95, 0x9F, 0x20))
writeText(offScreen, 0, 3, (0x20, 0x20, 0x87, 0x20, 0x20))
offScreen.save(basePath + os.sep + "Images" + os.sep + "pac00.png")

offScreen = img_bg.copy()
writeText(offScreen, 0, 0, (0x20, 0xE5, 0x87, 0x84, 0xED))
writeText(offScreen, 0, 1, (0x98, 0x92, 0x20, 0x93, 0x9B))
writeText(offScreen, 0, 2, (0xED, 0x9E, 0x95, 0x9F, 0x20))
writeText(offScreen, 0, 3, (0x20, 0x8B, 0x20, 0xE5, 0x20))
offScreen.save(basePath + os.sep + "Images" + os.sep + "pac01.png")

offScreen = img_bg.copy()
writeText(offScreen, 0, 0, (0x20, 0xE5, 0x86, 0x83, 0x20))
writeText(offScreen, 0, 1, (0x20, 0x96, 0x20, 0x93, 0xED))
writeText(offScreen, 0, 2, (0x20, 0xED, 0x95, 0x9F, 0x20))
writeText(offScreen, 0, 3, (0x20, 0x20, 0x87, 0x20, 0x20))
offScreen.save(basePath + os.sep + "Images" + os.sep + "pac02.png")

offScreen = img_bg.copy()
writeText(offScreen, 0, 0, (0x20, 0xE5, 0x87, 0x84, 0x20))
writeText(offScreen, 0, 1, (0x20, 0x96, 0xED, 0x96, 0x00))
writeText(offScreen, 0, 2, (0x20, 0x9E, 0x95, 0x9F, 0x20))
writeText(offScreen, 0, 3, (0x20, 0xE7, 0x20, 0xE5, 0x20))
offScreen.save(basePath + os.sep + "Images" + os.sep + "pac03.png")

offScreen = img_bg.copy()
writeText(offScreen, 0, 0, (0x20, 0xE5, 0x86, 0x83, 0xED))
writeText(offScreen, 0, 1, (0x9C, 0x92, 0x20, 0x93, 0x9F))
writeText(offScreen, 0, 2, (0xED, 0x9E, 0x95, 0x9F, 0x20))
writeText(offScreen, 0, 3, (0x20, 0xE7, 0x20, 0x20, 0xE5))
offScreen.save(basePath + os.sep + "Images" + os.sep + "pac04.png")

offScreen = img_bg.copy()
writeText(offScreen, 0, 0, (0x20, 0xE5, 0x87, 0x84, 0xED))
writeText(offScreen, 0, 1, (0xED, 0x96, 0x20, 0x93, 0x9F))
writeText(offScreen, 0, 2, (0x20, 0x9E, 0x95, 0x9F, 0x20))
writeText(offScreen, 0, 3, (0x20, 0x20, 0xE7, 0x20, 0xE7))
offScreen.save(basePath + os.sep + "Images" + os.sep + "pac05.png")

