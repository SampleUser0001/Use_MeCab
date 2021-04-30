# -*- coding: utf-8 -*-
import os
import csv
import glob
import subprocess

INPUT_FILE = './input/pmTQqhpHAHs.csv'
OUTPUT_DIR = './output/'
FILE_NAME = 'result'

# csvファイルの読み込み
CHAT_KEYS = ["authorExternalChannelId","user","timestampUsec","time","authorbadge","text","purchaseAmount","type","video_id","Chat_No"]
DICT_CHAT_KEYS = 9
# 形態素解析結果の行数
MORPHOLOGICAL_ANALYSIS_KEYS = ["line_count"]
INDEX_LINE_COUNT = 0

item_dict = {}

# チャットコメントを読み込む
with open(INPUT_FILE, mode='r', newline='', encoding='utf-8') as f:
    csv_reader = csv.DictReader(f, delimiter=',')
    for row in csv_reader:
        items = {}
        for key in CHAT_KEYS:
            items[key] = row[key]
        item_dict[FILE_NAME + row[DICT_CHAT_KEYS]] = items

# 形態素解析結果を読み込む
# 行数取得
files = glob.glob(OUTPUT_DIR + '*')
for file in files:
    item_dict[os.path.basename(file)][MORPHOLOGICAL_ANALYSIS_KEYS[0]] = int(subprocess.check_output(['wc', '-l', file]).decode().split(' ')[0])

print(item_dict['result12777'])

# 形態素解析結果の差分を取得する
for filename in item_dict.key:
    if item_dict[filename][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_LINE_COUNT]] > 50:
        # 形態素解析結果が50行以上の場合のみDiffする。
        for diff_filename in item_dict.key:
            if item_dict[diff_filename][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_LINE_COUNT]] > 50:
                # 比較対象のファイルも50行以上の場合のみDiffする。
