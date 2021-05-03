# -*- coding: utf-8 -*-
import os
import sys
import json
import glob
import MeCab
from difflib import SequenceMatcher , Differ

NG_PATTERN_DIR = './input/ng_pattern/**'

OUTPUT_DIR = './output/'
FILE_NAME = 'result'

# jsonファイルの読み込み
CHAT_KEYS = ["authorExternalChannelId","user","timestampUsec","time","authorbadge","text","purchaseAmount","type","video_id","Chat_No"]
DICT_CHAT_CHANNNELID = 0
DICT_CHAT_TEXT = 5
DICT_CHAT_KEY = 9

NG_RESULT_KEYS = ["pattern","similarity"]
INDEX_NG_RESULT_PATTERN = 0
INDEX_NG_RESULT_SIMILARITY = 1

# 類似度閾値
SIMILARITY_THRESHOLD = 0.8

NG_FLG_KEY = 'ng_flg'
NG_INFO_KEY = 'ng_info'

# 辞書ファイルパス
DIC_PATH = ' -d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd'

def read_comment_json(input_file):
    """ コメントjsonを読み込む
    """
    return_dict = {}

    with open(INPUT_FILE, mode='r') as f:
        comments = json.load(f)
        for comment in comments:
            return_dict[comment[CHAT_KEYS[DICT_CHAT_KEY]]] = comment

    return return_dict

def read_ng_pattern():
    """ NGパターンの形態素解析結果を読み込んで返す
    """
    ng_pattern = {}
    for file in [p for p in glob.glob(NG_PATTERN_DIR , recursive=True) if os.path.isfile(p) and os.path.splitext(p)[1][1:] == 'gitkeep' ]:
        with open(file) as f:
            ng_pattern[file] = f
    return ng_pattern


def get_ng_chat_id(comment_dict, ng_pattern, threshold):
    """ NGパターンに引っかかったコメントIDと、どのパターンに引っかかったかを返す。
    """
    ng_comments = []
    for comment_key in comment_dict:
        mplg_result = mplg(comment_dict[comment_key][CHAT_KEYS[DICT_CHAT_TEXT]])
        for ng_key in ng_pattern:
            similarity = SequenceMatcher(
                None,mplg_result,ng_pattern[ng_key]).ratio()
            if similarity > threshold:
                ng_comments[comment_key] = {
                    NG_RESULT_KEYS[INDEX_NG_RESULT_PATTERN]: ng_key,
                    NG_RESULT_KEYS[INDEX_NG_RESULT_SIMILARITY]: similarity
                }
    return ng_comments

def merge_ng_comments(comments, ng_comments):
    """ コメントにNG情報を付与する
    """
    
    return_comments = comments
    
    for key in comments:
        ng_info = {}
        if key in ng_comments:
            return_comments[key]['ng_flg'] = True
            ng_info = ng_comments[key]
        else:
            return_comments[key]['ng_flg'] = False

        return_comments[key]['ng_info'] = ng_info
    return return_comments

def mplg(text):
    """ 形態素解析を行う。
    """
    m = MeCab.Tagger(DIC_PATH)
    soup = m.parse (text)
    return soup


if __name__ == '__main__':
    args_index = 0
    args_index = args_index + 1

    VIDEO_ID = sys.argv[args_index] ; args_index = args_index + 1;
    INPUT_FILE = sys.argv[args_index] ; args_index = args_index + 1;

    # NGパターンを読み込む
    ng_pattern = read_ng_pattern()

    # コメントファイルをdictに変換する。
    item_dict = read_comment_json(INPUT_FILE)

    # NGェック
    ng_comments = get_ng_chat_id(item_dict, ng_pattern, 0.8)

    # コメントにNGフラグ、引っかかったパターン、類似度を付与する。
    comments_ng_merged = merge_ng_comments(item_dict, ng_comments)    
    
    print(json.dumps(comments_ng_merged))
