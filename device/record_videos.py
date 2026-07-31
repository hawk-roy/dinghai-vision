import cv2
import numpy as np
import pyrealsense2 as rs
from datetime import datetime
from pathlib import Path

output_dir = Path("data/videos")
output_dir.mkdir(parents=True, exist_ok=True)

video_path = output_dir / (
    datetime.now().strftime("color_%Y%m%d_%H%M%S") + ".mp4"
)

WIDTH = 640
HEIGHT = 480
FPS = 15


def save_video():
    ctx = rs.context()
    devs = list(ctx.query_devices())

    if len(devs) > 0:
        print("Devices: {}".format(devs))
        for dev in devs:
            name = dev.get_info(rs.camera_info.name)
            serial = dev.get_info(rs.camera_info.serial_number)
            print(f"Device: {name} & SerialNo: {serial}")
    else:
        print("No camera detected. Please connect a realsense camera and try again.")
        exit(0)

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
    print("按 q 停止录像")

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            if not color_frame:
                continue

            # 当前这一帧图像，形状通常是 (480, 640, 3)
            color_image = np.asanyarray(color_frame.get_data())

            # 把当前帧写入视频
            video_writer.write(color_image)

            # 实时预览
            cv2.imshow("RealSense Color", color_image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        video_writer.release()
        pipeline.stop()
        cv2.destroyAllWindows()

    print(f"录像完成：{video_path}")



