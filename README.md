# 部品振り分けプログラム

## 概要

本プログラムは、カメラで取得した画像をもとに部品を自動で判別し、GPIO制御によって部品の振り分けを行うシステムです。Raspberry Pi5で動作します。

## ソフトウエアの準備

以下のコマンドで、必要なツールやリポジトリをセットアップします。

```bash
# 1. Python仮想環境管理ツール「uv」のインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. テキストエディタ「micro」のインストール
cd /usr/bin/
curl https://getmic.ro | sudo bash

# 3. プログラム配置用ディレクトリの作成
mkdir programs
cd programs/

# 4. 本リポジトリのクローン
#   ※ 既存のprogramsディレクトリがある場合はcdのみでOK
git clone https://github.com/kawamlab/yolo4sakai
```

- `uv`はPython仮想環境の作成・パッケージ管理を高速化するツールです。
- `micro`は軽量なテキストエディタで、設定ファイルの編集に便利です。
- `programs`ディレクトリはユーザーの作業用ディレクトリです。
- `git clone`で本プログラム一式をダウンロードします。

## インストール方法

uvを使用できる環境を構築してください。

```bash
# 1. 仮想環境の作成
uv venv --system-site-packages .venv

# 2. 依存パッケージのインストール
uv pip install -r requirements.txt

# 3. シンボリックリンクの作成
sh src/create_symlink.sh
```

- `.venv`ディレクトリに仮想環境が作成されます。
- `requirements.txt`に記載されたPythonパッケージがインストールされます。
- `create_symlink.sh`は必要なリンクを自動で作成します。

## SDカードの長寿命化

Raspberry PiのSDカードの寿命を延ばすため、スワップや一時ファイルの無効化・削除を推奨します。以下の手順を参考にしてください。

```bash
# スワップを無効化
sudo swapon --show
sudo swapoff --all
free -h
sudo systemctl stop dphys-swapfile
sudo systemctl disable dphys-swapfile
systemctl status dphys-swapfile
sudo rm -f /var/swap
sudo reboot
```

```bash
# /etc/fstab からスワップや一時領域の自動マウントを削除
sudo nano /etc/fstab
```

```config
# 一番下に追記
tmpfs /tmp tmpfs defaults,size=64m,noatime,mode=1777 0 0
tmpfs /var/tmp tmpfs defaults,size=32m,noatime,mode=1777 0 0
```

```bash
# 一時ファイルの削除
sudo rm -rf /var/tmp
sudo rm -rf /tmp && sudo reboot
```

これらの設定により、SDカードへの書き込み回数を減らし、長寿命化が期待できます。

万が一、スワップや一時ファイルの削除後に問題が発生した場合は、以下のコマンドで元に戻すことができます。

```bash
# 再度有効化と容量アップ
sudo systemctl start dphys-swapfile
sudo systemctl enable dphys-swapfile
systemctl status dphys-swapfile

sudo nano /etc/dphys-swapfile
# CONF_SWAPSIZE=100を2048に変更。
```

```bash
# /etc/fstab からスワップや一時領域の自動マウントを削除
sudo nano /etc/fstab
```

```config
# 以下の行を削除
tmpfs /tmp tmpfs defaults,size=64m,noatime,mode=1777 0 0
tmpfs /var/tmp tmpfs defaults,size=32m,noatime,mode=1777 0 0
```

## 使い方

1. 必要なハードウェア（カメラ、GPIO制御用回路）を接続してください。
2. カメラが正しく認識されていることを確認してください。
3. プログラムを実行します。

```bash
sh src/run.sh
```

### ホスト名による動作切り替えについて

本プログラムは、実行時のホスト名によって動作内容を自動で切り替える設計になっています。

- 例えば `raspberrypi-1-black` で実行した場合は黒部品用、`raspberrypi-1-blue` で実行した場合は青部品用の処理が動作します。
- ホスト名の設定は `/etc/hostname` で確認・変更できます。
- 複数台で運用する場合は、各Raspberry Piのホスト名を用途に応じて設定してください。

## 動作モード

- 実行時にGUI（ディスプレイ）が利用可能な場合は、検出結果の画像表示が有効になります。
- GUIが利用できない場合は、画像表示なしで自動判別・振り分けのみ行います。

## ディレクトリ構成

- `src/` : カメラ制御や画像取得、メイン処理、各種スクリプト
- `gpio/` : GPIO制御用モジュール
- `models/` : 学習済みモデルや設定ファイル
- `data/` : 設定用データやサンプル画像
- `dataset_b/` : 学習用データセット
- `classify/` : 画像分類用スクリプト・ノートブック
- `segment/` : セグメンテーション用スクリプト・ノートブック
- `utils/` : 補助的なユーティリティ関数群
- `runs/` : 学習や推論の出力結果

## 注意事項

- GPIO制御には管理者権限が必要な場合があります。
- ハードウェアの接続ミスや誤動作にご注意ください。
- 本プログラムはRaspberry Pi5での動作を想定しています。他のモデルでは動作保証しません。
- モデルやデータセットの著作権・ライセンスにご注意ください。

## ライセンス

本プログラムはALL RIGHTS RESERVEDです。商用利用や再配布はご遠慮ください。

※ ただし、YOLO等の外部ライブラリ・モデルに関わる部分については、それぞれのライセンス条件に従ってご利用ください。

## センサ結線

モード切り換えスイッチは、Dに設定してください。

- 青線: GND
- 茶線: VCC(12V)
- レベル変換基盤から出ている長い線の結んでいない方: 12V
- レベル変換基盤から出ている長い線の結んでいる方: センサの黒線

詳細は[センサ仕様](https://www.fa.omron.co.jp/product/item/E3Z-T61_2M/ja/pdf/)の6ページ目を参照してください。
