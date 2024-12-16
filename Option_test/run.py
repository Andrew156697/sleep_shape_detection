import json
import cv2
import logging
import os
from time import sleep
import mediapipe as mp
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


#----------------------configuration---------------- 


# Tắt TF_DELEGATE_OPTIONS nếu không cần thiết
os.environ["TF_DELEGATE_OPTIONS"] = "0"

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config kết nối InfluxDB
bucket = "test1"
token = "lAylyIEo7Xjub7kr2I0GV5kr3I03JkDK5VghmVz3vMwFWOdarMvT_sXtb7MGyFfeTa9jPXDdDvOV8rD7UhmNsg=="
org = "97a897b1d7c9ba9d"
url = "http://192.168.100.42:8086"

# Tắt TF_DELEGATE_OPTIONS nếu không cần thiết
os.environ["TF_DELEGATE_OPTIONS"] = "0"

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


#----------------------------Function------------


def load_options(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading options: {e}")
        return {}
    
def open_camera(camera_id):
    try:
        client = InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
    except Exception as e:
        logging.error(f"Lỗi kết nối InfluxDB: {e}")
        client = None

    camera = cv2.VideoCapture(camera_id)
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



def main():
    options_path = "data/options.json"  # Đường dẫn đến tệp options.json
    options = load_options(options_path)
    camera_id = int(options.get("mycamera"))
    # print(type(int(camera_id)))
    print("this is camera id: ",camera_id)
    open_camera(0)



if __name__ == "__main__":
    main()