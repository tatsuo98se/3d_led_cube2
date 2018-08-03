# -*- coding: utf-8 -*-
import base64
import codecs
import json
import os
import os.path
import random
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime as dt
from multiprocessing import Process
from optparse import OptionParser

import numpy as np
#from matplotlib import pyplot as plt
from watchdog import events
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import cv2
from led_framework import LedFramework
from libled.led_cube import LedCubeFactory

GRID_COLUMNS = 16
GRID_ROWS = 32


def search_mark(img, pos):
    u""" search registar mark """

    frmX, toX = 0, 250  # x mark range
    frmY, toY = 0, 250  # y mark range
    if pos == 0:  # left upper
        mark = img[frmY:toY, frmX:toX]
        rect = {"x": frmX, "y": frmY}
    elif pos == 1:  # right upper右
        mark = img[frmY:toY, img.shape[1]-toX:img.shape[1]-frmX]
        rect = {"x": img.shape[1]-toX, "y": frmY}
    elif pos == 2:  # left bottom
        mark = img[img.shape[0]-toY:img.shape[0], frmX:toX]
        rect = {"x": frmX, "y": img.shape[0]-toY}
    else:  # right bottom
        mark = img[img.shape[0]-toY:img.shape[0]-frmY, img.shape[1]-toX:img.shape[1]-frmX]
        rect = {"x": img.shape[1]-toX, "y": img.shape[0]-toY}

    gray = cv2.cvtColor(mark, cv2.COLOR_BGR2GRAY)  # モノクロ化
    ret, bin0 = cv2.threshold(gray, 127, 255, 0)  # ２値化
    # ノイズ除去
    kernel = np.ones((2,2),np.uint8)
    bin = cv2.morphologyEx(bin0, cv2.MORPH_CLOSE, kernel)
    '''
    cv2.imshow('bin0',bin0)
    cv2.imshow('opening',bin)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

    # 輪郭の抽出
    contours, hierarchy = cv2.findContours(bin,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
#    print "contours={}, ".format(len(contours)), "hierarchy={}".format(len(hierarchy))

    if len(contours) > 1:  # １つめの輪郭は矩形そのものになるため1以上のものを確認
        cnt = contours[len(contours)-1]  # 末尾の輪郭
        M = cv2.moments(cnt)  # モーメント
        cx = int(M['m10']/M['m00'])  # 重心X
        cy = int(M['m01']/M['m00'])  # 重心Y
    else:
        return 0, 0  # 輪郭がない場合

    cv2.circle(img, (rect["x"] + cx, rect["y"]+cy), 10, (0, 0, 255), -1)
#    print (cx, cy), '=', (rect["x"] + cx, rect["y"] + cy)
    return rect["x"] + cx, rect["y"] + cy  # 関数の戻り値


def search_registration_marks(img):
    u""" search registration marks"""
    cx0, cy0 = search_mark(img, 0)  # 左上のトンボの重心（基準）
    dx0, dy0 = search_mark(img, 1)  # 右上のトンボの重心（基準）
    ex0, ey0 = search_mark(img, 2)  # 左下のトンボの重心（基準）
    fx0, fy0 = search_mark(img, 3)  # 右下のトンボの重心（基準）

    count_blanks = 0
    if cx0 == 0 and cy0 == 0:
        count_blanks += 1
    if dx0 == 0 and dy0 == 0:
        count_blanks += 1
    if ex0 == 0 and ey0 == 0:
        count_blanks += 1
    if fx0 == 0 and fy0 == 0:
        count_blanks += 1

    # トンボ3点検出失敗した場合はNoneを返す
    if count_blanks > 1 or count_blanks == 0:
        return None

    pts2 = np.float32([[cx0, cy0], [dx0, dy0], [fx0, fy0]])

    if (ex0 == 0 & ey0 == 0):
        pts2 = np.float32([[cx0, cy0], [dx0, dy0], [fx0, fy0]])
    elif (dx0 == 0 & dy0 == 0):
        pts2 = np.float32([[fx0, fy0], [ex0, ey0], [cx0, cy0]])  # 180度回転
    elif (fx0 == 0 & fy0 == 0):
        pts2 = np.float32([[ex0, ey0], [cx0, cy0], [dx0, dy0]])  # 左90度回転
    else:
        pts2 = np.float32([[dx0, dy0], [fx0, fy0], [ex0, ey0]])  # 右90度回転

    return pts2


def normalize_scan_image(scan_path, form_path):
    ''' normalize scan image'''
    # 比較元画像の読み込み
    src = cv2.imread(form_path)
    pts2 = search_registration_marks(src)
#    print 'src = ', pts2

    # スキャン画像の読み込み
    scan = cv2.imread(scan_path)
    pts1 = search_registration_marks(scan)
#    print 'scan = ', pts1

    if pts1 is not None:
        # アフィン変換
        height, width, ch = src.shape
        M = cv2.getAffineTransform(pts1, pts2)
        dst = cv2.warpAffine(scan, M, (width, height))

        # 画面に収まるようにリサイズして表示
        '''
        resized_scan = cv2.resize(scan, (scan.shape[1]/4, scan.shape[0]/4))
        resized_dst = cv2.resize(dst, (dst.shape[1]/4, dst.shape[0]/4))
        cv2.imshow("scan", resized_scan)
        cv2.imshow("affine", resized_dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        return dst
    return scan


def get_coloring_image(scan, rects_file,
                     saturation_max=False,
                     brightness_max=False):
    ''' get 'very small' coloring from scan img'''

    # 格子矩形情報をRead
    obj_text = codecs.open(rects_file, 'r', encoding='utf-8').read()
    tmp = json.loads(obj_text)
    rects = np.array(tmp)

    # 最終的に取得する16ｘ32の画像の箱を用意
    size = GRID_ROWS, GRID_COLUMNS, 3
    bgr_img = np.zeros(size, dtype=np.uint8)

    # 黒と白を除いた色の平均を求めるため、HSVで色の有無を確認する
    hsv_img = cv2.cvtColor(scan, cv2.COLOR_BGR2HSV)

    # 格子矩形のオフセット 10,10,0.2
    offset = 10
    # 彩度の閾値　彩度が低いものは無視する
    saturation_threshold = 10
    # 格子内で最低限必要なピクセルの割合。この数字以下ははみ出た線として無視する
    color_pixel_ratio = 0.25
#    print 'parms : offset ={0}, saturation_threshold = {1}, color_pixel_ratio = {2}'.format(offset, saturation_threshold, color_pixel_ratio)
#    print "[ X,  Y]  H    S V    [R   G   B  ]  number of pixels"

    idx = 0
    for rect in enumerate(rects):
        r = rect[1]  # r = x, y, w, h
        if r[2] == 0 & r[3] == 0:  # 右端の線はWとHが0なので無視
            continue

        # 格子矩形でクリップ
        cropped = hsv_img[r[1]+offset:r[1]+r[3]-offset, r[0] + offset: r[0]+r[2]-offset]
        cropped = cv2.resize(cropped, (cropped.shape[1]/4, cropped.shape[0]/4))


#        cropped_bgr = scan[r[1]+offset:r[1]+r[3]-offset, r[0]+offset:r[0]+r[2]-offset]
#        plt.imshow(cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB))
#        plt.show()

        # HSVそれぞれの平均を求める（彩度Sがしきい値よりも大きいピクセルのみを採用）
        valid_h_list = [[hsv[0] for hsv in img_line if hsv[1] > saturation_threshold] for img_line in cropped]
        valid_s_list = [[hsv[1] for hsv in img_line if hsv[1] > saturation_threshold] for img_line in cropped]
        valid_v_list = [[hsv[2] for hsv in img_line if hsv[1] > saturation_threshold] for img_line in cropped]
        pixel_count = sum([len(line) for line in valid_h_list])

        average_h, average_s, average_v = 0, 0, 0
        # 色ついたのピクセル数がcolor_pixel_ratioの割合以上であれば採用
        height, width, channels = cropped.shape[:3]
#        if pixel_count > len(cropped) * len(cropped) * color_pixel_ratio:
        if pixel_count > height * width * color_pixel_ratio:
            average_h = (sum([sum(line) for line in valid_h_list]) / pixel_count)
            average_s = (sum([sum(line) for line in valid_s_list]) / pixel_count)
            average_v = (sum([sum(line) for line in valid_v_list]) / pixel_count)
            if saturation_max:
                average_s = 255
            if brightness_max:
                average_v = 255

        # HSV to RGB
        bgr_pixel = cv2.cvtColor(np.array([[[average_h, average_s, average_v]]],
                                          dtype=np.uint8),
                                 cv2.COLOR_HSV2BGR)[0][0]

        # GRID_COLUMNS x GRID_ROWSの画像にピクセル値を設定する
        bgr_img[idx/GRID_COLUMNS, idx-(idx/GRID_COLUMNS)*GRID_COLUMNS] = bgr_pixel

#        print '[{0:2d}, {1:2d}] {2:3d} {3:3d} {4:3d}, {5:3}, {6:3d}'.format(idx / GRID_COLUMNS + 1, idx - (idx / GRID_COLUMNS) * GRID_COLUMNS + 1, int(average_h+0.5), int(average_s+0.5), int(average_v+0.5), bgr_pixel, pixel_count)
        idx = idx + 1

    return bgr_img


def get_checkbox_index(scan, rects_file):
    ''' get chacked box index from scan img'''

    # チェックボックス格子矩形情報をRead
    obj_text = codecs.open(rects_file, 'r', encoding='utf-8').read()
    tmp = json.loads(obj_text)
    rects = np.array(tmp)

    # 黒と白を除いた色の平均を求めるため、HSVで色の有無を確認する
    hsv_img = cv2.cvtColor(scan, cv2.COLOR_BGR2HSV)

    # 格子矩形のオフセット 10,10,0.2
    offset = 5
    # 彩度の閾値　彩度が低いものは無視する
    saturation_threshold = 10
    # 格子内で最低限必要なピクセルの割合。この数字以下ははみ出た線として無視する
    color_pixel_ratio = 0.25

    checked = [False, False, False, False, False, False]
    idx = 0
    for rect in enumerate(rects):
        r = rect[1]  # r = x, y, w, h

        # 格子矩形でクリップ
        cropped = hsv_img[r[1]+offset:r[1]+r[3]-offset, r[0] + offset: r[0]+r[2]-offset]
#        plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_HSV2RGB))
#        plt.show()

        # 彩度Sがしきい値よりも大きいピクセルのみを採用
        valid_h_list = [[hsv[0] for hsv in img_line if hsv[1] > saturation_threshold] for img_line in cropped]
        pixel_count = sum([len(line) for line in valid_h_list])

        # 色ついたのピクセル数がcolor_pixel_ratioの割合以上であれば採用
        height, width, channels = cropped.shape[:3]
        if pixel_count > height * width * color_pixel_ratio:
            checked[idx] = True

        idx = idx + 1

    return checked


def create_coloring(src_path, saturation_max=False, brightness_max=False):
    print "*** start coloring...", src_path

    start = time.time()

    # アフィン変換後のスキャン画像を取得
    scan = normalize_scan_image(src_path, 'asset/coloring/3dledcube_form.jpg')

    # 塗り絵画像を取得
    bgr_img = get_coloring_image(scan,
                                 'asset/coloring/rects.json',
                                 saturation_max,
                                 brightness_max)

    dst_path = SCAN_OUT + dt.now().strftime('%Y%m%d_%H%M%S_%f') + '.png'
    cv2.imwrite(dst_path, bgr_img)
    elapsed_time = time.time() - start
    print ("*** end coloring. elapsed_time:{0}".format(elapsed_time) + "[sec]")

    # チェックボックスを取得
    checked = get_checkbox_index(scan, 'asset/coloring/rects_checkbox.json')
    print checked
    # matplotlibの色空間はRGB
#    plt.imshow(cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB))
#    plt.show()
    return checked


SCAN_IN = 'asset/coloring/scan_in2/'
SCAN_OUT = 'asset/coloring/scan_out/'
SCAN_TMP = 'asset/coloring/scan_tmp'
BASEDIR = SCAN_IN


class ChangeHandler(FileSystemEventHandler):
    ''' watchdog handler '''
    def __init__(self):
        self.led_process = None

    def getext(self, filename):
        return os.path.splitext(filename)[-1].lower()

    def on_created(self, event):
        print('%s has been created.' % event.src_path)
        if event.is_directory:
            return
        if isinstance(event, events.FileCreatedEvent):
            if self.getext(event.src_path) in ('.jpg','.tif','.tiff', '.png'):
                self.do_coloring(event.src_path)

    def on_modified(self, event):
        print('%s has been modified.' % event.src_path)
        if event.is_directory:
            return
#        if isinstance(event, events.FileModifiedEvent):
#            if self.getext(event.src_path) in ('.jpg','.tif','.tiff', '.png'):
#                self.do_coloring(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        print('%s has been deleted.' % event.src_path)

    def do_coloring(self, src_path):

        if self.led_process is not None and self.led_process.is_alive():
            pass
        else:
            if os.path.exists(SCAN_OUT):
                shutil.rmtree(SCAN_OUT)
                os.mkdir(SCAN_OUT)

        if self.getext(src_path) in ('.jpg', '.jpeg', '.png'):
            try:
                checked = create_coloring(src_path,
                                          option_saturation_max,
                                          option_brightness_max)
                self.show_led_on_multiprocess(checked, destip)
            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
                traceback.print_exc()
        elif self.getext(src_path) in ('.tif', '.tiff'):
            # マルチページTIFFをImageMagickでJpegに分解して画像生成
            try:
                if os.path.exists(SCAN_TMP):
                    shutil.rmtree(SCAN_TMP)
                os.mkdir(SCAN_TMP)
                args = ['mogrify.exe', '-path', os.path.abspath(SCAN_TMP), '-format', 'jpeg', os.path.abspath(src_path)]
                res = subprocess.check_output(args)
                print "convert tiff2jpg succeeded.", res
                splitted_imgs = os.listdir(SCAN_TMP)
                for img in sorted(splitted_imgs):
                    checked = create_coloring(os.path.join(SCAN_TMP, img),
                                              option_saturation_max,
                                              option_brightness_max)
                    self.show_led_on_multiprocess(checked, destip)
            except Exception:
                traceback.print_exc()

    def show_led_on_multiprocess(self, checked, destip):
        p = Process(target=show_led, name='show_led', args=(checked,destip,))
        if self.led_process is not None and self.led_process.is_alive():
            self.led_process.terminate()
            self.led_process.join()
        self.led_process = p
        self.led_process.start()



def show_led(checked, destip):

    options = [
        {"id": "filter-zoom"},
        {"id": "filter-rainbow"},
        {"id": "filter-bk-snows"},
        {"id": "filter-bk-grass", "z": 4},
        {"id": "filter-wave"}
    ]

    filters = [
        {"id": "filter-swaying"},
        {"id": "filter-rolldown"},
        {"id": "filter-spiral"},
        {"id": "filter-skewed"},
        {"id": "filter-flat-wave"},
        {"id": "filter-jump"}
    ]

    backgrounds = [
        {"id": "filter-bk-snows"},
        {"id": "filter-bk-sakura"},
        {"id": "filter-bk-mountain", "z": 6},
        {"id": "filter-bk-cloud", "z": 7},
        {"id": "filter-bk-grass", "z": 4},
    ]

    dic = {"orders": []}

    LOOP_COUNT = 10
    
    # 最初は画像のみを表示
    colorings = os.listdir(SCAN_OUT)
    dic["orders"].append({"id": "ctrl-loop", "count": LOOP_COUNT/len(colorings)})
    for coloring in colorings:
        with open(SCAN_OUT + coloring, "rb") as f:
            dic["orders"].append({"id": "object-bitmap", "lifetime": 1, "z": 0, "thick": 3, "bitmap": base64.b64encode(f.read())})

    if destip is not None:
        LedCubeFactory.get_instance().SetUrl(destip)
    ledfw = LedFramework()
    ledfw.show(dic)

    dic = {}
    dic = {"orders": []}

    # オプションに従って表示
    for i, chk in enumerate(checked):
        if chk and i < len(options):
            dic["orders"].append(options[i])
            if i == 3:   # 草原の場合は雲と山も
                dic["orders"].append({"id": "filter-bk-mountain", "z": 6})
                dic["orders"].append({"id": "filter-bk-cloud", "z": 7})
        elif chk:   # [?] はランダム
            dic["orders"].append(random.choice(filters))
            dic["orders"].append(random.choice(backgrounds))

    dic["orders"].append({"id": "ctrl-loop", "count": LOOP_COUNT/len(colorings)})
    colorings = os.listdir(SCAN_OUT)
    for coloring in colorings:
        with open(SCAN_OUT + coloring, "rb") as f:
            dic["orders"].append({"id": "object-bitmap", "lifetime": 1, "z": 0, "thick": 3, "bitmap": base64.b64encode(f.read())})

    ledfw.show(dic)


option_saturation_max = False
option_brightness_max = False
destip = None

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-d", "--dest",
                      action="store", type="string", dest="dest", 
                      help="(optional) device ip adddres.")
    parser.add_option("-s", "--saturation",
                      action="store_true", dest="option_saturation_max",
                      help="(optional) set the saturation to the maximum .")
    parser.add_option("-b", "--brightness",
                      action="store_true", dest="option_brightness_max", 
                      help="(optional) set the brightness to the maximum .")

    options, _ = parser.parse_args()

    if options.dest is not None:
        destip = options.dest
    option_saturation_max = options.option_saturation_max
    option_brightness_max = options.option_brightness_max

    _event_handler = ChangeHandler()
    _observer = Observer()
    _observer.schedule(_event_handler, BASEDIR, recursive=True)
    _observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        _observer.stop()
    _observer.join()
