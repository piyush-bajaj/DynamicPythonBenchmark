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
    - chmod 777 run-test.sh
    - chmod 777 run-dynapyt-analysis.sh
    - chmod 777 run-dynapyt-instrumentation.sh
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
1. Pull the docker image from dockerhub (use the provided docker credentials for access)
    - docker pull dypybench/dypybench:v0.2
2. Run the docker image to start the container
    - docker run -itd --name dypybenchv0.2 dypybench/dypybenchv0.2
3. Login to the container
    - docker start -i dypybenchv0.2

## Using DyPyBench
1. List the projects setup in DyPyBench
    - python3 run_dypybench.py --list
2. Run Test Suites of one or more available projects
    - python3 run_dypybench.py --test 1 2 3 4
2. Run DynaPyt Instrumentation
    - python3 run_dypybench.py --instrument 1 2 3 4 --file ./includes.txt --analysis TraceAll
3. Run DynaPyt Analysis
    - python3 run_dypybench.py --run 1 2 3 4 --analysis TraceAll

### Available flags
1. --list / -l 
    - list the projects
2. --test / -t
    - specify projects for test
3. --instrument / -i
    - specify projects for instrumentation
4. --run / -r
    - specify projects for analysis
5. --file / -f
    - specify path of includes.txt file for instrumentation
6. --analysis / -a
    - name of the analysis to run
7. --save / -s
    - specify the file to save output

## Structure of includes.txt
    - proj_no flag path
        - proj_no: Project number for which the entry is
        - flag: d for directory path or f for file path
        - path: path of the file/directory to instrument