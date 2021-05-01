# -*- coding: utf-8 -*-
import os
import sys
import json
import glob
import MeCab

import subprocess

OUTPUT_DIR = './output/'
FILE_NAME = 'result'

# jsonファイルの読み込み
CHAT_KEYS = ["authorExternalChannelId","user","timestampUsec","time","authorbadge","text","purchaseAmount","type","video_id","Chat_No"]
DICT_CHAT_TEXT = 5
DICT_CHAT_KEY = 9
# 形態素解析結果
MORPHOLOGICAL_ANALYSIS_KEYS = ["mplg_words","mplg_text","line_count"]
INDEX_MPLG_WORDS = 0
INDEX_MPLG_TEXT = 1
INDEX_LINE_COUNT = 2

# 辞書ファイルパス
DIC_PATH = ' -d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd'
# DIC_PATH = ' -d /usr/local/mecab/lib/mecab/dic/ipadic'

def read_comment_json(input_file):
    """ コメントjsonを読み込む
    """
    return_dict = {}

    with open(INPUT_FILE, mode='r') as f:
        comments = json.load(f)
        for comment in comments:
            return_dict[comment[CHAT_KEYS[DICT_CHAT_KEY]]] = comment

    return return_dict


def morphological_analysis(dict_comments):
    """ 形態素解析を行い、dict型で返す。
    形態素解析結果はCHAT_KEYS[DICT_CHAT_KEY]の値をキーにしたdict型で返す。
    """
    return_dict = {}
    for key in dict_comments:
        # コメントを取得
        comment = dict_comments[key][CHAT_KEYS[DICT_CHAT_TEXT]]

        # print(comment)

        # 形態素解析を行う
        words, text = mplg(comment)

        # dict型に変換して返す。
        mplg_result = {INDEX_MORPHOLOGICAL_ANALYSIS[INDEX_MPLG_WORDS]: words , INDEX_MORPHOLOGICAL_ANALYSIS[INDEX_MPLG_TEXT]: text}
        return_dict[key] = mplg_result

def mplg(text):
    """ 形態素解析を行う。
    """
    output_words = []
    output_text  = ''
    # 辞書へのパス
    m = MeCab.Tagger(DIC_PATH)
    # m = MeCab.Tagger()
    soup = m.parse (text)
    for row in soup.split("\n"):
        word =row.split("\t")[0]
        if word == "EOS":
            break
        else:
            pos = row.split("\t")[1]
            slice = pos.split(",")
            if len(word) > 1:
                if slice[0] == "名詞":
                    output_words.append(word)
                    output_text = output_text + ' ' + word
                elif slice[0] in [ "形容詞" , "動詞", "副詞"]:
                    if slice[5] == "基本形":
                        output_words.append(slice[-3])#活用していない原型を取得
                        output_text = output_text + ' ' + slice[-3]
    return output_words,output_text


def get_diff_morphological_analysis():
    """ 形態素解析結果の差分を取得する
    """
    # 行数取得
    files = glob.glob(OUTPUT_DIR + '*')
    for file in files:
        item_dict[os.path.basename(file)][MORPHOLOGICAL_ANALYSIS_KEYS[0]] = int(subprocess.check_output(['wc', '-l', file]).decode().split(' ')[0])

    # 形態素解析結果の差分を取得する
    for filename in item_dict.key:
        if item_dict[filename][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_LINE_COUNT]] > 50:
            # 形態素解析結果が50行以上の場合のみDiffする。
            for diff_filename in item_dict.key:
                if item_dict[diff_filename][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_LINE_COUNT]] > 50:
                    # 比較対象のファイルも50行以上の場合のみDiffする。
                    pass

if __name__ == '__main__':
    args_index = 0
    args_index = args_index + 1

    INPUT_FILE = sys.argv[args_index] ; args_index = args_index + 1;

    # print('INPUT_FILE : ' + INPUT_FILE)

    item_dict = read_comment_json(INPUT_FILE)

    mplg_dict = morphological_analysis(item_dict)
    print(mplg_dict['00000'])
