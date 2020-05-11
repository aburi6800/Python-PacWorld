import time
import tkinter
import random
import os
from PIL import Image, ImageTk, ImageDraw

############################################################################### 
# 初期処理
############################################################################### 

# 仮想VRAMのサイズ
VRM_WIDTH = 40
VRM_HEIGHT = 24

# ゲームの状態
GAMESTATUS_TITLE = 0
GAMESTATUS_START = 1
GAMESTATUS_MAIN = 2
GAMESTATUS_MISS = 3
GAMESTATUS_OVER = 4


# スクリプトのパス
basePath = os.path.abspath(os.path.dirname(__file__))

# 空の仮想VRAM配列
blankRow = [0] * VRM_WIDTH
vrm = [blankRow] * VRM_HEIGHT

# PhotoImageの保存用変数
photoImage = ""

# ゲームの状態管理用
gameStatus = GAMESTATUS_TITLE

# ゲームの経過時間管理用
gameTime = 0

# パックマンのキャラクタパターン
pac_ptn = 0

# ハイスコア
highScore = 2000
score = 0


############################################################################### 
# タイトル
############################################################################### 
def title():
	global pac_ptn

	pac_ptn = (pac_ptn + 1) % 8

############################################################################### 
# 画面描画
############################################################################### 
def drawScreen():
	global photoImage

    # canvasのイメージ削除
	canvas.delete("SCREEN")

	# オフスクリーン作成
	offScreen = img_bg.copy()
	writeText(offScreen,  2,  0, "1UP")
	writeText(offScreen,  1,  1, "{:>6}".format(score) + "0")
	writeText(offScreen, 15,  0, "HIGH-SCORE")
	writeText(offScreen, 17,  1, "{:>6}".format(highScore) + "0")
	writeText(offScreen, 10,  8, (0x9C, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x9D))
	writeText(offScreen, 10,  9, (0x96, 0x20, 0x50, 0x20, 0x41, 0x20, 0x43, 0x20, 0x20, 0x2D, 0x20, 0x20, 0x57, 0x20, 0x4F, 0x20, 0x52, 0x20, 0x4C, 0x20, 0x44, 0x20, 0x96))
	writeText(offScreen, 10, 10, (0x9E, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x9F))
	writeText(offScreen, 15, 15, "JUMP [z]")
	writeText(offScreen, 10, 19, "[1] <=       => [2]")

	# パックマン
	offScreen.paste(img_pac[pac_ptn // 2], (gPos(17), gPos(18))) 

	offScreen = offScreen.resize((offScreen.width * 2, offScreen.height * 2), Image.NEAREST)

	# オフスクリーンでPhotoImage生成
	photoImage = ImageTk.PhotoImage(offScreen)
	canvas.create_image((offScreen.width / 2, offScreen.height / 2), image = photoImage, tag = "SCREEN")


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


############################################################################### 
# メイン処理
############################################################################### 
def main():

	# タイトル
	if gameStatus == GAMESTATUS_TITLE:
		title()

	# 画面描画
	drawScreen()

	root.after(50, main)


# Windowを生成
root = tkinter.Tk()
root.geometry(str(VRM_WIDTH * 8 * 2) + "x" + str(VRM_HEIGHT * 8 * 2))
root.title("PAC-WORLD on Python")

# Canvas生成
canvas = tkinter.Canvas(width = (VRM_WIDTH * 8 * 2), height = (VRM_HEIGHT * 8 * 2))
canvas.pack()

# BG生成
img_bg = Image.new("RGBA", (VRM_WIDTH * 8, VRM_HEIGHT * 8), (0, 0, 0))

# フォントイメージ
img_fonts = loadImage(basePath + os.sep + "Images" + os.sep + "p8font.png")
img_font = []
for h in range(0, img_fonts.height, 8):
	for w in range(0, img_fonts.width, 8):
		img = img_fonts.crop((w , h, w + 8, h + 8))
		img_font.append(img)

# パックマン
img_pac = [
	loadImage(basePath + os.sep + "Images" + os.sep + "pac00.png"),
	loadImage(basePath + os.sep + "Images" + os.sep + "pac01.png"),
	loadImage(basePath + os.sep + "Images" + os.sep + "pac02.png"),
	loadImage(basePath + os.sep + "Images" + os.sep + "pac03.png"),
	loadImage(basePath + os.sep + "Images" + os.sep + "pac04.png"),
	loadImage(basePath + os.sep + "Images" + os.sep + "pac05.png")
]

# メイン処理
main()

# ウィンドウイベントループ実行
root.mainloop()
