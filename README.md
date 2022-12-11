# DyPyBench
Master Thesis Project

## Setting Up DyPyBench

### Requirements
- Ubuntu >= 20.04
- Python >= 3.8
- pip >= 22.0
- python3-virtualenv >= 20.16.6
- libjpeg8-dev (project requirement)
- Git >= 2.34
- Docker >= 20.10

### Steps to setup DyPyBench on Ubuntu Machine
1. Clone DyPyBench Repository
    - git clone https://github.com/sola-st/master-thesis-piyush-bajaj.git
2. Change the permissions for the bash files
    - chmod 777 auto-script.sh
    - chmod 777 auto-test.sh
3. Initialize DyPyBench (download the project repositories and dependencies inside python virtual environement for each project) : Ensure the requirements are met before proceeding with this step.
    - ./auto-script.sh > install.log 2>&1
4. Check the installation
    - Check the file install.log to see if there are any errors

### Steps to setup DyPyBench on Docker Container
1. Clone DyPyBench Repository
    - git clone https://github.com/sola-st/master-thesis-piyush-bajaj.git
2. Build docker image using docker build command
    - docker build -t dypybench .
3. Run the created docker image to start the container
    - docker run -itd --name dypybench dypybench
4. Login to the docker container and execute the bash scripts.
    - docker start -i dypybench
    - ./auto-script.sh > install.log 2>&1

### Steps to use existing Docker Container of DyPyBench
1. Download the required tar file
    - Download the latest prepared docker image tar file from https://drive.google.com/drive/folders/1P2hrq-DisDwTtoVVMNblpztBbbZAPV5c?usp=sharing
2. Run the docker load command to get the image in local docker images
    - docker load -i dypybenchv0.1.tar
3. Run the loaded docker image to start the container
    - docker run -itd --name dypybench dypybenchv0.1
4. Login to the container
    - docker start -i dypybenchv0.1

## Using DyPyBench
1. List the projects setup in DyPyBench
    - python3 run_dypybench.py --list
2. Run Test Suites of one or more available projects
    - python3 run_dypybench.py --test 1 2 3 4
2. Run DynaPyt Instrumentation
    - python3 run_dypybench.py --instrument 1 2 3 4 --directory ./grab --analysis TraceAll
    - python3 run_dypybench.py --instrument 1 2 3 4 --files ./test.py --analysis TraceAll
3. Run DynaPyt Analysis
    - python3 run_dypybench.py --run 1 2 3 4 --entry ./run_all_tests.py --analysis TraceAll

### Available flags
1. --list / -l 
    - list the projects
2. --test / -t
    - specify projects for test
3. --instrument / -i
    - specify projects for instrumentation
4. --run / -r
    - specify projects for analysis
5. --directory / -d
    - specify directory for instrumentation
6. --files / -f
    - specify file for instrumentation
7. --analysis / -a
    - name of the analysis to run
8. --entry / -e
    - entry file for analysis
9. --save / -s
    - specify the file to save output
