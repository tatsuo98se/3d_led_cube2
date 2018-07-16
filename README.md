## Requirements

Python 2.7  
pip install pillow  
pip install numpy  
pip install flask  
pip install opencv-python  
pip install pyzmq  
pip install pyserial  
pip install pyaudio  
[Optional] pip install pyrealsense  

### for macOS

brew install opencv  
brew install boost  
brew install portaudio  
> pyaudioをインストールする前にportaudioを導入してください。

## Tested with

macOS

## 各ファイルの役割

### ファイル名の命名規則

#### "main_"から始まるもの

呼び出しのエントリーポイントとなるファイル

### "main_*_service.py"

このファイルの呼び出しで、一つのLEDのアトラクションを提供するもの

### "main_*_module.py"

"_service.py"を補助するために必要なサービス  
利用するには、このファイルも実行する必要がある

### "main_*_test.py", "main_*_sample"

テストを実行するためのエントリーポイント

### main_block_service.py

受け取ったブロックの組み合わせを表すのJson命令をLED CUBEとシミュレータに表示する。   
表示に成功した命令は、./log/order_history以下にログとして保存する

### main_paint_service.py

お絵かきコンテンツを実行する  
ポート5301にお絵かきのWebUIを表示する

### main_realsense_service.py

人影のコンテンツを実行する  
main_realsense_module.pyの実行も必要  


### main_block_test.py - 標準入力からブロックの組み合わせを表すのJson命令を受信して表示するスクリプト

ローカル環境確認用  
コンソールへの以下の入力で、HTTP経由での命令と等価の動作となる

| HTTPでの表示命令 | main_block_test.pyでのコンソールへの表示命令入力 |
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
./asset/coloring/scan_in2/
+ 塗り絵フォーム
./asset/coloring/3dledcube_form.xlsx


#### つかい方（複合機連携なし）
塗り絵フォームを印刷して塗り絵をする.
スキャンしてファイルを保存する.
スキャン文書をスキャン入稿フォルダに格納する

#### つかい方（複合機連携あり）
「複合機連携セットアップ手順(後述)」に従い設定する.
塗り絵フォームを印刷して塗り絵をする.
複合機でスキャナー（ネットワーク）から登録した宛先を選択する.
塗り絵をスキャンする.

### 複合機連携セットアップ手順
+ スキャン入稿フォルダの公開  
PCでスキャン入稿フォルダを共有フォルダ設定する.  
Everyoneに読み書き権限を付与する.    
PCのIPアドレスを確認する.
+ 複合機の宛先表登録（DocuPrint CM310/210z)
複合機とLANケーブルを接続した状態で電源ON.  
IPアドレスをDHCPにして再起動し、IPアドレスを確認.  
PCのブラウザからCWISでアクセスする.  
[宛先表＞サーバーアドレス]を押下後、[新規登録]を選択.  
[サーバーアドレスの登録]で宛先を登録する.  
　名前:任意   
　サーバータイプ:SMB  
　サーバーアドレス：192.168.100.xxx  
　ポート：139  
　ログイン名：（空）  
　パスワード：（空）  
　共有名：scan_in  
　サーバーパス：（空） 
+ スキャン設定(デフォルト)の設定  
以下を設定する.    
　解像度：200dpi  
　カラーモード：カラー   
　画像フォーマット：TIFF   
　フォルダ作成：ON   
+ DocuPrint CM210 z の場合の追加手順
./asset/coloring/MoveTiffFile.cmdを実行する  
  -> scan_inに格納されたTiff画像を、scan_in2へ移動する

以上