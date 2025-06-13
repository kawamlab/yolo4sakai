import pathlib
import cv2
import numpy as np

# 画像ディレクトリ
IMG_DIR = pathlib.Path(r"c:/Users/sone.NAKAZAWA23/programs/yolo4sakai/dataset_b/train")


# ファイル名からクラスIDを決定（例: BLB_ → 0, BLF_ → 1 など。必要に応じて修正）
def get_class_id(filename):
    if filename.startswith("BLB_"):
        return 1
    elif filename.startswith("BLF_"):
        return 0
    else:
        return 0  # デフォルト


# YOLO形式でアノテーションを書き出し
def write_yolo_annotation(txt_path, class_id, bbox, img_shape):
    h, w = img_shape[:2]
    x, y, bw, bh = bbox
    x_c = (x + bw / 2) / w
    y_c = (y + bh / 2) / h
    bw_n = bw / w
    bh_n = bh / h
    with open(txt_path, "w") as f:
        f.write(f"{class_id} {x_c:.6f} {y_c:.6f} {bw_n:.6f} {bh_n:.6f}\n")


# 青色検出してバウンディングボックス取得
def detect_blue_circle(img) -> None | tuple[int, int, int, int]:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 80, 80])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    return (x, y, w, h)


# メイン処理
def main():
    for img_path in IMG_DIR.glob("*.jpg"):
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        bbox = detect_blue_circle(img)
        if bbox is None:
            print(f"No blue circle found: {img_path.name}")
            continue
        class_id = get_class_id(img_path.name)
        # バウンディングボックスを画像に描画
        x, y, w, h = bbox
        img_draw = img.copy()
        cv2.rectangle(img_draw, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img_draw, f"class: {class_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Result", img_draw)
        print(
            f"YOLO: {class_id} {(x + w / 2) / img.shape[1]:.6f} {(y + h / 2) / img.shape[0]:.6f} {w / img.shape[1]:.6f} {h / img.shape[0]:.6f}"
        )
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # 保存はコメントアウト
        # txt_path = img_path.with_suffix(".txt")
        # write_yolo_annotation(txt_path, class_id, bbox, img.shape)
        print(f"Annotated: {img_path.name}")


if __name__ == "__main__":
    main()
