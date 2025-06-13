import os
import pathlib
import sys
import time
from collections import Counter

from gpio.valve import AutoFactory
from src.yolo_detector import YoloDetector, YoloModel

sys.modules["pathlib._local"] = pathlib
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath

show = True  # 物体検出結果を表示するかどうか

if __name__ == "__main__":
    af = AutoFactory()
    detector = YoloDetector(model_type=YoloModel.BLACK)

    # BKBなら通す
    through_direction = "BKB"  # TODO: fix

    af.cam.off()
    af.blower.off()

    while True:
        # パーツを検知エリアに配置
        af.cam.on()
        time.sleep(3)  # TODO: fix
        print("カムを引き、パーツを検知エリアに配置しました。")

        # 物体検出を実行
        # 物体検出をN回繰り返して確度を高める
        N = 3  # 検出回数
        CONF_THRESHOLD = 0.6  # 信頼度の閾値（例: 0.6）
        detection_results = []
        print("物体検出を実行中...")
        for i in range(N):
            results = []
            while not results:
                results = detector.detect_on_image(0, show=show)
                if not results:
                    print(f"No objects detected. ({i + 1}/{N}) 再検出します...")
                    time.sleep(0.5)
            # 信頼度が閾値以上のものだけ追加
            detection_results.extend([r for r in results if r.confidence >= CONF_THRESHOLD])
            time.sleep(0.2)  # 連続検出時の間隔

        label_counter = Counter([r.label for r in detection_results])
        if not label_counter:
            print(f"N回検出しても信頼度{CONF_THRESHOLD}以上の物体が見つかりませんでした。")
            continue
        most_common_label, count = label_counter.most_common(1)[0]
        # 最頻ラベルの平均信頼度
        confidences = [r.confidence for r in detection_results if r.label == most_common_label]
        avg_conf = sum(confidences) / len(confidences)
        print(f"最頻ラベル: {most_common_label} (出現回数: {count}/{N}), 平均信頼度: {avg_conf:.2f}")

        # 最頻ラベルの最初のDetectionResultをpartとする
        part = next(r for r in detection_results if r.label == most_common_label)

        # パーツを通過させる
        af.cam.off()

        if part.label != through_direction:
            print(f"物体 {part.label} が検出されました。弾きます。")
            time.sleep(1)  # TODO: fix
            af.blowout()

        else:
            print(f"物体 {part.label} が検出されました。通過させます。")
            time.sleep(3)  # TODO: fix

    # # read from camera
    # while True:
    #     results = detector.detect_on_image(0, show=True)
    #     for result in results:
    #         print(
    #             f"物体 {result.index}: クラス {result.label}, 信頼度 {result.confidence:.2f}, "
    #             f"座標 ({result.x1:.0f}, {result.y1:.0f}) - ({result.x2:.0f}, {result.y2:.0f})"
    #         )
