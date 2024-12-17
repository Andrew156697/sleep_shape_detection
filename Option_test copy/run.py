import json
import cv2
import logging
import os
from time import sleep
import mediapipe as mp
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime


#----------------------configuration---------------- 


# Tắt TF_DELEGATE_OPTIONS nếu không cần thiết
os.environ["TF_DELEGATE_OPTIONS"] = "0"

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config kết nối InfluxDB
# bucket = "test1"
# token = "lAylyIEo7Xjub7kr2I0GV5kr3I03JkDK5VghmVz3vMwFWOdarMvT_sXtb7MGyFfeTa9jPXDdDvOV8rD7UhmNsg=="
# org = "97a897b1d7c9ba9d"
# url = "http://192.168.100.42:8086"

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
    
def open_camera(camera_id, url, token, org, bucket,duration):
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
            now = datetime.now()
            # time_wrtire = now.strftime('%Y%m%d%H%M%S')
            # Xử lý kết quả
            if results.pose_landmarks:
                logging.info("Connected! Landmarks detected.")

                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    x, y, z, visibility = landmark.x, landmark.y, landmark.z, landmark.visibility  # Tọa độ chuẩn hóa
                    logging.info(f"Landmark {idx}: x ={x:.3f}, y={y:.3f}, z={z:.3f}, visibility={visibility:3f}")

                    # Tạo dữ liệu Point cho từng landmark
                    point = Point(f"{idx}") \
                        .field(f"x{idx}", x) \
                        .field(f"y{idx}", y) \
                        .field(f"z{idx}", z) \
                        .field(f"visibility{idx}", visibility) 
                        # .field(f"timewrtire{idx}", time_wrtire) 
                        # .time(time=None, write_precision=WritePrecision.NS)
                    
                    if client:
                        try:
                            write_api.write(bucket=bucket, org=org, record=point)
                        except Exception as e:
                            logging.error(f"Lỗi khi ghi vào InfluxDB: {e}")
                    
            sleep(duration)
    except Exception as e:
        logging.error(f"Lỗi xảy ra: {e}")
    finally:
        camera.release()
        if client:
            client.close()
        logging.info("Camera và kết nối InfluxDB đã được giải phóng.")



def main():
    options_path = "/data/options.json"  # Đường dẫn đến tệp options.json
    options = load_options(options_path)

    bucket = options.get("my_bucket")
    token = options.get("my_token")
    org = options.get("my_org")
    url = options.get("my_url")
    duration = options.get("my_duration")
    camera_id = options.get("my_camera")

    if duration is None:
        logger.error("Key 'my_duration' is missing in options.json")
        return

    try:
        duration = int(duration)
    except ValueError:
        logger.error(f"Invalid value for 'my_duration': {duration}")
        return
    
    if camera_id is None:
        logger.error("Key 'my_camera' is missing in options.json")
        return

    try:
        camera_id = int(camera_id)
    except ValueError:
        logger.error(f"Invalid value for 'my_camera': {camera_id}")
        return

    logger.info(f"Using camera ID: {camera_id}")
    print(type(camera_id))
    print("This is camera ID:", camera_id)
    open_camera(camera_id,url=url,token=token,org=org,bucket=bucket,duration=duration)


if __name__ == "__main__":
    main()