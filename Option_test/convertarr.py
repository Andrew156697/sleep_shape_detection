import pandas as pd
import numpy as np
import logging
import os
from influxdb_client import InfluxDBClient, QueryApi
import matplotlib.pyplot as plt


# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cấu hình kết nối InfluxDB
bucket = "test2"
token = "fCtJij8tgs27OpTf9ZiJDiu7EtPxwRthAvfHDIxqLoA4wsL0873Rq2y8N-Y2cyvtcM9KFdYQb2zrLrcK9H1mGA=="
org = "97a897b1d7c9ba9d"
url = "http://192.168.100.42:8086/"

# Tên file CSV để lưu trữ kết quả
csv_file_path = 'landmarks_data.csv'


def query_influxdb_and_export():
    try:
        # Khởi tạo kết nối với InfluxDB
        with InfluxDBClient(url=url, token=token, org=org) as client:
            query_api: QueryApi = client.query_api()

            # Viết truy vấn Flux
            query = f'''
            from(bucket: "{bucket}")
              |> range(start: -60m)
              |> filter(fn: (r) => r["_measurement"] == "0" or 
                                 r["_measurement"] == "1" or 
                                 r["_measurement"] == "2" or 
                                 r["_measurement"] == "3" or 
                                 r["_measurement"] == "4" or 
                                 r["_measurement"] == "5" or 
                                 r["_measurement"] == "6" or 
                                 r["_measurement"] == "7" or 
                                 r["_measurement"] == "8" or 
                                 r["_measurement"] == "9" or 
                                 r["_measurement"] == "10" or 
                                 r["_measurement"] == "11" or 
                                 r["_measurement"] == "12" or 
                                 r["_measurement"] == "13" or 
                                 r["_measurement"] == "14" or 
                                 r["_measurement"] == "15" or 
                                 r["_measurement"] == "16" or 
                                 r["_measurement"] == "17" or 
                                 r["_measurement"] == "18" or 
                                 r["_measurement"] == "19" or 
                                 r["_measurement"] == "20" or 
                                 r["_measurement"] == "21" or 
                                 r["_measurement"] == "22" or 
                                 r["_measurement"] == "23" or 
                                 r["_measurement"] == "24" or 
                                 r["_measurement"] == "25" or 
                                 r["_measurement"] == "26" or 
                                 r["_measurement"] == "27" or 
                                 r["_measurement"] == "28" or 
                                 r["_measurement"] == "29" or 
                                 r["_measurement"] == "30" or 
                                 r["_measurement"] == "31" or 
                                 r["_measurement"] == "32"
              )
            '''

            logger.info("Đang thực hiện truy vấn InfluxDB...")
            result = query_api.query(query)
            logger.info("Truy vấn thành công.")

            # Tạo một từ điển để lưu trữ dữ liệu
            data = {}

            # Xử lý kết quả truy vấn
            for table in result:
                for record in table.records:
                    time = record.get_time().strftime('%Y-%m-%d %H:%M')  # Format thời gian
                    key = record.get_field()
                    value = record.get_value()

                    # Khởi tạo từ điển con nếu chưa có thời gian
                    if time not in data:
                        data[time] = {}

                    # Lưu giá trị vào từ điển
                    data[time][key] = value

            # Chuyển đổi dữ liệu sang DataFrame
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index = pd.to_datetime(df.index)  # Chuyển index sang datetime

            # Sắp xếp DataFrame theo thứ tự tăng dần của time_write
            df = df.sort_index()

            # Loại bỏ cột đầu tiên
            # df = df.iloc[:, 1:]  # Loại bỏ cột đầu tiên (cột index 0)

            print(df.shape)

            # Tạo mảng để lưu 32 điểm (mỗi điểm có 3 trục x, y, z)
            all_coordinates = []

            # Duyệt từng hàng của file
            for index, row in df.iterrows():
                # Chuyển dữ liệu của hàng hiện tại thành một danh sách
                row_data = row.values
                
                # Chia dữ liệu thành nhóm 3 (x, y, z)
                points = row_data.reshape(-1, 4)
                
                # Lọc lấy 32 điểm đầu tiên nếu đủ
                if len(points) >= 32:
                    all_coordinates.append(points[:32])  # Thêm 32 điểm vào mảng
                else:
                    print(f"Dòng {index + 1} không đủ 32 điểm.")

            # Chuyển danh sách thành numpy array
            result = np.array(all_coordinates)
            print(result)

            return result       

    except Exception as e:
        logger.error(f"Lỗi xảy ra khi truy vấn hoặc xử lý dữ liệu: {e}")


def convert2Imgae(data,index):
    filtered_landmarks = [(x, y) for visibility, x, y, z  in data if visibility > 0.5]

    # Tách các tọa độ x, y
    x_coords = [point[0] for point in filtered_landmarks]
    y_coords = [point[1] for point in filtered_landmarks]

    # Vẽ các điểm
    plt.figure()
    plt.scatter(x_coords, y_coords, c='b', marker='o')

    # Thiết lập nhãn cho các trục
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')

    # Thiết lập tiêu đề
    plt.title('Landmarks with Visibility > 0.5')

    # Xuất hình ảnh ra file JPG
    output_folder = 'images1'
    os.makedirs(output_folder, exist_ok=True)   
    plt.savefig('landmarks_visibility_2d.jpg', format='jpg')
    plt.savefig(os.path.join(output_folder, f'landmarks_{index}.jpg'), format ='jpg')


    # Hiển thị đồ thị
    plt.show()


if __name__ == "__main__":
    data = query_influxdb_and_export()
    index = 0
    for x in data:
        index = index + 1
        convert2Imgae(x,index)
