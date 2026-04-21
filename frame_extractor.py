import cv2
import os


def get_smart_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    cap.release()

    if duration < 300:
        return 4        # Under 5 mins → 4fps
    elif duration < 600:
        return 2        # Under 10 mins → 2fps
    else:
        return 1        # Long video → 1fps


def extract_frames(video_path, output_dir="frames"):
    os.makedirs(output_dir, exist_ok=True)
    fps = get_smart_fps(video_path)

    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(video_fps / fps))

    frame_count = 0
    saved_count = 0
    frame_paths = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            path = os.path.join(output_dir, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(path, frame)
            frame_paths.append(path)
            saved_count += 1
        frame_count += 1

    cap.release()
    print(f"   Extracted {len(frame_paths)} frames at {fps}fps")
    return frame_paths
