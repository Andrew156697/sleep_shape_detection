from influxdb_client import InfluxDBClient
import pandas as pd

# Chi tiết kết nối
bucket = "test1"
token = "RV_G0qv6j_IuGbL_ITsG_mRkWZZz6dFIqFI76XExtftLAOIKh1AOqgsKMj1vhWxr2czFf-svcFjTm_pdz6vSSA=="
org = "59f6f678313bf9b1"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

# Tạo truy vấn
query = f'''
from(bucket: "{bucket}")
  |> range(start: -4h)\
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
