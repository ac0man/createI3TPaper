"""The main proc for createI3TPaper app."""

import os
import random
import shutil
import sys
from typing import Any, Dict, List

from dicts import Words_dict as Dct

import env

from paths import PathConst as Paths


import requests


def create_words4exam(words: List[Dict[int, str]]):
    """用語リスト（10要素）を作成する"""
    # 合計で10個の用語一覧を作成する為、各辞書における必要最大要素数（MAX_ENO）を定義する
    # {'words_en': 1, '_katakana1': 2, '_katakana2': 4, '_material': 3, }
    MAX_ENO = [1, 2, 4, 3]
    wd4e = []

    for i, d in enumerate(words):
        # 辞書の値をリストとして全取得し、その内から重複なしでランダムに指定個数分を取得後、返却リストに追加
        rnd_words = random.sample(list(d.values()), MAX_ENO[i])
        wd4e.append(rnd_words)

    # 2次元配列から1次元配列に変換
    wd4e = [ls1[j] for i, ls1 in enumerate(wd4e) for j, ls2 in enumerate(ls1)]

    return wd4e


def make_newdir(dirpath: str):
    """指定した名称でディレクトリを作成する"""
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


def export2txt_words4exam(words4exam: List[str]):
    """TODO 連日に渡るIT用語の重複回避を分析する用途として用語リストを保存する."""

    dirpath = Paths().DIR_words4analyze
    # ファイル出力用のディレクトリが存在しない場合、新規作成する
    make_newdir(dirpath)

    # 用語リストを本日付けで保存する
    newfile = Paths().gen_FILE_WORD_LIST
    shutil.copy(Paths().PATH_template_1st, dirpath + newfile)


def export2md_paper(words4exam: List[str]):
    dirpath = Paths().DIR_exam_papers
    # ファイル出力用のディレクトリが存在しない場合、新規作成する
    make_newdir(dirpath)

    # テンプレをコピー＆本日付けで別ファイルとして保存する
    newfile = Paths().gen_FILE_EXAM_PAPER()
    shutil.copy(Paths().PATH_template_1st, dirpath + newfile)

    # 用語リストの箇所に引数で受け取った用語を書き込む
    with open(dirpath + newfile, 'a', encoding='utf-8') as fst:
        for word in words4exam:
            fst.write('- ' + word + '\n')

        with open(Paths().PATH_template_2nd, 'r', encoding='utf-8') as snd:
            read_data = snd.read()
            fst.write(read_data)

    print(' Exported.')

    upload2slack(dirpath, newfile)
    return


def upload2slack(dirpath: str, newfile: str):
    """生成したファイルを指定のSlackチャンネルに送信する"""
    # 入力チェック
    if dirpath is None:
        # dirpath をデフォルトで設定する
        dirpath = Paths().DIR_exam_papers

    if newfile is None:
        newfile = Paths().FILE_EXAM_PAPER
        # 本日付けの確認テスト用ファイルを探索し、存在しない場合は異常終了
        if not os.path.exists(dirpath + newfile):
            print(' Today\'s file not found: ')
            sys.exit(1)

    URL_UPLOAD = "https://slack.com/api/files.upload"

    with open(dirpath + newfile, 'rb') as f:
        f = {'file': f.read()}
        p = {
            'token': env.TOKEN,
            'channels': env.CHANNEL_ID,
            'filename': newfile,
            'filetype': 'md',
            'initial_comment': "―【説明】―――――――――――――――――\
                                \n　*添付ファイルをダウンロード後、以下を行いアップロードして下さい。*\
                                \n　　1. 解答欄に記述\
                                \n　　2. 記述後、ファイルを保存\
                                \n　　3. ファイル名の変更（\"~_name.md\"  ← name を変更する）\
                                \n\
                                \n―【解答方法】―――――――――――――――\
                                \n　*合計 10P に達するように、解答用紙記載の用語リストを用いて文章を作成せよ。*\
                                \n　　・参考リンクに記載のサイト等を利用し、自身で意味を調べて解答すること。\
                                \n　　・１つの文章は、句点までを１文とみなす。\
                                \n　　・１文あたり何語使用するかで加点が異なる。\
                                \n　　　- １語のみ ： 1P UP↑\
                                \n　　　- ２語　　 ： 3P UP↑\
                                \n　　　- ３語以上 ： 5P UP↑\
                                \n　　・用語リスト内から選択する際、１語以上であれば使用語数に制限はない。\
                                \n　　・各文章間で用語が重複している場合、その文章は無効とする。\
                                \n　",
            'title': "解答用紙_IT用語テスト",
        }
        r = requests.post(url=URL_UPLOAD, params=p, files=f)

    if str(r.status_code) == '200':
        print(' Uploaded.')
    else:
        print(' Upload_failed: ', r)

    return


def response_debug(r: Any = None):
    if r is None:
        print('オブジェクト不明')
        sys.exit(1)
    # Paths.
    # リクエストURLの確認
    print(r.url)
    # レスポンス内容の確認
    print(r.status)


def main():
    # 用語集が定義された辞書を格納したリストを取得する
    words = Dct().words_lists

    # 辞書の最大要素数の取得→辞書から乱数で要素番号にアクセスして任意の要素を取得する
    words4exam = create_words4exam(words)

    # md形式で問題を出力し、slackにアップロードする
    export2md_paper(words4exam)

    # 今回選ばれた10個の単語を標準出力する
    print('\n Words list:')
    for word in range(0, len(words4exam)):
        print('  - ' + words4exam[word])

    print('\n Done!!\n')


if __name__ == '__main__':
    main()
    sys.exit(0)
