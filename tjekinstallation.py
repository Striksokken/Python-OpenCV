import pyvirtualcam
import numpy as np

with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
    print(f"Virtual camera '{cam.device}' started")
    frame = np.zeros((720, 1280, 3), np.uint8)  # Sort baggrund
    for _ in range(100):
        cam.send(frame)
        cam.sleep_until_next_frame()
