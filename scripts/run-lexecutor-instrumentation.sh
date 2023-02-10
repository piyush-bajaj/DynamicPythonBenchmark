#!/usr/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}

echo "Running LExecutor instrumentation on $1"

#current working directory
ROOT_DIR=$(pwd)

#create and change to temp folder
if [[ ! -d "temp" ]]
then
    mkdir "temp"
fi

cd "temp"

if [[ ! -d "project$2" ]]
then
    #copy project folder to temp folder
    cp -r "$ROOT_DIR/Project/project$2" .
fi

cd project$2

#copy the dynypyt src if needed
if [[ -d "$ROOT_DIR/LExecutor" ]]
then
    cp -r "$ROOT_DIR/LExecutor" "./LExecutor"
fi

#activate virtual env
if [[ -d "vm/local" ]]
then
    source vm/local/bin/activate
elif [[ -d "vm/bin" ]]
then
    source vm/bin/activate
else
    echo "Unable to activate virtual env"
    exit
fi

#install LExecutor
if [[ -d ./LExecutor ]]
then
    pip install -r ./LExecutor/requirements.txt
    pip install -e ./LExecutor
else
    echo "LExecutor is not installed, please install it first before continuing"
    exit
fi

# run instrument for given files or a single .txt file, other arguments can be added later using if else
python -m lexecutor.Instrument --files ${@:3}

#deactivate vm
deactivate