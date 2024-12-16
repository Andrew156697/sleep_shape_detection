import cv2
import logging
import os
from time import sleep
import mediapipe as mp
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


bucket = "storage"
token = "5VXStBHdRgn-NxSy_cxzqzSU0EaAR1OSzLESuKPjV3_IV85EelzvO2RMU_LeJOgTy0iEsxABRraKLxdBnIbv-w=="
org = "chtlab"
url = "http://192.168.1.29:8086"

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
    logging.error("Can't open camera")
    exit()
else:
    logging.info("Camera ready!")

try:
    while True:
        success, frame = camera.read()
        if not success:
            logging.error("Can't get frame from camera.")
            break

        # Đổi sang không gian màu RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Dự đoán pose landmarks
        results = pose.process(rgb_frame)

        # Xử lý kết quả
        if results.pose_landmarks:
            logging.info("Connected! Landmarks detected.")
            points = []
            data_table = []

            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                x, y, z = landmark.x, landmark.y, landmark.z  # Tọa độ chuẩn hóa
                data_table.append((idx, x, y, z))
                logging.info(f"Landmark {idx}: x={x:.2f}, y={y:.2f}, z={z:.2f}")

                point_id = str(idx)
                # Tạo dữ liệu Point cho từng landmark
                point = Point(point_id) \
                    .field("x", x) \
                    .field("y", y) \
                    .field("z", z) \
                    .time(time=None, write_precision=WritePrecision.NS)
                if client:
                    try:
                        write_api.write(bucket=bucket, org=org, record=point)
                    except Exception as e:
                        logging.error(f"Error writing to InfluxDB: {e}")
                
                print(point)

            # logging.debug(f"landmarks Table:\n{data_table}")
            
            
        sleep(5)
except Exception as e:
    logging.error(f"Error: {e}")
finally:
    camera.release()
    if client:
        client.close()
    logging.info("Camera and InfluxDB connection have been released.")
