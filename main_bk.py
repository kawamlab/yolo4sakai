import os
import pathlib
import sys
import time
from collections import Counter
from src.camera_capture_linuxpy import CameraCaptureLinuxpy
from gpio.valve import AutoFactory
from src.yolo_detector import YoloDetector, YoloModel

sys.modules["pathlib._local"] = pathlib
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath


def is_gui_available() -> bool:
    return os.environ.get("DISPLAY") is not None


if is_gui_available():
    show = True  # GUIが利用可能なら物体検出結果を表示する
else:
    print("GUI is not available. Disabling object detection display.")
    show = False  # GUIが利用できない場合は物体検出結果を表示しない

if __name__ == "__main__":
    af = AutoFactory()
    detector = YoloDetector(model_type=YoloModel.BLACK)

    # BKBなら通す
    through_direction = "BKB"  # TODO: fix

    af.cam.off()
    af.blower.off()

    camera = CameraCaptureLinuxpy(0)  # カメラ番号を指定

    try:
        while True:
            # パーツが検知エリアに入るまで待機
            time.sleep(0.2)  # TODO: 時間調整

            # 物体検出を実行
            # 物体検出をN回繰り返して確度を高める
            N = 1  # 検出回数
            CONF_THRESHOLD = 0.5  # 信頼度の閾値（例: 0.6）
            detection_results = []
            print("物体検出を実行中...")
            for i in range(N):
                results = []
                while not results:
                    img = camera.get_image()
                    if img is None:
                        print(f"画像取得失敗 ({i + 1}/{N}) 再取得します...")
                        time.sleep(0.5)
                        continue
                    results = detector.detect_on_image(img, show=show)
                    if not results:
                        print(f"No objects detected. ({i + 1}/{N}) 再検出します...")
                        time.sleep(0.5)

                # r.x1が500以上のものを除外
                results = [r for r in results if r.x1 < 500]

                # r.x2が100以下のものを除外
                results = [r for r in results if r.x2 > 100]

                # r.y1が100以上のものを除外
                results = [r for r in results if r.y1 < 100]

                # 信頼度が閾値以上のものだけ追加
                detection_results.extend([r for r in results if r.confidence >= CONF_THRESHOLD])
                time.sleep(0.2)  # 連続検出時の間隔

            # detection_resultsの全座標を出力
            for r in detection_results:
                print(f"検出ラベル: {r.label}, 信頼度: {r.confidence:.2f}, 座標: {r}")

            label_counter = Counter([r.label for r in detection_results])

            if not label_counter:
                print(f"{N}回検出しても信頼度{CONF_THRESHOLD}以上の物体が見つかりませんでした。")
                continue
            most_common_label, count = label_counter.most_common(1)[0]
            # 最頻ラベルの平均信頼度
            confidences = [r.confidence for r in detection_results if r.label == most_common_label]
            avg_conf = sum(confidences) / len(confidences)
            print(f"最頻ラベル: {most_common_label} (出現回数: {count}/{N}), 平均信頼度: {avg_conf:.2f}")

            # 最頻ラベルの最初のDetectionResultをpartとする
            part = next(r for r in detection_results if r.label == most_common_label)

            # パーツを通過させる
            print(f"物体 {part.label} を通過させます。")
            af.cam.on()

            # 物体が通過するまで待機
            # センサーが遮られるまで待機
            print("物体がセンサーを遮るのを待機中...")
            af.intr_sensor.wait_for_inactive()

            # カムをオフにする
            af.cam.off()

            if part.label != through_direction:
                print(f"物体 {part.label} が検出されました。弾きます。")
                time.sleep(0)  # TODO: 時間調整
                af.blowout(count=3)

            else:
                print(f"物体 {part.label} が検出されました。通過させます。")
                time.sleep(0)  # TODO: 時間調整

                # センサーが遮られた後、物体が通過するのを待機
                print("物体がセンサーを通過するのを待機中...")
                af.intr_sensor.wait_for_active()

    except KeyboardInterrupt:
        print("\nCtrl+Cが押されたため、処理を終了します。")
