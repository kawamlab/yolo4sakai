# 環境構築方法

## microのインストール

```bash
sudo apt update
sudo apt upgrade -y
cd /usr/bin
curl https://getmic.ro/r | sudo sh
```

## uvのインストール

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## directoryの作成

```bash
mkdir -p ~/programs
git clone https://github.com/kawamlab/yolo4sakai.git
cd ~/programs/yolo4sakai
```

## 仮想環境の作成

```bash
uv venv --system-site-packages
```

## 必要なパッケージのインストール

```bash
uv pip install -r requirements.txt
```

## 実行

```bash
uv run main.py
```