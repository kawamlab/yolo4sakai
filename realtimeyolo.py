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
        path=str(root / "models" / "BKweights_epoch_150.pt"),
        # path=str(root / "models" / "BLweights_epoch_150.pt"),
        source="local",
        # force_reload=True,
    )

    # --- 検出の設定 ---
    model.conf = 0.55  # --- 検出の下限値（<1）。設定しなければすべて検出
    model.iou = 0.45  # --- 検出の下限値（<1）。設定しなければすべて検出

    # --- 映像の読込元指定 ---
    # --- localの動画ファイルを指定
    camera = cv2.VideoCapture(
        str(root / "samples" / "black.mp4")  # --- 動画ファイルのパスを指定
    )
    # --- カメラ：Ch.(ここでは0)を指定
    # camera = cv2.VideoCapture(0)

    # --- 画像のこの位置より左で検出したら、ヒットとするヒットエリアのためのパラメータ ---

    # camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    # camera.set(cv2.CAP_PROP_EXPOSURE, 750)

    end_count = 0

    while end_count < 10:  # --- 1000フレームで終了
        ret, imgs = camera.read()

        if ret is False:
            print("No frame")
            end_count += 1
            continue

        results = model(imgs, size=640)  # --- 160ピクセルの画像にして処理

        results.render()
        cv2.imshow("color", results.ims[0])
        result = results.xyxy[0]

        names = results.names

        num_objects = result.shape[0]
        print(f"検出された物体の個数: {num_objects}")
        if num_objects > 0:
            for i in range(num_objects):
                x1, y1, x2, y2, conf, _cls = result[i]
                label = names.get(int(_cls), f"Class {int(_cls)}")
                print(
                    f"物体 {i + 1}: クラス {label}, 信頼度 {conf:.2f}, 座標 ({x1:.0f}, {y1:.0f}) - ({x2:.0f}, {y2:.0f})"
                )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
