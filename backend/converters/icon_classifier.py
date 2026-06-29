"""Classify EWA report icon images for compact HTML conversion."""

from __future__ import annotations

import logging
import os
import re
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)

_BAR_HORIZ_SIZE = (32, 15)
_BAR_VERT_WIDTH = 41
_MIN_COLOR_PIXELS = 5


def _avg_color(image_path: str) -> tuple[Optional[tuple[int, int, int]], int, int]:
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as exc:
        logger.warning("Cannot open image %s: %s", image_path, exc)
        return None, 0, 0

    color_pixels = []
    for red, green, blue, alpha in img.getdata():
        if alpha < 50:
            continue
        if red > 240 and green > 240 and blue > 240:
            continue
        color_pixels.append((red, green, blue))

    if len(color_pixels) < _MIN_COLOR_PIXELS:
        return None, img.width, img.height

    count = len(color_pixels)
    avg_red = sum(red for red, _, _ in color_pixels) // count
    avg_green = sum(green for _, green, _ in color_pixels) // count
    avg_blue = sum(blue for _, _, blue in color_pixels) // count
    return (avg_red, avg_green, avg_blue), img.width, img.height


def _label_from_rgb(red: int, green: int, blue: int) -> str:
    if red < 20 and green < 20 and blue < 20:
        return "[NOT_RATED]"
    if red > green + 40 and red > blue + 40:
        return "[RED]"
    if blue > red + 30 and blue > green + 30:
        return "[BLUE]"
    if red > 100 and green > 80 and blue < 80:
        return "[YELLOW]"
    if green > red + 15 and green > blue + 15:
        return "[GREEN]"
    if abs(red - green) < 30 and abs(green - blue) < 30:
        return "[GRAY]"
    return "[NOT_RATED]"


def _classify_bar(image_path: str) -> str:
    avg, _, _ = _avg_color(image_path)
    if avg is None:
        return "[NOT_RATED]"
    return _label_from_rgb(*avg).replace("]", "_BAR]")


def classify_icon(image_path: str) -> str:
    """Classify an icon image by dominant non-background pixel color."""
    avg, width, height = _avg_color(image_path)

    if width > 50 and height > 50:
        return _classify_bar(image_path) if width <= _BAR_VERT_WIDTH else "[IMAGE]"
    if (width, height) == _BAR_HORIZ_SIZE or width == _BAR_VERT_WIDTH:
        return _classify_bar(image_path)
    if width > 100 and height < 20:
        return "[SEPARATOR]"
    if width > 50:
        return "[IMAGE]"
    if avg is None:
        return "[NOT_RATED]"
    return _label_from_rgb(*avg)


def build_icon_map(images_dir: str) -> dict[str, str]:
    """Pre-scan companion images and build {filename: label}."""
    icon_map: dict[str, str] = {}
    if not os.path.isdir(images_dir):
        logger.warning("Images directory not found: %s", images_dir)
        return icon_map

    for filename in os.listdir(images_dir):
        if filename.lower().endswith((".gif", ".png", ".jpg", ".jpeg")):
            icon_map[filename] = classify_icon(os.path.join(images_dir, filename))

    logger.info("Classified %d images in %s", len(icon_map), images_dir)
    return icon_map


def detect_encoding(html_bytes: bytes) -> str:
    """Detect encoding from HTML meta tags, defaulting to windows-1252."""
    head = html_bytes[:2048].decode("ascii", errors="ignore")
    match = re.search(r'charset=(["\']?)([^"\'\s;>]+)', head, re.IGNORECASE)
    if match:
        return match.group(2)
    return "windows-1252"
