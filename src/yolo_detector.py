import pathlib
from enum import Enum
from typing import Union

import cv2
import numpy as np
import torch
from pydantic import BaseModel


class YoloModel(Enum):
    BLACK = "BKweights_epoch_150.pt"
    BLUE = "BLweights_epoch_200.pt"


class DetectionResult(BaseModel):
    index: int
    label: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


class YoloDetector:
    def __init__(self, model_type: YoloModel, conf: float = 0.55, iou: float = 0.45) -> None:
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

    def detect_on_video(self, video_source: Union[str, int], frame_limit: int = 3, show: bool = True) -> None:
        """
        動画またはカメラ入力に対してYOLO推論を実行する
        video_source: 動画ファイルパスまたはカメラ番号
        frame_limit: 最大フレーム数
        show_window: 画像ウィンドウ表示有無
        """
        camera: cv2.VideoCapture = cv2.VideoCapture(video_source)
        end_count: int = 0
        while end_count < frame_limit:
            ret: bool
            ret, imgs = camera.read()
            if ret is False:
                print("No frame")
                end_count += 1
                continue
            if callable(self.model):
                results = self.model(imgs, size=640)
            else:
                print("モデルが呼び出し可能ではありません")
                break
            if show:
                if hasattr(results, "render"):
                    results.render()  # type: ignore
                if hasattr(results, "ims"):
                    cv2.imshow("color", results.ims[0])  # type: ignore
            result = getattr(results, "xyxy", [None])[0]
            names = getattr(results, "names", {})
            if result is not None:
                filtered = []
                for row in result:
                    x1, y1, x2, y2, conf, _cls = row[:6]
                    if conf < self.conf:
                        continue
                    filtered.append(row)
                num_objects: int = len(filtered)
                print(f"検出された物体の個数: {num_objects}")
                if num_objects > 0:
                    for i, row in enumerate(filtered):
                        x1, y1, x2, y2, conf, _cls = row[:6]
                        label = names.get(int(_cls), f"Class {int(_cls)}")
                        print(
                            f"物体 {i + 1}: クラス {label}, 信頼度 {conf:.2f}, 座標 ({x1:.0f}, {y1:.0f}) - ({x2:.0f}, {y2:.0f})"
                        )
            if show and cv2.waitKey(1) & 0xFF == ord("q"):
                break
        camera.release()
        if show:
            cv2.destroyAllWindows()

    def detect_on_image(self, image: Union[str, np.ndarray, int], show: bool = False) -> list[DetectionResult]:
        """
        画像ファイルパス、ndarray、またはカメラ番号(int)を入力してYOLO推論を実行し、confでフィルタ済みのDetectionResultリストを返す
        show: Trueの場合は推論画像をウィンドウ表示（ウィンドウは閉じない）
        戻り値: List[DetectionResult]
        """
        img = None
        cap = None
        if isinstance(image, str):
            img = cv2.imread(image)
            if img is None:
                print(f"画像ファイルが開けません: {image}")
                return []
        elif isinstance(image, np.ndarray):
            img = image
        elif isinstance(image, int):
            cap = cv2.VideoCapture(image)
            ret, img = cap.read()
            cap.release()
            if not ret or img is None:
                print(f"カメラから画像を取得できません: {image}")
                return []
        else:
            print("入力はファイルパス、ndarray、またはカメラ番号(int)で指定してください")
            return []
        if callable(self.model):
            results = self.model(img, size=640)
        else:
            print("モデルが呼び出し可能ではありません")
            return []
        if show:
            if hasattr(results, "render"):
                results.render()  # type: ignore
            if hasattr(results, "ims"):
                cv2.imshow("detect_on_image", results.ims[0])  # type: ignore
                cv2.waitKey(1)  # ウィンドウは閉じない
        result = getattr(results, "xyxy", [None])[0]
        names = getattr(results, "names", {})
        detection_results: list[DetectionResult] = []
        if result is not None:
            for i, row in enumerate(result):
                x1, y1, x2, y2, conf, _cls = row[:6]
                if conf < self.conf:
                    continue
                label = names.get(int(_cls), f"Class {int(_cls)}")
                detection_results.append(
                    DetectionResult(
                        index=i + 1,
                        label=label,
                        confidence=float(conf),
                        x1=float(x1),
                        y1=float(y1),
                        x2=float(x2),
                        y2=float(y2),
                    )
                )
        return detection_results


if __name__ == "__main__":
    detector = YoloDetector(model_type=YoloModel.BLACK)

    # root = pathlib.Path(__file__).resolve(strict=True).parent.parent
    # images_dir = root / "samples" / "output_frames" / "black"

    # for image_file in images_dir.glob("*.jpg"):
    #     image_path = image_file
    #     print(f"Testing image: {image_path.stem}")

    #     results = detector.detect_on_image(str(image_path), show=False)
    #     for result in results:
    #         print(
    #             f"物体 {result.index}: クラス {result.label}, 信頼度 {result.confidence:.2f}, "
    #             f"座標 ({result.x1:.0f}, {result.y1:.0f}) - ({result.x2:.0f}, {result.y2:.0f})"
    #         )

    while True:
        # カメラからの画像を取得して検出
        results = detector.detect_on_image(0, show=True)
        if not results:
            print("No objects detected.")
            continue
        for result in results:
            print(
                f"物体 {result.index}: クラス {result.label}, 信頼度 {result.confidence:.2f}, "
                f"座標 ({result.x1:.0f}, {result.y1:.0f}) - ({result.x2:.0f}, {result.y2:.0f})"
            )


# 他ファイルからの利用例:
# from src.yolo_detector import YoloDetector, YoloModel
# detector = YoloDetector(model_type=YoloModel.BLUE)
# detector.run(0)
