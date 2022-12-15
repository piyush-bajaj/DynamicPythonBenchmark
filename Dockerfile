FROM ubuntu:latest

WORKDIR /DyPyBench

RUN apt-get update

RUN apt-get install python3 -yq

RUN apt install python3-pip -yq

RUN apt install python3-virtualenv -yq

RUN apt install libjpeg8-dev -yq

RUN apt install git -yq

RUN pip install --upgrade pip setuptools wheel

COPY ./github-url.txt ./github-url.txt

COPY ./auto-script.sh ./auto-script.sh

COPY ./run_dypybench.py ./run_dypybench.py

COPY ./run-dynapyt-analysis.sh ./run-dynapyt-analysis.sh

COPY ./run-test.sh ./run-test.sh

COPY ./run-dynapyt-instrumentation.sh ./run-dynapyt-instrumentation.sh

COPY ./includes.txt ./includes.txt

COPY ./clear-project.sh ./clear-project.sh

#RUN ./auto-script.sh docker > out.log 2>&1

#RUN ./auto-script.sh docker tests > out.log 2>&1