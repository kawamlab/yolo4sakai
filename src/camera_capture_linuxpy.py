import io
import pathlib
import subprocess

import cv2
import imageio.v2 as imageio
from linuxpy.video.device import Device, VideoCapture


class CameraCaptureLinuxpy:
    def __init__(self, cam_id: int):
        """
        初期化時にsrc/set-camera.shを実行し、カメラ番号を保存
        """
        # set-camera.shの実行
        script_path = pathlib.Path(__file__).resolve().parent.parent / "src" / "set-camera.sh"
        subprocess.run(["bash", str(script_path)])
        print("Camera settings applied from set-camera.sh")
        self.cam_id = cam_id

    def get_image(self):
        """
        linuxpyを使い、指定カメラ番号から最新の1枚をRGB画像(numpy.ndarray)で返す。
        取得できない場合はNoneを返す。
        """
        img = None
        with Device.from_id(self.cam_id) as cam:
            capture = VideoCapture(cam)
            capture.set_format(width=640, height=480)
            with capture:
                for frame in capture:
                    try:
                        img = imageio.imread(io.BytesIO(frame.data))
                        brightness = cv2.mean(img)[0]
                        if brightness < 50:
                            continue
                    except BaseException as e:
                        print(f"Error reading frame: {e}")
                        continue
                    break
        if img is None:
            return None
        # imageioは通常RGBだが、念のためBGR→RGB変換
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
