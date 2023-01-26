#!/usr/bin/bash

ROOT_DIR=$(pwd)

if [[ -d Project ]]
then
    cd Project
else
    echo "Projects are not installed! Please install them first."
    exit
fi

WORK_DIR=$(pwd)

#loop through all projects
for idx in {1..50};
do
    cd "$WORK_DIR/project$idx"
    #activate virtual env
    if [[ -d "vm/local" ]]
    then
        source vm/local/bin/activate
    elif [[ -d "vm/bin" ]]
    then
        source vm/bin/activate
    else
        echo "Unable to create virtual env"
        exit
    fi
    #upgrade dynypyt for the project
    pip install dynapyt --upgrade
done

#proceed only if temp folder exists
if [[ -d temp ]]
then
    rm -rf temp
    echo "Please run instrumentation again."
fi