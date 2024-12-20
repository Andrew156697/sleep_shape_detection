FROM python:3.10.12-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install opencv-python-headless
RUN pip install mediapipe
RUN pip install pandas
RUN pip install openpyxl
RUN pip3 install influxdb-client


COPY run.py /run.py

CMD ["python", "run.py"]
