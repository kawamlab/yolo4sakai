import pathlib
import time

from gpio.valve import AutoFactory
from src.yolo_detector import DetectionResult, YoloDetector, YoloModel

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
        print("物体検出を実行中...")
        results = []
        while not results:
            results = detector.detect_on_image(0, show=True)
            if not results:
                print("No objects detected. 再検出します...")
                time.sleep(0.5)

        for result in results:
            print(
                f"物体 {result.index}: クラス {result.label}, 信頼度 {result.confidence:.2f}, "
                f"座標 ({result.x1:.0f}, {result.y1:.0f}) - ({result.x2:.0f}, {result.y2:.0f})"
            )

        # 物体検出結果の最初のものを使用(ここは必要に応じて変更)
        part = results[0]

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
