import cv2

def plant_optimizer(img_path: str, max_dim: int = 1024) -> bytes:
    """Resizes and compresses the blueprint to save input tokens."""
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"The image could not be loaded: {img_path}")

    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / float(max(h, w))
        img = cv2.resize(
            img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA
        )

    # Convert to JPG with 80% quality.
    _, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    return buffer.tobytes()
