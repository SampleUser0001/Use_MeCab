# -*- coding: utf-8 -*-
import os
import sys
import json
import glob
import MeCab
from difflib import SequenceMatcher , Differ

import subprocess

OUTPUT_DIR = './output/'
FILE_NAME = 'result'

# jsonファイルの読み込み
CHAT_KEYS = ["authorExternalChannelId","user","timestampUsec","time","authorbadge","text","purchaseAmount","type","video_id","Chat_No"]
DICT_CHAT_CHANNNELID = 0
DICT_CHAT_TEXT = 5
DICT_CHAT_KEY = 9

# 形態素解析結果
MORPHOLOGICAL_ANALYSIS_KEYS = ["mplg_words","mplg_text","mplg_soup"]
INDEX_MPLG_WORDS = 0
INDEX_MPLG_TEXT = 1
INDEX_MPLG_SOUP = 2

# 形態素解析結果差分
SIMILARITY_DIFF_KEYS = ["origin_authorExternalChannelId", "diff_chat_no", "diff_authorExternalChannelId", "similarity"]
INDEX_SIMILARITY_ORIGIN_CHANNEL_ID = 0
INDEX_SIMILARITY_DIFF_CHAT_NO = 1
INDEX_SIMILARITY_DIFF_CHANNEL_ID = 2
INDEX_SIMILARITY = 3

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

def morphological_analysis(comments_dict):
    """ 形態素解析を行い、dict型で返す。
    形態素解析結果はCHAT_KEYS[DICT_CHAT_KEY]の値をキーにしたdict型で返す。
    """
    return_dict = {}
    for key in comments_dict:
        # コメントを取得
        comment = comments_dict[key][CHAT_KEYS[DICT_CHAT_TEXT]]

        # print(comment)

        # 形態素解析を行う
        words, text = mplg_edit(comment)
        soup = mplg(comment)

        # dict型に変換して返す。
        mplg_result = {
            MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_WORDS]: words ,
            MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_TEXT]: text ,
            MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_SOUP]: soup }
        return_dict[key] = mplg_result

    return return_dict

def mplg(text):
    """ 形態素解析を行う。
    """
    m = MeCab.Tagger(DIC_PATH)
    soup = m.parse (text)
    return soup

def mplg_edit(text):
    """ 形態素解析を行う。必要な項目だけ取得する。
    TODO: 必要な項目を絞り込む
    """
    output_words = []
    output_text  = ''
    # 辞書へのパス
    m = MeCab.Tagger(DIC_PATH)
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

def get_over_length_keys(mplg_dict, length):
    """ コメントの形態素解析結果のサイズがlength以上のkeyの一覧を返す。
    """
    
    return_list = []
    for key in mplg_dict:
        if len(mplg_dict[key][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_SOUP]].splitlines()) > length:
            return_list.append(key)
    return return_list

def get_diff_morphological_analysis(comments_dict, mplg_dict, key_list):
    """ 形態素解析結果の差分を取得する
    """

    return_list = []
    
    for key in key_list:
        for diff_key in key_list:
            if int(key) < int(diff_key):
                similarity = SequenceMatcher(
                    None,
                    mplg_dict[key][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_SOUP]],
                    mplg_dict[diff_key][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_SOUP]]).ratio()
                if similarity > 0.8:
                    return_list.append({
                        'chat_id': key,
                        SIMILARITY_DIFF_KEYS[INDEX_SIMILARITY_ORIGIN_CHANNEL_ID]: comments_dict[key][CHAT_KEYS[DICT_CHAT_CHANNNELID]],
                        SIMILARITY_DIFF_KEYS[INDEX_SIMILARITY_DIFF_CHAT_NO]: diff_key,
                        SIMILARITY_DIFF_KEYS[INDEX_SIMILARITY_DIFF_CHANNEL_ID]: comments_dict[diff_key][CHAT_KEYS[DICT_CHAT_CHANNNELID]],
                        SIMILARITY_DIFF_KEYS[INDEX_SIMILARITY]: similarity})
    return return_list

if __name__ == '__main__':
    args_index = 0
    args_index = args_index + 1

    INPUT_FILE = sys.argv[args_index] ; args_index = args_index + 1;

    # コメントファイルをdictに変換する。
    item_dict = read_comment_json(INPUT_FILE)

    # 取得したコメントファイルのコメントを形態素解析する。
    mplg_dict = morphological_analysis(item_dict)
    
#    # 類似度を取得する
#    text00104 = mplg_dict['00104'][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_SOUP]]
#    text00299 = mplg_dict['00299'][MORPHOLOGICAL_ANALYSIS_KEYS[INDEX_MPLG_SOUP]]
#    print(SequenceMatcher(None, text00104, text00299).ratio())

    diff_morphological_analysis = get_diff_morphological_analysis(item_dict, mplg_dict, get_over_length_keys(mplg_dict, 50))
    print(json.parse(diff_morphological_analysis))
