#!/bin/bash
# ダブルクリックで起動したら、~/programs/yolo4sakai ディレクトリに移動し、ホスト名で分岐してuv run main_bl.py または main_bk.py を実行
cd ~/programs/yolo4sakai

HOSTNAME=$(hostname)
if [[ "$HOSTNAME" == *blue* ]]; then
    uv run main_bl.py
elif [[ "$HOSTNAME" == *black* ]]; then
    uv run main_bk.py
else
    echo "ホスト名に 'blue' も 'black' も含まれていません: $HOSTNAME"
    exit 1
fi
