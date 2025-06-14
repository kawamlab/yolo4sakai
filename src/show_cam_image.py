import io
import imageio.v2 as imageio
import cv2
from linuxpy.video.device import Device, BufferType, Capability, VideoCapture, Memory, FrameReader

with Device.from_id(2) as cam:
    # cam.set_format(width=640, height=480, buffer_type=BufferType.VIDEO_CAPTURE, pixel_format="MJPG")

    capture = FrameReader(cam, raw_read=True)
    capture.set_format(width=640, height=480)

    with capture:
        for frame in capture:
            try:
                img = imageio.imread(io.BytesIO(frame.data))

            except BaseException as e:
                print(f"Error reading frame: {e}")
                continue
            # 色をBGRからRGBに変換
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imshow("Camera", img)
            if cv2.waitKey(1) == 27:
                break
    cv2.destroyAllWindows()
    capture.close()
