import pathlib
from enum import Enum
from typing import Optional, Union

import cv2
import torch


class YoloModel(Enum):
    BLACK = "BKweights_epoch_150.pt"
    BLUE = "BLweights_epoch_200.pt"


class YoloDetector:
    def __init__(self, model_type: YoloModel = YoloModel.BLACK, conf: float = 0.55, iou: float = 0.45) -> None:
        """
        YOLOモデルの初期化
        model_type: YoloModel Enum（BLACK or BLUE）
        conf, iou: 検出閾値
        """
        root: pathlib.Path = pathlib.Path(__file__).resolve(strict=True).parent.parent
        self.root: pathlib.Path = root
        print(f"loading model: {model_type.value}")
        self.model = torch.hub.load(
            str(root),
            "custom",
            path=str(root / "models" / model_type.value),
            source="local",
            autoshape=True,  # AutoShapeラッパーを有効化
        )
        self.conf = conf
        self.iou = iou

    def run(self, video_source: Union[str, int], frame_limit: int = 10, show_window: bool = True) -> None:
        """
        YOLO推論を実行するメソッド
        video_source: 動画ファイルパスまたはカメラ番号
        frame_limit: 最大フレーム数
        show_window: 画像ウィンドウ表示有無
        """
        camera: cv2.VideoCapture = cv2.VideoCapture(video_source)
        end_count: int = 0
        while end_count < frame_limit:
            ret: bool
            imgs: Optional[any]
            ret, imgs = camera.read()
            if ret is False:
                print("No frame")
                end_count += 1
                continue
            if callable(self.model):
                results = self.model(imgs, size=640, conf=self.conf, iou=self.iou)
            else:
                print("モデルが呼び出し可能ではありません")
                break
            if hasattr(results, "render"):
                results.render()
            if show_window and hasattr(results, "ims"):
                cv2.imshow("color", results.ims[0])
            result = getattr(results, "xyxy", [None])[0]
            names = getattr(results, "names", {})
            if result is not None:
                num_objects: int = result.shape[0]
                print(f"検出された物体の個数: {num_objects}")
                if num_objects > 0:
                    for i in range(num_objects):
                        x1, y1, x2, y2, conf, _cls = result[i]
                        label = names.get(int(_cls), f"Class {int(_cls)}")
                        print(
                            f"物体 {i + 1}: クラス {label}, 信頼度 {conf:.2f}, 座標 ({x1:.0f}, {y1:.0f}) - ({x2:.0f}, {y2:.0f})"
                        )
            if show_window and cv2.waitKey(1) & 0xFF == ord("q"):
                break
        camera.release()
        if show_window:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve(strict=True).parent.parent
    video_path = str(root / "samples" / "black.mp4")
    detector = YoloDetector(model_type=YoloModel.BLACK)
    detector.run(video_path)

# 他ファイルからの利用例:
# from src.yolo_detector import YoloDetector, YoloModel
# detector = YoloDetector(model_type=YoloModel.BLUE)
# detector.run(0)
