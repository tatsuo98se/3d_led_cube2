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


### led_framework.py - pythonプログラム用、Json表示命令受信クラス

実装例

``` example.py
from led_framework import LedFramework

LedFramework().show({"orders":[{"id":"object-fill"},{"id":"object-cube"}]})

```
