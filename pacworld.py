import time
import tkinter
import random
import os
import csv
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
GAMESTATUS_GAME = 2
GAMESTATUS_MISS = 3
GAMESTATUS_GOAL = 4
GAMESTATUS_OVER = 5

# キー判定用
KEY_LEFT = "Left"
KEY_RIGHT = "Right"
KEY_SPACE = "space"
KEY_Z = "z"

# ジャンプ種別
JUMP_HIGH = 2
JUMP_LOW = 1
JUMP_NO = 0

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

# パックマンのY座標
pac_y = 13

# パックマンのスピード
pac_speed = 0.0

# パックマンジャンプフラグ
pac_jump_flg = JUMP_NO

# パックマンジャンプカウンタ
pac_jump_cnt = 0

# パックマンの残り
pac_left = 2

# ハイスコア
highScore = 2000

# スコア
score = 0

# ボーナス
bonus = 0

# マップの位置
map_x = 0.0

# ポイント
point = 10

# ポイント取得時の位置
point_x = 0

# ポイント取得時のウェイトカウンタ
point_wait_cnt = 0

# ラウンド
round = 0

# 最後に進んだラウンド
lastRound = 0

# キーイベント用
key = ""
keyOff = True


############################################################################### 
# メイン処理
############################################################################### 
def main():
	global gameTime, key, keyOff

	# 画面描画
	draw()

	# 処理
	if gameStatus == GAMESTATUS_TITLE:
		# タイトル処理
		title()

	else:
		# ゲームメイン処理
		game()		

	# 時間進行
	gameTime = gameTime + 1

	# キーリピート対策
	if keyOff == True:
		key = ""
		keyOff = False

	root.after(50, main)


############################################################################### 
# キーイベント：キー押す
############################################################################### 
def pressKey(e):
	global key, keyOff

#	if keyOff == True:
	key = e.keysym
	keyOff = False


############################################################################### 
# キーイベント：キー離す
############################################################################### 
def releaseKey(e):
	global keyOff

	keyOff = True


############################################################################### 
# ゲーム状態変更
############################################################################### 
def changeGameStatus(status):
	global gameStatus, gameTime

	gameStatus = status
	gameTime = 0


############################################################################### 
# タイトル処理
############################################################################### 
def title():
	global key, pac_ptn

	pac_ptn = (pac_ptn + 1) % 8

	if key == KEY_SPACE:
		# ゲーム初期化
		initializeGame(lastRound)
		changeGameStatus(GAMESTATUS_GAME)

	if key == KEY_Z:
		# ゲーム初期化
		initializeGame(0)	
		changeGameStatus(GAMESTATUS_GAME)

	key = ""


############################################################################### 
# ゲーム初期化
############################################################################### 
def initializeGame(startRound):
	global round, score, pac_left

	# ラウンド
	round = startRound

	# スコア
	score = 0

	# パックマンの残り
	pac_left = 2

	# ラウンド初期化
	initializeRound()


############################################################################### 
# ラウンド初期化
############################################################################### 
def initializeRound():
	global pac_y, pac_ptn, pac_speed, pac_jump_flg, pac_jump_cnt, map_x, point, point_x, point_wait_cnt, bonus

	# パックマンのY座標
	pac_y = 13

	# パックマンのキャラクタパターン
	pac_ptn = 0

	# パックマンのスピード
	pac_speed = 0.0

	# パックマンジャンプフラグ
	pac_jump_flg = JUMP_NO

	# パックマンジャンプカウンタ
	pac_jump_cnt = 0

	# マップの位置
	map_x = 0.0

	# ポイント
	point = 10

	# ポイント取得時の位置
	point_x = 0

	# ポイント取得時のウェイトカウンタ
	point_wait_cnt = 0

	# ボーナス
	bonus = 0


############################################################################### 
# ゲーム処理
############################################################################### 
def game():

	if gameStatus == GAMESTATUS_GAME:
		# ゲームメイン処理
		game_main()
		
	elif gameStatus == GAMESTATUS_GOAL:
		# ゴール処理
		game_goal()

	elif gameStatus == GAMESTATUS_MISS:
		# ミス処理
		game_miss()

	elif gameStatus == GAMESTATUS_OVER:
		# ゲームオーバー処理
		game_over()


############################################################################### 
# ゲームメイン処理
############################################################################### 
def game_main():
	global key, score, map_x, pac_y, pac_ptn, pac_speed, pac_jump_flg, pac_jump_cnt, point_x, point, point_wait_cnt

	# スコアアップ
	score = score + int(pac_speed + 0.5)

	# ゴール判定
	map_x = map_x + pac_speed
	if map_x > 410:
		changeGameStatus(GAMESTATUS_GOAL)
		return

	# ジャンプ中？
	if pac_jump_flg != JUMP_NO:
		pac_ptn = 4 + (pac_jump_cnt > 5)
		pac_jump_cnt = pac_jump_cnt + 1
		if pac_jump_flg == JUMP_LOW:
			pac_y = lowJump_y[pac_jump_cnt]
			if pac_jump_cnt == 9:
				pac_jump_flg = JUMP_NO
				pac_jump_cnt = 0
				pac_y = 13
		if pac_jump_flg == JUMP_HIGH:
			pac_y = highJump_y[pac_jump_cnt]
			if pac_jump_cnt == 19:
				pac_jump_flg = JUMP_NO
				pac_jump_cnt = 0
				pac_y = 13

	else:
		# パックマンのスピード
		pac_speed = pac_speed + ((key == KEY_RIGHT and pac_speed < 1.5) - (key == KEY_LEFT and pac_speed > 0)) / 4
		pac_ptn = ((pac_ptn + 1) % 4) * (pac_speed > 0)
	
		# ジャンプ
		if key == KEY_Z:
			pac_jump_cnt = 0
			if map[round][int(map_x) + 11:int(map_x) + 12] == [0x3D]:
				pac_jump_flg = JUMP_HIGH
			else:
				pac_jump_flg = JUMP_LOW

		# 穴判定
		if map[round][int(map_x) + 10:int(map_x) + 15] == [0x20] * 5:
			changeGameStatus(GAMESTATUS_MISS)
			pac_ptn = 5

		# ポイント取得
		if point_wait_cnt > 0:
			point_wait_cnt = point_wait_cnt - 1
			if point_wait_cnt == 0:
				point = point + 2
		if map[round][int(map_x) + 11:int(map_x) + 12] == [0x24] and point_x != int(map_x):
			score = score + point
			if point_wait_cnt > 0:
				point = point + 2
			point_wait_cnt = 4
			point_x = int(map_x)


############################################################################### 
# ゴール処理
############################################################################### 
def game_goal():
	global score, bonus, round, highScore, lastRound

	if gameTime == 1:
		# ボーナス算出・加算
		if pac_jump_flg == JUMP_NO:
			bonus = 500 + pac_ptn * 50
		else:
			bonus = 300 + pac_jump_cnt * 30

		score = score + bonus

	elif gameTime >= 30:
		# 次ラウンドへ
		round = round + 1
		if round < 4:
			initializeRound()
			changeGameStatus(GAMESTATUS_GAME)

	elif gameTime >= 60:
		lastRound = 3
		if score > highScore:
			highScore = score
		# タイトル
		changeGameStatus(GAMESTATUS_TITLE)


############################################################################### 
# ミス処理
############################################################################### 
def game_miss():
	global pac_y, pac_left

	if gameTime < 7:
		pac_y = pac_y + 1

	elif gameTime >= 30:
		pac_left = pac_left - 1
		if pac_left < 0:
			# ゲームオーバー
			changeGameStatus(GAMESTATUS_OVER)
		else:
			# リスタート
			initializeRound()
			changeGameStatus(GAMESTATUS_GAME)


############################################################################### 
# ゲームオーバー処理
############################################################################### 
def game_over():
	global lastRound, highScore

	if gameTime > 30:

		# 最終ラウンド更新
		if round > lastRound:
			lastRound = round

		# ハイスコア更新
		if score > highScore:
			highScore = score

		changeGameStatus(GAMESTATUS_TITLE)


############################################################################### 
# 画面描画
############################################################################### 
def draw():
	global photoImage

    # canvasのイメージ削除
	canvas.delete("SCREEN")


	if gameStatus == GAMESTATUS_TITLE:
		# タイトル
		img_screen = drawTitle()

	else:
		# ゲーム画面
		img_screen = drawGame()

	# 画面イメージを拡大
	img_screen = img_screen.resize((img_screen.width * 2, img_screen.height * 2), Image.NEAREST)

	# オフスクリーンでPhotoImage生成
	photoImage = ImageTk.PhotoImage(img_screen)
	canvas.create_image((img_screen.width / 2, img_screen.height / 2), image = photoImage, tag = "SCREEN")


############################################################################### 
# タイトル画面描画
############################################################################### 
def drawTitle():

	# 画面イメージ作成
	img_screen = img_bg.copy()
	writeText(img_screen,  2,  0, "1UP")
	writeText(img_screen,  1,  1, "{:>6}".format(score) + "0")
	writeText(img_screen, 15,  0, "HIGH-SCORE")
	writeText(img_screen, 17,  1, "{:>6}".format(highScore) + "0")
	writeText(img_screen, 10,  8, (0x9C, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x9D))
	writeText(img_screen, 10,  9, (0x96, 0x20, 0x50, 0x20, 0x41, 0x20, 0x43, 0x20, 0x20, 0x2D, 0x20, 0x20, 0x57, 0x20, 0x4F, 0x20, 0x52, 0x20, 0x4C, 0x20, 0x44, 0x20, 0x96))
	writeText(img_screen, 10, 10, (0x9E, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x95, 0x9F))
	writeText(img_screen, 15, 15, "JUMP [z]")
	writeText(img_screen, 10, 19, "[1] <=       => [2]")

	# パックマン
	img_screen.paste(img_pac[pac_ptn // 2], (gPos(17), gPos(18))) 

	return img_screen


############################################################################### 
# ゲーム画面描画
############################################################################### 
def drawGame():

	# オフスクリーン作成
	img_screen = img_gamebg.copy()

	# パックマンの残り表示
	for i in range(pac_left):
		writeText(img_screen, 30 + i * 3, 0, [0xE6, 0XE5])
		writeText(img_screen, 30 + i * 3, 1, [0xE4, 0XE7])

	# ラウンド表示
	writeText(img_screen, 24, 0, str(round + 1))

	# スコア表示
	writeText(img_screen, 7, 0, "{: 6}0".format(score))

	# ポイント表示
	writeText(img_screen, 5, 1, str(point * 10))

	# マップ描画
	for i in range(40):
		writeText(img_screen, i, 17, (map[round][int(map_x) + i:int(map_x) + i + 40]))

	# パックマン
	img_screen.paste(img_pac[pac_ptn], (gPos(10), gPos(pac_y))) 

	# スコア取得時の表示
	if point_wait_cnt > 0:
		writeText(img_screen, 8, 11, str(point * 10) + "pts")

	# ミスメッセージ
	if (gameStatus == GAMESTATUS_MISS and gameTime > 6) or gameStatus == GAMESTATUS_OVER:
		writeText(img_screen, 13, 8, ">> OUT !! <<")
 
	# ゴール
	if gameStatus == GAMESTATUS_GOAL:
		writeText(img_screen, 21,  7, [0x87, 0x87, 0x87, 0x87, 0x87, 0xEF])
		writeText(img_screen, 21,  8, [0x8C, 0x85, 0x85, 0x85, 0x86, 0x20, 0xEF])
		writeText(img_screen, 21,  9, [0x8C, 0x87, 0x87, 0x87, 0x87, 0x20, 0x97])
		writeText(img_screen, 21, 10, [0x87, 0x87, 0x87, 0x87, 0x87, 0x20, 0x97])
		writeText(img_screen, 21, 11, [0x8C, 0x85, 0x85, 0x85, 0x86, 0x20, 0x97])
		writeText(img_screen, 21, 12, [0x8C, 0x87, 0x87, 0x87, 0x87, 0x20, 0x97])
		writeText(img_screen, 21, 13, [0x87, 0x87, 0x87, 0x87, 0x87, 0x20, 0x97])
		writeText(img_screen, 21, 14, [0x20, 0x20, 0x20, 0x20, 0x20, 0xE6, 0x87])
		writeText(img_screen, 21, 15, [0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xE6, 0x20, 0xE6, 0x87, 0x87, 0x87, 0x87, 0x87, 0xE5])
		writeText(img_screen, 21, 16, [0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xE6, 0x87, 0x87, 0x87, 0x87, 0x87, 0xE5])
		if gameTime > 1:
			writeText(img_screen, 7, 10, "BONUS " + str(bonus * 10))
		if gameTime > 30:
			writeText(img_screen, 12, 8, ">> THE  END <<")

	# ゲームオーバーメッセージ
	if gameStatus == GAMESTATUS_OVER:
		writeText(img_screen, 11, 12, ">> GAME OVER <<")

	return img_screen


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


# Windowを生成
root = tkinter.Tk()
root.geometry(str(VRM_WIDTH * 8 * 2) + "x" + str(VRM_HEIGHT * 8 * 2))
root.title("PAC-WORLD on Python")
root.bind("<KeyPress>", pressKey)
root.bind("<KeyRelease>", releaseKey)

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

# ゲームのメインスクリーン
img_gamebg = img_bg.copy()
writeText(img_gamebg, 2, 0, "1UP :")
writeText(img_gamebg, 3, 1, "$=")
writeText(img_gamebg, 18, 0, "ROUND")
writeText(img_gamebg, 0, 2, (0x20, 0x20, 0x20, 0x20, 0xE4, 0xE5, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xE4, 0xE5, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xE4, 0xE5, 0x20, 0x20, 0x20, 0x20, 0x20))
writeText(img_gamebg, 0, 3, (0x20, 0x20, 0x20, 0xE4, 0x87, 0x87, 0xE5, 0x20, 0x20, 0xE4, 0xE5, 0x20, 0x20, 0xE4, 0x87, 0x87, 0xE5, 0xE4, 0xE5, 0x20, 0x20, 0xE4, 0x87, 0x87, 0xE5, 0xE4, 0xE5, 0x20, 0x20))
writeText(img_gamebg, 0, 4, (0x20, 0x20, 0xE4, 0x87, 0x87, 0xE7, 0xE6, 0xE5, 0xE4, 0x87, 0x87, 0xE5, 0xE4, 0x87, 0x87, 0xE7, 0xE6, 0x87, 0x87, 0xE5, 0xE4, 0x87, 0x87, 0xE7, 0xE6, 0x87, 0x87, 0xE5, 0x20))
writeText(img_gamebg, 0, 5, (0x20, 0xE4, 0x87, 0x87, 0xE7, 0x20, 0x20, 0xE6, 0x87, 0x87, 0xE7, 0xE6, 0x87, 0x87, 0xE7, 0x20, 0x20, 0xE6, 0x87, 0x87, 0x87, 0x87, 0xE7, 0x20, 0x20, 0xE6, 0x87, 0x87, 0xE5))

# ジャンプ時のY座標
lowJump_y = (13, 11, 9, 8 ,7, 7, 8, 9, 11, 13)

# ロングジャンプ時のY座標
highJump_y = (13, 11, 9, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 11, 13)

# マップデータ読み込み
map = []
field_start = [0x87, 0x87, 0x87, 0x87, 0x87, 0x20, 0x53, 0x54, 0x41, 0x52, 0x54, 0x20, 0x3D, 0x3E, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87, 0x87]
field_goal = [0x92, 0x47, 0x4F, 0x41, 0x4C, 0x20, 0x49, 0x4E, 0x93, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83, 0x83]
for i in range(4):
	f = open(basePath + os.sep + "Data" + os.sep + "map0" + str(i + 1) + ".dat")	
	reader = csv.reader(f)
	field = []
	for row in reader:
		for data in row:
			field.append(int(data, 16))
	map.append(field_start + field + field_goal)

# メイン処理
main()

# ウィンドウイベントループ実行
root.mainloop()
