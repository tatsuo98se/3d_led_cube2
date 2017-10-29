## Requirements

Python 2.7  
pip install pillow  
pip install numpy  
pip install flask  

### for macOS

brew install opencv  
brew install boost  

## Tested with

macOS

## 各ファイルの役割

### main_server.py

以下の2つの役割がある

#### 1. JSON表示命令の受取

受け取った命令をLED CUBEとシミュレータに表示する。
表示に成功した命令は、./log/order_history以下にログとして保存する


#### 2. 表示済みのコンテンツのJSON表示命令ファイルの配信

./log/order_history以下のファイルを、HTTPで公開する。
例えば、上記ディレクトリ以下に"2.log"というファイルがあった場合、以下のURLから上記ファイルが取得できる

http://(IP):5000/api/content/2

### main_client.py  - 生徒PC用のシュミレーションスクリプト

任意の固定のURLからJsonの表示命令を取得し、シミュレーターに表示する
Enterキーの入力で、再度Jsonの表示命令の取得を行う

### main_notcp.py - 標準入力から命令を受信して表示するスクリプト

ローカル環境確認用  
コンソールへの以下の入力で、HTTP経由での命令と等価の動作となる

| HTTPでの表示命令 | main_notcp.pyでのコンソールへの表示命令入力 |
| ---------------- | ----------------------- |
| HTTP POST<br/>http://(サーバーのIP)/api/show<br/>コンテンツ: (JSON表示命令) | show:{(JSON表示命令)} |
| HTTP POST<br/>http://(サーバーのIP)/api/abort | abort |


### led_framework.py - pythonプログラム用、Json表示命令受信クラス

実装例

``` example.py
from led_framework import LedFramework

LedFramework().show({"orders":[{"id":"object-fill"},{"id":"object-cube"}]})

```

# for led_coloring

## Requirements

pip install watchdog
pip install opencv

ImageMagick-7.0.7-8-portable
https://www.imagemagick.org/script/download.php
パスを設定する。Windowsのパス設定は「コントロールパネル→システム→システムの詳細設定→環境変数(N)

## 各ファイルの役割

### for led_coloring - スキャン文書から塗り絵を読み込み表示するアプリケーション
+ 対象フォーマット
 .jpg, .jpeg .png, .tif(single) .tif(multi)
+ スキャン解像度
 200dpi
+ スキャン入稿フォルダ
./asset/coloring/scan_in/
+ 塗り絵フォーム
./asset/coloring/3dledcube_form.xlsx


#### 基本的なつかい方
塗り絵フォームを印刷して塗り絵をする.
スキャンしてファイルを保存する.
スキャン文書をスキャン入稿フォルダに格納する

#### 複合機連携
塗り絵フォームを印刷して塗り絵をする.
スキャン入稿フォルダを共有フォルダ(SMB|FTP)設定する.
複合機のスキャン文書の転送先で上記共有フォルダを設定する.
塗り絵をスキャンする.

