FROM tensorflow/tensorflow:1.13.1
LABEL maintainer="alice_k106@naver.com"
RUN pip install flask flask_dropzone Pillow
ADD ["server.py", "templates", "uploads", "/home/"]
ENTRYPOINT ["python", "/home/server.py"]
