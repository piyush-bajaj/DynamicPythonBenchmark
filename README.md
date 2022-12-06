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
4. Login to the docker image and execute the bash scripts.
    - docker start -i dypybench
    - ./auto-script.sh > install.log 2>&1

## Using DyPyBench
1. Run Test Suites of all projects
    - ./auto-test.sh tests
2. Run DynaPyt Instrumentation
    - ./auto-test.sh dynapyt.instrument
3. Run DynaPyt Analysis
    - ./auto-test.sh dynapyt.analysis
4. Run DynaPyt Instrumentation and Analysis
    - ./auto-test.sh dynapyt