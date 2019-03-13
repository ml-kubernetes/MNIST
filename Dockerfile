FROM tensorflow/tensorflow:1.13.0rc2

RUN apt-get update && cd /root
RUN apt-get install curl -y
RUN curl https://gist.githubusercontent.com/graykode/f68d6367f97faa28a401ce2459828c9a/raw/0bed26ecca7e046aa7d20c0df62a16d42c7c4877/mnist.py -O mnist.py