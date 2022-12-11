#!/usr/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}

echo "Running test suite of $1"

#current working directory
WORK_DIR=$(pwd)

mkdir "temp"
cd "temp"
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

echo "\n--------------Test Time Start--------------\n"
timestamp
echo "\n--------------Test Time Start--------------\n"

#if [ $URL == "https://github.com/lorien/grab.git" ]
if [ $1 == "grab" ]
then
    python runtest.py --test-all    #tests for grab project are not named correctly and run from a py file
else
    pytest $3
fi

echo "\n--------------Test Time End--------------\n"
timestamp
echo "\n--------------Test Time End--------------\n"

deactivate