FROM tensorflow/tensorflow:1.13.1
LABEL maintainer="nlkey2022@gmail.com"
RUN apt-get update
WORKDIR /home
ADD trainer.py /home
ENTRYPOINT ["python", "trainer.py"]