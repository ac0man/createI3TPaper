"""The paths for createI3TPaper app."""

from datetime import datetime as time


class PathConst:
    """createI3TPaper_main.py で使用するパスを定義したクラス."""

    DIR_words4analyze = './words4analyze/'
    DIR_exam_papers = './exam_papers/'
    FILE_WORD_LIST = ''
    FILE_EXAM_PAPER = ''
    PATH_template_1st = './templates/template_1st.md'
    PATH_template_2nd = './templates/template_2nd.md'

    def set_FILE_WORD_LIST(self, newfile: str):
        """分析用ファイル名を自身へ設定. private メソッド."""
        self.FILE_WORD_LIST = newfile

    def set_FILE_EXAM_PAPER(self, newfile: str):
        """テスト用ファイル名を自身へ設定. private メソッド."""
        self.FILE_EXAM_PAPER = newfile

    def gen_FILE_WORD_LIST(self, date: str = time.today().strftime('%Y%m%d')):
        """IT用語リストのファイル名を生成して自身に設定後、呼び出し元に返却."""

        newfile = 'wd4eList_{}.txt'.format(date)
        self.set_FILE_WORD_LIST(newfile)

        return self.FILE_WORD_LIST

    def gen_FILE_EXAM_PAPER(self, date: str = time.today().strftime('%Y%m%d')):
        """IT用語テスト用紙のファイル名を生成して自身に設定後、呼び出し元に返却."""

        newfile = 'IT用語テスト_{}_name.md'.format(date)
        self.set_FILE_EXAM_PAPER(newfile)

        return self.FILE_EXAM_PAPER
