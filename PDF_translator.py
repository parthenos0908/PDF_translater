import argparse
import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import os
import sys
import time


def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True


def get_text_from_pdf(filepath, pdfname, limit=1000):

    # 処理するPDFファイルを開く/開けなければ
    try:
        fp = open(filepath + "/" + pdfname + ".pdf", 'rb')
    except:
        print("ファイルが見つかりません")
        print("注意) PDFファイルはexeファイルと同じディレクトリに配置してください")
        sys.exit()

    # PDFからテキストの抽出
    rsrcmgr = PDFResourceManager()
    out_fp = StringIO()
    la_params = LAParams()
    la_params.detect_vertical = True
    device = TextConverter(rsrcmgr, out_fp, codec='utf-8', laparams=la_params)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None, caching=True, check_extractable=True):
        interpreter.process_page(page)
    text = out_fp.getvalue()
    fp.close()
    device.close()
    out_fp.close()

    with open(filepath + "/" + pdfname + "_unshaped.txt", "w", encoding="UTF-8") as f_t:
        f_t.write(text)

    # 改行で分割する
    lines = text.splitlines()

    outputs = []
    output = ""

    # 置換文字の辞書
    replace_byte_dict = {
        # NUL
        b'\x00': b'',
        # 合字
        b'\xef\xac\x80': b'ff',
        b'\xef\xac\x81': b'fi',
        b'\xef\xac\x82': b'fl',
        b'\xef\xac\x83': b'ffi',
        b'\xef\xac\x84': b'ffl',
        b'\xef\xac\x85': b'ft',
        b'\xef\xac\x86': b'st',
    }

    replace_char_dict = {
        "(cid:129)": "•",
    }

    is_period_end = False
    is_blank_line = False

    # 分割した行でループ
    for line in lines:

        # tmp = line
        # print(tmp)
        # time.sleep(0.5)

        # byte文字列に変換
        line_utf8 = line.encode('utf-8')

        # 余分なバイトコードを除去する
        for b in replace_byte_dict:
            line_utf8 = line_utf8.replace(b, replace_byte_dict[b])

        # strに戻す
        line = line_utf8.decode()

        for c in replace_char_dict:
            line = line.replace(c, replace_char_dict[c])

        # 連続する空白を一つにする
        line = re.sub("[ ]+", " ", line)

        # 両端の連続する空白文字を削除
        line = line.strip()

        # 空行は無視
        if len(line) == 0:
            output += "\n"
            is_blank_line = True
            continue

        # 数字だけの行は無視
        if is_float(line):
            continue

        # # 1単語しかなく、末尾がピリオドで終わらないものは無視
        # if len(line.split(" ")) == 1 and not line.endswith("."):
        #     continue

        # 文章の切れ目の場合
        if is_blank_line:
            # 文字数がlimitを超えていたらここで一旦区切る
            if(len(output) > limit):
                output = re.sub("\n\n+", "\n\n", output)  # 3回以上重複した改行の削除
                outputs.append(output)
                output = "\n"
            else:
                output += "\n"
        # 前の行からの続きの場合
        elif output.endswith("-"):
            output = output[:-1]
        # それ以外の場合は、単語の切れ目として半角空白を入れる
        else:
            if output:  # 文頭に空白が入る事の回避
                output += " "

        output += str(line)
        is_blank_line = False

    outputs.append(output)
    return outputs


def translate(text):
    if text:
        pass
    else:
        return ""
    api_url = "https://script.google.com/macros/s/AKfycbz6c_xIZ_gbmE-VHldaFgcB-IlqfIeqVYtTrWzpWij0qCrdXxAr/exec"
    params = {
        'text': text,
        'source': 'en',
        'target': 'ja'
    }

    r_post = requests.post(api_url, data=params)
    return r_post.json()['text']


def main():
    mode = input(
        'モードを選択してください\n 0. PDF → txt\n 1. txt → taranslated_txt\n 2. PDF → txt → taranslated_txt\nplease enter a number : ')
    if(mode == "0" or mode == "1" or mode == "2"):
        mode = int(mode)
    else:
        print("未定義の入力です")
        sys.exit()

    # os.path.dirname(__file__)だとexe化した時にうまく動かない
    path = os.path.dirname(sys.argv[0])
    if mode in [0, 2]:
        filename = input('PDFファイル名を入力してください（拡張子不要）: ')
        texts = get_text_from_pdf(path, filename, limit=2000)
        f_text = open(path + "/" + filename + ".txt", "w", encoding="utf-8")
    elif mode in [1]:
        filename = input('txtファイル名を入力してください（拡張子不要）: ')
        try:
            with open(path + "/" + filename + ".txt", "r", encoding="utf-8") as f_input_text:
                input_texts = f_input_text.readlines()
        except:
            print("ファイルが見つかりません")
            print("注意) txtファイルはexeファイルと同じディレクトリに配置してください")
            sys.exit()

        # １行ずつだと翻訳時間が長いので，文字数上限を超えないようにまとめる
        MAX_char = 3000
        texts = []
        block = ""
        for text in input_texts:
            if len(text) > MAX_char:
                if block != "":
                    texts.append(block)
                    block = ""
                texts.append(text)
                continue
            tmp = block + text
            if len(tmp) > MAX_char:
                texts.append(block)
                block = text
            else:
                block = tmp
        texts.append(block)


    if mode in [1, 2]:
        f_trans = open(path + "/" + filename +
                       '_translate.txt', "w", encoding="utf-8")

    # pdfをテキストに変換
    # 一定文字列で分割した文章毎にAPIを叩く
    for i, text in enumerate(texts):
        # 結果をファイルに出力
        if(mode != 1):
            f_text.write(text)
        if(mode != 0):
            print(
                "[taranslate : {0}/{1} is proccessing]".format((i+1), len(texts)))
            text_translate = translate(text)
            f_trans.write(text_translate)
            time.sleep(1)  # google翻訳のエラー回避

    if(mode != 1):
        f_text.close()
    if(mode != 0):
        f_trans.close()

    print("succeeded!")
    time.sleep(1)


if __name__ == "__main__":
    main()
