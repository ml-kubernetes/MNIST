FROM tensorflow/tensorflow:1.13.1
LABEL maintainer="alice_k106@naver.com"
RUN pip install flask flask_dropzone Pillow && \
  mkdir /home/uploads
ADD server.py /home/
ADD templates /home/templates
WORKDIR /home/uploads
ENTRYPOINT ["python", "/home/server.py"]
