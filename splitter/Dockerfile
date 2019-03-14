FROM tensorflow/tensorflow:1.13.1
LABEL maintainer="nlkey2022@gmail.com"
RUN apt-get update
WORKDIR /home
ADD ./splitter.py /home
ENTRYPOINT ["python", "splitter.py"]
