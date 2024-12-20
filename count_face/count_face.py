import json
import cv2
import logging
import os
from time import sleep
import mediapipe as mp
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# --------------------configuration---------------------

# Khởi tạo Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Mở video từ webcam
cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Không thể đọc video.")
            break

        # Chuyển đổi hình ảnh sang RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        # Vẽ các khuôn mặt phát hiện được
        if results.detections:
            face_count = len(results.detections)
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = image.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(image, bbox, (255, 0, 0), 2)

            # Hiển thị số lượng khuôn mặt
            cv2.putText(image, f'Face Count: {face_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Hiển thị hình ảnh
        cv2.imshow('Face Detection', image)

        if cv2.waitKey(5) & 0xFF == ord('q'):  # Nhấn 'Esc' để thoát
            break

cap.release()
cv2.destroyAllWindows()