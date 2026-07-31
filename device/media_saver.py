import os
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np


class MediaSaver:
    """专为树莓派相机/RealSense 设计的媒体文件保存器"""

    def __init__(self, base_dir="data"):
        # 默认保存在当前目录下的 output_data，也可以改为绝对路径如 "~/fish-monitor/data"
        self.base_dir = Path(base_dir).expanduser().resolve()

    def _ensure_dir(self, dir_path: Path):
        """确保目标文件夹存在"""
        dir_path.mkdir(parents=True, exist_ok=True)

    def _get_timestamp(self) -> str:
        """生成与你原逻辑一致的时间戳"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_image(self, image_array: np.ndarray, sub_dir="", prefix="color", ext="png") -> str:
        """
        保存图片（针对 OpenCV / NumPy 数组）
        :param image_array: 传入的 color_image 数组
        :param sub_dir: 子文件夹，默认为空（直接存放在 output_data 下）
        :param prefix: 文件名前缀，如 "color"
        :param ext: 文件后缀，你的原逻辑是 "png"
        """
        # 1. 确定最终文件夹路径
        target_dir = self.base_dir / sub_dir if sub_dir else self.base_dir
        self._ensure_dir(target_dir)

        # 2. 生成文件名：例如 color_20260731_142230.png
        filename = f"{prefix}_{self._get_timestamp()}.{ext.lstrip('.')}"
        full_path = target_dir / filename

        # 3. 使用 OpenCV 保存 NumPy 数组（核心替换原逻辑）
        # cv2.imwrite 需要字符串路径，所以用 str(full_path)
        success = cv2.imwrite(str(full_path), image_array)

        if success:
            print(f"[INFO] 图片已成功保存至: {full_path}")
            return str(full_path)
        else:
            print(f"[ERROR] 图片保存失败: {full_path}")
            return ""

