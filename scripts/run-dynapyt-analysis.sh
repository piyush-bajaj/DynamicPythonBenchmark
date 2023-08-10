#!/usr/bin/bash

# args
# $1 = project name
# $2 = project number
# $3 = analysis name
# $4 = test folder/file
# $5 = timeout in seconds

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}

echo "Running dynapyt analysis on $1"

#current working directory
ROOT_DIR=/DyPyBench

cd $ROOT_DIR

#check if instrumentation is done first
if [[ ! -d temp/project$2 ]]
then
    echo "Please perform instrumentation first"
    exit
fi

#change to project directory
cd "temp/project$2"

#activate virtual env
if [[ -d ".vm/local" ]]
then
    source .vm/local/bin/activate
elif [[ -d ".vm/bin" ]]
then
    source .vm/bin/activate
else
    echo "Unable to activate virtual env"
    exit
fi

printf "import pytest\n\npytest.main(['--import-mode=importlib', '$ROOT_DIR/temp/project$2/$4'])\n" > run_all_tests.py

#run analysis on the given project
timeout -k 10s $5 python -m dynapyt.run_analysis --entry ./run_all_tests.py --analysis $3

#deactivate vm
deactivate