import time
import sys

import os
import datetime
import json
import requests
from selenium import webdriver
from optparse import OptionParser

#python3 aguri.py -y 2016 -c 2

TARGET_DIR = "./image"
if not os.path.isdir(TARGET_DIR):
    os.makedirs(TARGET_DIR)

parser = OptionParser()

parser.add_option(
    '-y', '--year',
    action = 'store',
    type = 'str',
    dest = 'year',
)

parser.add_option(
    '-c', '--cours',
    action = 'store',
    type = 'str',
    dest = 'cours',
)

parser.add_option(
    '-s', '--sleep_second',
    action = 'store',
    type = 'int',
    dest = 'sleep_sec',
)

parser.set_defaults(
    year = 2017,
    cours_id = 1,
    sleep_sec = 5
)

options, args = parser.parse_args()

year = options.year
cours = options.cours
sleep_sec = options.sleep_sec


url = 'http://api.moemoe.tokyo/anime/v1/master/' + year + '/' + cours
result = requests.get(url)

master_list = json.loads(result.text)

create_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')


browser = webdriver.PhantomJS()

browser.implicitly_wait(3)
browser.set_window_size(1920, 1200)


for master in master_list:

    title = master['title']

    url = master['public_url']

    filename = create_time + "_" + str(master['id']) + ".png"

    print(title + " " + url + " " + filename)

    browser.get(url)

    # CSSアニメーションが始まるサイトが多いので５秒ぐらいは待つ必要がある
    time.sleep(sleep_sec)

    # TODO 動画が始まるサイトは強制的にCLOSEする処理を入れる -> 左上を一度クリックする
    # <button title="Close (Esc)" type="button" class="mfp-close">×</button>
    # <button type="button" id="cboxClose">close</button>
    # <div class="mfp-bg mfp-fade mfp-ready" style="height: 1238px; position: absolute;"></div>
    # <div id="cboxClose" class="" style="">close</div> <---さくらクエスト
    # <button type="button" id="cboxClose">close</button>

    # 動画ダイアログがあったら消す
    browser.execute_script('var e = document.getElementById("colorbox"); if(e){e.parentNode.removeChild(e);}')
    browser.execute_script('var e = document.getElementById("cboxOverlay"); if(e){e.parentNode.removeChild(e);}')

    browser.execute_script('var e = document.getElementsByClassName("mfp-skip_bt"); if(e.length > 0){e[0].click();}')
    browser.execute_script('var e = document.getElementById("skip_bt"); if(e){e.click();}')
    browser.execute_script('var e = document.getElementsByClassName("lity-close"); if(e.length > 0){e[0].click();}')
    browser.execute_script('var e = document.getElementsByClassName("mfp-close"); if(e.length > 0){e[0].click();}')

    # ベルセルク / アトム
    # <div id="skip_bt"><a id="skip_button" href="javascript:void(0);"><img src="core_sys/images/sys/close_bt.gif"></a></div>

    # カド
    # <button class="lity-close" type="button" title="Close (Esc)" data-lity-close="">×</button>

    #おらとりあ
    # <button title="Close (Esc)" type="button" class="mfp-close">×</button>

    # http://www.jacklmoore.com/colorbox
    #<div id="cboxOverlay" style="opacity: 0.9; cursor: pointer;"></div> この要素ごと消す
    #<div id="colorbox" class="" role="dialog" tabindex="-1" style="display: block; visibility: visible; top: 141px; left: 167px; position: absolute; width: 855px; height: 584px;"><div id="cboxWrapper" style="height: 584px; width: 855px;"><div><div id="cboxTopLeft" style="float: left;"></div><div id="cboxTopCenter" style="float: left; width: 855px;"></div><div id="cboxTopRight" style="float: left;"></div></div><div style="clear: left;"><div id="cboxMiddleLeft" style="float: left; height: 552px;"></div><div id="cboxContent" style="float: left; width: 855px; height: 552px;"><div id="cboxLoadedContent" style="width: 853px; overflow: auto; height: 550px;"> <iframe frameborder="0" name="1506181249227" allowfullscreen="" src="top_info.html" class="cboxIframe"></iframe></div><div id="cboxTitle" style="float: left; display: block;"></div><div id="cboxCurrent" style="float: left; display: none;"></div><button type="button" id="cboxPrevious" style="display: none;"></button><button type="button" id="cboxNext" style="display: none;"></button><button type="button" id="cboxSlideshow" style="display: none;"></button><div id="cboxLoadingOverlay" style="float: left; display: none;"></div><div id="cboxLoadingGraphic" style="float: left; display: none;"></div><button type="button" id="cboxClose">close</button></div><div id="cboxMiddleRight" style="float: left; height: 552px;"></div></div><div style="clear: left;"><div id="cboxBottomLeft" style="float: left;"></div><div id="cboxBottomCenter" style="float: left; width: 855px;"></div><div id="cboxBottomRight" style="float: left;"></div></div></div><div style="position: absolute; width: 9999px; visibility: hidden; max-width: none; display: none;"></div></div>

    #youtube組み込み
    # <button title="Close (Esc)" type="button" class="mfp-close">×</button>

    time.sleep(1)
    browser.save_screenshot(TARGET_DIR + "/" + filename)


browser.quit()

