import pathlib
import time

import cv2
import torch

if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve(strict=True).parent

    # --- 検出する際のモデルを読込 ---
    model = torch.hub.load(
        "./",
        "custom",
        # path=str(root / "models" / "BKweights_epoch_150.pt"),
        path=str(root / "models" / "BLweights_epoch_150.pt"),
        source="local",
        # force_reload=True,
    )

    # --- 検出の設定 ---
    model.conf = 0.55  # --- 検出の下限値（<1）。設定しなければすべて検出
    model.iou = 0.45  # --- 検出の下限値（<1）。設定しなければすべて検出

    # --- 映像の読込元指定 ---
    # --- localの動画ファイルを指定
    camera = cv2.VideoCapture(
        str(root / "samples" / "blue.mp4")  # --- 動画ファイルのパスを指定
    )
    # --- カメラ：Ch.(ここでは0)を指定
    # camera = cv2.VideoCapture(0)

    # --- 画像のこの位置より左で検出したら、ヒットとするヒットエリアのためのパラメータ ---

    # camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    # camera.set(cv2.CAP_PROP_EXPOSURE, 750)

    while True:
        ret, imgs = camera.read()

        now = time.time()
        results = model(imgs, size=640)  # --- 160ピクセルの画像にして処理
        print(time.time() - now)

        results.render()
        cv2.imshow("color", results.ims[0])
        result = results.xyxy[0]  # --- pandasで出力
        print(result)
        # time.sleep(0.001)
        # cv2.waitKey(25)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
