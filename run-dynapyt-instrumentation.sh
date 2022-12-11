#!/usr/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}

echo "Running dynapyt instrumentation on $1"

#current working directory
WORK_DIR=$(pwd)

#create and change to temp folder
mkdir "temp"
cd "temp"

#copy project folder to temp folder
cp -r "$WORK_DIR/Project/project$2" .

cd project$2

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

#install dynapyt dependencies
pip install dynapyt libcst pytest-xdist

#run instrumentation on the given directory
python -m dynapyt.run_instrumentation --directory $3 --analysis $4

#deactivate vm
deactivate