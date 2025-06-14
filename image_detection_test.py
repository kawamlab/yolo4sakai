import os
import pathlib
import sys

import cv2

from src.yolo_detector import YoloDetector, YoloModel

sys.modules["pathlib._local"] = pathlib
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath

if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve(strict=True).parent

    # YOLO Detectorの初期化
    detector = YoloDetector(model_type=YoloModel.BLUE, conf=0.55, iou=0.45)

    # 動画ファイルのパス
    video_path = str(root / "samples" / "blue.mp4")
    # camera = cv2.VideoCapture(video_path)
    end_count = 0
    frame_limit = 10

    while end_count < frame_limit:
        # YOLO推論（画像1枚ごと）
        results = detector.detect_on_image(0, show=True)

        print(f"検出された物体の個数: {len(results)}")
        for det in results:
            print(
                f"物体 {det.index}: クラス {det.label}, 信頼度 {det.confidence:.2f}, "
                f"座標 ({det.x1:.0f}, {det.y1:.0f}) - ({det.x2:.0f}, {det.y2:.0f})"
            )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
