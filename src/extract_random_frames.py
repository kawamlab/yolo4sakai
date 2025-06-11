import os
import pathlib
import random

import cv2

VIDEO_PATH = pathlib.Path(__file__).resolve(strict=True).parent.parent / "samples" / "blue.mp4"
# 色名を動画ファイル名から取得（拡張子除去）
color_name = VIDEO_PATH.stem
OUTPUT_DIR = pathlib.Path(__file__).resolve(strict=True).parent.parent / "samples" / "output_frames" / color_name
NUM_FRAMES = 10


def extract_random_frames(video_path: str, output_dir: str, num_frames: int = 50) -> None:
    # 出力ディレクトリを作成し、既存ファイルを全削除
    os.makedirs(output_dir, exist_ok=True)
    for f in os.listdir(output_dir):
        file_path = os.path.join(output_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"動画ファイルが開けません: {video_path}")
        return
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames < num_frames:
        print(f"動画のフレーム数({total_frames})が抽出数({num_frames})より少ないです")
        num_frames = total_frames
    frame_indices = sorted(random.sample(range(total_frames), num_frames))
    idx_set = set(frame_indices)
    saved = 0
    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        if i in idx_set:
            filename = os.path.join(output_dir, f"frame_{saved + 1:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1
            if saved >= num_frames:
                break
    cap.release()
    print(f"{saved}枚のフレームを{output_dir}に保存しました")


if __name__ == "__main__":
    extract_random_frames(str(VIDEO_PATH), str(OUTPUT_DIR), NUM_FRAMES)
