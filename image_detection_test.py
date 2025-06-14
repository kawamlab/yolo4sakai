import io
import os
import pathlib
import sys

import cv2
import imageio.v2 as imageio
from linuxpy.video.device import BufferType, Device, VideoCapture

from src.yolo_detector import YoloDetector, YoloModel

sys.modules["pathlib._local"] = pathlib
if os.name == "nt":
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath

if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve(strict=True).parent

    # YOLO Detectorの初期化
    detector = YoloDetector(model_type=YoloModel.BLUE_NEW, conf=0.55, iou=0.45)

    # 動画ファイルのパス
    video_path = str(root / "samples" / "blue.mp4")
    # camera = cv2.VideoCapture(video_path)
    end_count = 0
    frame_limit = 10

    while end_count < frame_limit:
        # YOLO推論（画像1枚ごと）

        with Device.from_id(0) as cam:
            # cam.set_format(width=640, height=480, buffer_type=BufferType.VIDEO_CAPTURE, pixel_format="MJPG")

            capture = VideoCapture(cam)
            capture.set_format(width=640, height=480)

            with capture:
                for frame in capture:
                    img = None
                    try:
                        img = imageio.imread(io.BytesIO(frame.data))
                        print(f"フレーム取得: {frame.frame_nb}, サイズ: {len(frame.data)} バイト")
                    except BaseException as e:
                        print(f"Error reading frame: {e}")
                        continue

                    break

        if img is None:
            print("No image data found, skipping frame.")
            end_count += 1
            continue

        print(f"取得した画像の形状: {img.shape}")

        # 色をBGRからRGBに変換
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        print(f"フレーム取得: {frame.frame_nb}, サイズ: {len(frame.data)} バイト")

        results = detector.detect_on_image(img, show=True)

        print(f"検出された物体の個数: {len(results)}")
        for det in results:
            print(
                f"物体 {det.index}: クラス {det.label}, 信頼度 {det.confidence:.2f}, "
                f"座標 ({det.x1:.0f}, {det.y1:.0f}) - ({det.x2:.0f}, {det.y2:.0f})"
            )

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
