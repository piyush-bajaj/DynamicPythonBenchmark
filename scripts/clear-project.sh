#!/usr/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}

echo "Clear Project folder for $1"

#current working directory
WORK_DIR=$(pwd)

#proceed only if temp folder exists
if [[ -d temp ]]
then
    cd temp
else
    echo "Project directory does not exist"
    exit
fi

#remove directory if it exists
if [[ -d "project$2" ]]
then
    rm -rf "project$2"
else
    echo "Project does not exist"
fi
