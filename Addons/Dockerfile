FROM python:3.10.12-slim

RUN apt update && apt install -y \
    python3-dev
    

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install opencv-python-headless
RUN pip install mediapipe
RUN pip install pandas
RUN pip install openpyxl
RUN pip3 install influxdb-client

#COPY write.py /write.py
COPY write2.py /write2.py
#COPY read2.py /read2.py
#COPY read.py /read.py

CMD ["python", "write2.py"]
