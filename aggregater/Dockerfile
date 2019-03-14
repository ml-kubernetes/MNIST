FROM tensorflow/tensorflow:1.13.1
LABEL maintainer="nlkey2022@gmail.com"
RUN apt-get update
WORKDIR /home
ADD aggregater.py /home
ENTRYPOINT ["python", "aggregater.py"]