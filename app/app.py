# -*- coding: utf-8 -*-
import os
import sys
import json
import glob
import MeCab
from difflib import SequenceMatcher , Differ

NG_PATTERN_DIR = './input/ng_pattern/**'

OUTPUT_COMMENT_DIR = './output/comment/'
OUTPUT_CHANNEL_DIR = './output/channel/'
OUTPUT_USER_DIR = './output/user/'

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

# YoutubeチャンネルURL
YOUTUBE_CHANNEL = 'https://www.youtube.com/channel/'

def read_comment_json(input_file):
    """ コメントjsonを読み込む
    """
    return_dict = []

    with open(INPUT_FILE, mode='r') as f:
        comments = json.load(f)
        for comment in comments:
            return_dict.append(comment)

    return return_dict

def read_ng_pattern():
    """ NGパターンの形態素解析結果を読み込んで返す
    """
    ng_pattern = {}
    for file in [p for p in glob.glob(NG_PATTERN_DIR , recursive=True) if os.path.isfile(p) and os.path.splitext(p)[1][1:] != 'gitkeep' ]:
        with open(file) as f:
            ng_pattern[file] = f.read()
            # print(ng_pattern[file])
    return ng_pattern


def get_ng(comment_list, ng_pattern, threshold):
    """ NGパターンに引っかかったコメントIDと、どのパターンに引っかかったかを返す。
    Parameters:
    ----
    comment_list : jsonの配列
        読み込んだコメントの配列。
        read_comment_json(string)の戻り値。
    ng_pattern : dict
        読み込んだNGパターンの形態素解析結果の辞書。
        read_ng_pattern()の戻り値。
    threshold : float
        類似度のしきい値。
    
    Returns:
    ----
    ng_comments: dict
        NG判定したコメントの辞書。
        key : コメントID
        value : json
            pattern : 一致した形態素解析結果ファイル
            similarity : 類似度
    ng_channel_list : list
        NG判定したチャンネルURL
    ng_user_list : list
        NG判定したユーザID
    """
    ng_comments = {}
    ng_channel_list = []
    ng_user_list = []
    for comment_key in range(0, len(comment_list)):
        mplg_result = mplg(comment_list[comment_key][CHAT_KEYS[DICT_CHAT_TEXT]])
        for ng_key in ng_pattern:
            similarity = SequenceMatcher(
                None,mplg_result,ng_pattern[ng_key]).ratio()
            if similarity > threshold:
                ng_comments[comment_key] = {
                    NG_RESULT_KEYS[INDEX_NG_RESULT_PATTERN]: ng_key,
                    NG_RESULT_KEYS[INDEX_NG_RESULT_SIMILARITY]: similarity
                }
                
                # ユーザの取得
                ng_user = comment_list[comment_key][CHAT_KEYS[DICT_CHAT_CHANNNELID]]
                if ng_user not in ng_user_list:
                    ng_user_list.append(ng_user)
                    ng_channel_list.append(YOUTUBE_CHANNEL + ng_user)
                break
    return ng_comments, ng_channel_list, ng_user_list

def merge_ng_comments(comment_list, ng_comment_dict):
    """ コメントにNG情報を付与する
    """
    
    return_comment_list = []

    for key in range(0, len(comment_list)):
        comment_info = comment_list[key]
        if key in ng_comment_dict:
            comment_info[NG_FLG_KEY] = True
            comment_info[NG_INFO_KEY] = ng_comment_dict[key]
        else:
            comment_info[NG_FLG_KEY] = False

        return_comment_list.append(comment_info)
    return return_comment_list

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

    # コメントファイルを配列に変換する。
    comment_list = read_comment_json(INPUT_FILE)

#    with open('./tmp/test.json' , mode='w') as f:
#        f.write(json.dumps(comment_infos))

    # NGェック
    ng_comment_dict, ng_channel_list, ng_user_list = get_ng(comment_list, ng_pattern, 0.8)

    # コメントにNGフラグ、引っかかったパターン、類似度を付与する。
    comments_ng_merged = merge_ng_comments(comment_list, ng_comment_dict)

    # NGフラグを付与したコメントを出力する。
    with open(OUTPUT_COMMENT_DIR + VIDEO_ID + '.json' , mode='w') as f:
        f.write(json.dumps(comments_ng_merged))

    # print(ng_channel_list)
    # NG判定したチャンネル一覧を出力する
    with open(OUTPUT_CHANNEL_DIR + VIDEO_ID + '.txt' , mode='w') as f:
        f.write('\n'.join(ng_channel_list))
        # newlineオプション + writelines関数が聞かない？
        
    # NG判定したユーザ一覧を出力する
    with open(OUTPUT_USER_DIR + VIDEO_ID + '.txt' , mode='w') as f:
        f.write('\n'.join(ng_user_list))