from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import re
import urllib.parse
import chromedriver_binary


def translate_deepl(from_text, from_lang="en", to_lang="ja", sleep_time=1, try_max_count=30):
    url = 'https://www.deepl.com/translator#' + from_lang + '/' + to_lang

    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--user-agent=Mozilla/5.0')

    # ブラウザーを起動
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(20)  # 見つからないときは、20秒まで待つ
    textarea = driver.find_element_by_css_selector(
        '.lmt__textarea.lmt__source_textarea.lmt__textarea_base_style')  # deeplのtextボックス
    textarea.send_keys(from_text)

    # 入力文字列の末尾の改行を保持(翻訳結果で消されるため)
    match = re.search(r'\n+$', from_text)
    end_newline = ""
    if match:
        end_newline = match.group()

    for i in range(try_max_count):
        time.sleep(sleep_time)
        html = driver.page_source
        to_text = get_text_from_page_source(html)
        if to_text:
            break
    driver.quit()  # ブラウザ停止
    return to_text + end_newline


def get_text_from_page_source(html):
    soup = BeautifulSoup(html, features="html.parser")
    # deeplの翻訳結果出力(<div id="source-dummydiv" class="lmt__textarea lmt__textarea_dummydiv">はうまくいかず)
    target_elem = soup.find(class_="lmt__translations_as_text__text_btn")
    text = target_elem.text
    return text


if __name__ == '__main__':
    from_lang = 'en'
    to_lang = 'ja'
    from_text = 'ABSTRACT\nhe is a man\n\n'

    # 翻訳
    to_text = translate_deepl(from_text)
    print(to_text)
