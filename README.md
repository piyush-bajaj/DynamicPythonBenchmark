# DyPyBench
Master Thesis Project

## Setting Up DyPyBench

### Requirements
- Python >= 3.8
- pip >= 22.0
- python3-virtualenv >= 20.16.6
- ffmpeg (project requirement)
- libjpeg8-dev (project requirement)
- libavcodec-extra (project requirement)
- Git >= 2.34
- Docker >= 20.10

### Steps to setup DyPyBench on Docker Container
1. Clone DyPyBench Repository
    - git clone https://github.com/sola-st/master-thesis-piyush-bajaj.git
2. Build docker image using docker build command
    - docker build -t dypybench .
3. Run the created docker image to start the container
    - docker run -itd --name dypybench dypybench
4. Login to the docker container and execute the bash scripts.
    - docker start -i dypybench
    - ./scripts/install-all-projects.sh > install.log 2>&1

### Steps to use existing Docker Container of DyPyBench
1. Pull the docker image from dockerhub (use the provided docker credentials for access)
    - docker pull dypybench/dypybench:v0.6
2. Run the docker image to start the container
    - docker run -itd --name dypybenchv0.6 dypybench/dypybenchv0.6
3. Login to the container
    - docker start -i dypybenchv0.6

### Copying files between Docker Container and Local Machine
1. Using volume to map local directory to container directory
    - Start the container with the --volume flag and provide full folder paths
        - docker run -itd --volume local_folder:container_folder --name dypybenchv0.6 dypybench/dypybenchv0.6
2. Copy files or folders individually from running container to local machine
    - docker cp container_name:container_path local_path 
3. Copy files or folders individually to running container from local machine
    - docker cp local_path container_name:container_path

## Using DyPyBench
1. List the projects setup in DyPyBench
    - python3 dypybench.py --list
2. Run Test Suites of one or more available projects
    - python3 dypybench.py --test 1 2 3 4
2. Run DynaPyt Instrumentation
    - python3 dypybench.py --instrument 1 2 3 4 --file ./text/includes.txt --analysis TraceAll
3. Run DynaPyt Analysis
    - python3 dypybench.py --run 1 2 3 4 --analysis TraceAll
4. Run LExecutor Instrumentation
    - python3 dypybench.py --lex_instrument 1 2 3 4 --lex_file ./text/includes.txt
5. Run tests to generate LExecutor trace
    - python3 dypybench.py --lex_test 1 2 3 4
6. Update DynaPyt source code
    - python3 dypybench.py --update_DynaPyt_source
7. Update LExecutor source code
    - python3 dypybench.py --update_LExecutor_source

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
8. --original
    - run tests on code present in original folder
9. --update_DynaPyt_source
    - get or update dynapyt source code
10. --update_LExecutor_source
    - get or update LExecutor source code
11. --lex_instrument / -li
    - Specify the project no. to run LExecutor instrumentation
12. --lex_file / -lf
    - Specify the path to file containing the includes.txt file to run the instrumentation
13. --lex_test / -lt
    - Specify the project no. to run LExecutor Tests for trace generation
14. --timeout
    - Specify timeout to be used in seconds for running test suite and analysis, default is 600 seconds

## Structure of includes.txt for DynaPyt
    - proj_name flag path
        - proj_name: Project name for which the entry belongs to
        - flag: d for directory path or f for file path
        - path: path of the file/directory to instrument from the root of the project

## Structure of includes.txt for LExecutor
    - proj_name path
        - proj_name: Project name for which the entry belongs to
        - path: path of the file to instrument from the root of DyPyBench
