import linuxpy.video
import numpy as np
import cv2

# カメラデバイスを開く
with linuxpy.video.Device("/dev/video0") as cam:
    cam.set_format(640, 480, fourcc="MJPG")
    cam.request_buffers(1)
    cam.queue_all_buffers()
    cam.start()
    print("Press 'q' to quit.")
    while True:
        buf = cam.dequeue()
        frame = np.frombuffer(buf.data, dtype=np.uint8)
        img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        if img is not None:
            cv2.imshow("Camera", img)
        cam.queue_buffer(buf)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.stop()
cv2.destroyAllWindows()
