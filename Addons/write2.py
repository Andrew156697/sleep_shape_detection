import cv2
import logging
import os
from time import sleep
import mediapipe as mp
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Config kết nối InfluxDB
bucket = "test2"
token = "f8bXUcj_hlnb_Ey_KFH45D5T1Ln2AWF-WSniwGVwYpDHWuY7Gm_CaJwB_zJNFgsxUY6qiad40bnioWOAOGzQ7g=="
org = "chtlab"
url = "http://shapepose.local:8086"

try:
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
except Exception as e:
    logging.error(f"Lỗi kết nối InfluxDB: {e}")
    client = None

# Tắt TF_DELEGATE_OPTIONS nếu không cần thiết
os.environ["TF_DELEGATE_OPTIONS"] = "0"

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Mở camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    logging.error("Không thể mở camera.")
    exit()
else:
    logging.info("Camera đã sẵn sàng.")

try:
    while True:
        success, frame = camera.read()
        if not success:
            logging.error("Không thể lấy frame từ camera.")
            break

        # Đổi sang không gian màu RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Dự đoán pose landmarks
        results = pose.process(rgb_frame)

        # Xử lý kết quả
        if results.pose_landmarks:
            logging.info("Connected! Landmarks detected.")

            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                x, y, z = landmark.x, landmark.y, landmark.z  # Tọa độ chuẩn hóa
                logging.info(f"Landmark {idx}: x={x:.3f}, y={y:.3f}, z={z:.3f}")

                # Tạo dữ liệu Point cho từng landmark
                point = Point("points") \
                    .field(f"x{idx}", x) \
                    .field(f"y{idx}", y) \
                    .field(f"z{idx}", z) \
                    .time(time=None, write_precision=WritePrecision.NS)
                
                if client:
                    try:
                        write_api.write(bucket=bucket, org=org, record=point)
                    except Exception as e:
                        logging.error(f"Lỗi khi ghi vào InfluxDB: {e}")
                
                # print("day la point: \n")
                # print(point)

        sleep(7)
except Exception as e:
    logging.error(f"Lỗi xảy ra: {e}")
finally:
    camera.release()
    if client:
        client.close()
    logging.info("Camera và kết nối InfluxDB đã được giải phóng.")