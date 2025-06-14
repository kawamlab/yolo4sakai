import uvc
import numpy as np
import cv2

# UVC対応カメラ一覧を取得
dev_list = uvc.device_list()
print(f"UVC対応カメラ一覧: {dev_list}")
if not dev_list:
    print("UVC対応カメラが見つかりません")
    exit(1)
cap = uvc.Capture(dev_list[0]["uid"])  # 1台目を使用

# 解像度を設定（例：640x480）
cap.frame_mode = cap.frame_modes[0]

# 設定（固定露出・ゲインなど）
cap.exposure_auto = False
cap.exposure_abs = 750
cap.white_balance_auto = False
cap.white_balance_temperature = 4600
cap.gain = 0

# プレビュー表示
while True:
    frame = cap.get_frame_robust()  # タイムアウト付きで安全に取得
    img = frame.img  # numpy.ndarray (H, W, 3), dtype=uint8
    cv2.imshow("Camera via pyuvc", img)
    if cv2.waitKey(1) == 27:  # ESCキーで終了
        break

cap.close()
cv2.destroyAllWindows()
