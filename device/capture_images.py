import pyrealsense2 as rs
from datetime import datetime
import numpy as np
import cv2
import os
from media_saver import MediaSaver
saver = MediaSaver(base_dir="data")

def save_image():
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

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            saver.save_image(color_image, prefix="color", ext="png")

    finally:
        # Stop streaming
        pipeline.stop()
