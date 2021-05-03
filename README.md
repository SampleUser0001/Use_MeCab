# Use MeCab

形態素解析を使用して、YoutubeのNGコメントを検出する。  
事前に[Get_NG_Pattern](https://github.com/SampleUser0001/Get_NG_Pattern)でパターンを作成しておく。

## 実行

1. ```app/input/${動画ID}.json```に[GetYoutubeArchiveComment](https://github.com/SampleUser0001/GetYoutubeArchiveComment)で取得したコメント.jsonファイルを取得する。
   - [GetYoutubeArchiveComment](https://github.com/SampleUser0001/GetYoutubeArchiveComment)はYoutubeの規約で、公開停止。
2. ```app/input/ng_pattern```配下にNGパターンの形態素解析結果を配置する。
   - [Get_NG_Pattern](https://github.com/SampleUser0001/Get_NG_Pattern)で作成したパターン
3. ```docker-compose.yml```の```VIDEO_ID```を${動画ID}に修正。
4. ```docker-compose up```を実行。

## 実行結果

### 出力パス

``` sh
./app/output/result_${動画ID}.json
```

### 出力パターン

```
{
  "authorExternalChannelId": "（隠蔽）",     # コメント投稿者のチャンネルID
  "user": "（隠蔽）",                        # コメント投稿者名
  "timestampUsec": "1618180355896087",      # コメント投稿時刻(UnixTime)
  "time": "2:00",                           # コメント投稿時間(配信開始時からの経過時間)
  "authorbadge": "",                        # コメント投稿者の属性(一般/メンバー(期間)/モデレータ等)
  "text": "(一応隠蔽)",                      # 投稿コメント
  "purchaseAmount": "￥200",                # スーパーチャットで投げられた金額
  "type": "SUPERCHAT",                      # コメント種類
  "video_id": "1h78n8hzpqg",                # 動画ID
  "Chat_No": "00552"                        # コメントID（動画内で何番目に投稿されたコメントかの番号）
  "ng_flg": true,                           # NGコメント判定されたか
  "ng_info": {                              # NGのときのみ出力
    "pattern": "./input/ng_pattern/pmTQqhpHAHs/00096.txt", # どのパターンでNGになったか
    "similarity": 1                                        # 検出されたパターンとの一致度
  }
},
```


## 参考

- [PythonとMecabで形態素解析をする:Qiita](https://qiita.com/DisneyAladdin/items/eb72a47f6543efe2b951)
- [MeCab](http://taku910.github.io/mecab/)
  - 形態素解析エンジン
- [Python difflib 覚書:はてだBlog（仮称）](https://itdepends.hateblo.jp/entry/2020/03/04/225605)
