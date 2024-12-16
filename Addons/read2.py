from influxdb_client import InfluxDBClient
import pandas as pd

# Chi tiết kết nối
bucket = "test1"
token = "f1hPnzVwo3elefsiIlXM4_yRwme12_C9sD9rRxZroeihZcBbpB03W0_dnyQB0AS3Mgw6qySUS6m4V6WEA_Kvpw=="
org = "chtlab"
url = "http://192.168.137.214:8086"  # Đảm bảo URL bao gồm giao thức (http://)
client = InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

# Xác định phạm vi thời gian cho truy vấn
start_time = "2024-12-15T19:33:30Z"  # Thay thế bằng thời gian bắt đầu của bạn
stop_time = "2024-12-15T19:34:50Z"   # Thay thế bằng thời gian dừng của bạn

# Tạo truy vấn
query = f'''
from(bucket: "{bucket}")
  |> range(start: -50m)\
  |> filter(fn: (r) => r["_measurement"] == "points")\
'''

# Thực thi truy vấn
result = query_api.query(org=org, query=query)

# Xử lý kết quả
data = []
for table in result:
    for record in table.records:
        data.append((record.get_time(), record.get_field(), record.get_value()))

# Tạo một DataFrame
df = pd.DataFrame(data, columns=['time', 'field', 'value'])

# Chuyển đổi 'time' thành datetime
df['time'] = pd.to_datetime(df['time'])

# Nhóm theo thời gian và lọc các nhóm có nhiều hơn một bản ghi
grouped = df.groupby('time').filter(lambda x: len(x) > 1)

# Sắp xếp dữ liệu để dễ đọc
grouped = grouped.sort_values(by='time')

# Hiển thị kết quả
print(grouped[['time', 'field', 'value']])

# Đóng kết nối máy khách
client.close()
