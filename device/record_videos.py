import json
import time
import cv2
import numpy as np
import pyrealsense2 as rs
from datetime import datetime
from pathlib import Path

output_dir = Path("data/videos")

WIDTH = 640
HEIGHT = 480
FPS = 15
DURATION_SEC = 60


def build_output_paths():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)

    record_dir = output_dir / f"record_{timestamp}"
    record_dir.mkdir(parents=True, exist_ok=True)

    video_path = record_dir / f"video_{timestamp}.mp4"
    video_json_path = record_dir / f"paramFile_{timestamp}.json"
    return video_path, video_json_path


def save_video():
    video_path, video_json_path = build_output_paths()

    ctx = rs.context()
    devs = list(ctx.query_devices())

    camera_Name = "default_Name"
    serial_Name = "default_Name"


    if len(devs) > 0:
        print("Devices: {}".format(devs))
        for dev in devs:
            camera_Name = dev.get_info(rs.camera_info.name)
            serial_Name = dev.get_info(rs.camera_info.serial_number)
            print(f"Device: {camera_Name} & SerialNo: {serial_Name}")
    else:
        raise RuntimeError(
            "No camera detected. Please connect a realsense camera and try again."
        )

    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(
        rs.stream.color,
        WIDTH,
        HEIGHT,
        rs.format.bgr8,
        FPS,
    )

    pipeline.start(config)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video_writer = cv2.VideoWriter(
        str(video_path),
        fourcc,
        FPS,
        (WIDTH, HEIGHT),
    )

    if not video_writer.isOpened():
        pipeline.stop()
        raise RuntimeError("视频文件创建失败，请检查输出路径或编码器")

    print(f"开始录像：{video_path}")
    start_time = time.monotonic()

    saved_frame_count = 0

    try:
        while True:
            elapsed = time.monotonic() - start_time
            if elapsed >= DURATION_SEC:
                break

            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            if not color_frame:
                continue

            # 当前这一帧图像，形状通常是 (480, 640, 3)
            color_image = np.asanyarray(color_frame.get_data())

            # 把当前帧写入视频
            video_writer.write(color_image)
            saved_frame_count += 1

    finally:
        video_writer.release()
        pipeline.stop()
        cv2.destroyAllWindows()

    actual_elapsed_sec = time.monotonic() - start_time
    effective_capture_fps = (
        saved_frame_count / actual_elapsed_sec if actual_elapsed_sec > 0 else 0.0
    )
    file_size_bytes = video_path.stat().st_size if video_path.exists() else 0

    data = {
        "camera_name": camera_Name,
        "serial_number": serial_Name,
        "width": WIDTH,
        "height": HEIGHT,
        "target_fps": FPS,
        "target_duration_sec": DURATION_SEC,
        "actual_elapsed_sec": actual_elapsed_sec,
        "saved_frame_count": saved_frame_count,
        "effective_capture_fps": effective_capture_fps,
        "output_file": str(video_path),
        "file_size_bytes": file_size_bytes,
        "status": "success",
    }

    with open(video_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"文件已成功保存至: {video_json_path}")

    print(f"录像完成：{video_path}")



