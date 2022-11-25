#!/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}
echo "Starting the installation, setup and running of python projects and their test suites"

echo "Please provide the complete location of url file"
#read URL_FILE
URL_FILE=/home/bajajpn/Automation/github-url.txt

# Create project folder to keep all the projects together inside one parent folder
PROJ_DIR=Project
#if folder already present, then delete the folder
if [ -d "$PROJ_DIR" ]
then
    rm -rf "$PROJ_DIR" 
fi

#create directory
mkdir -p "$PROJ_DIR"
cd "$PROJ_DIR"

#current working directory
WORK_DIR=$(pwd) 

#run a while loop to create vm for all projects
idx=1
while read line
do
    echo $line

    echo "Start time :" 
    timestamp

    #change to working directory
    cd $WORK_DIR
    #create directory for project
    mkdir -p "project$idx"
    #clone the repo to project directory
    git clone "$line" "project$idx"
    #go into the project directory
    cd "project$idx"
    #create virtual env name vm
    virtualenv vm
    #activate virtual env
    source vm/bin/activate
    #install using setup.py file or requirements.txt

    if [ -e setup.py ]
    then
        python setup.py install
    elif [ -e requirements.txt ]
    then
        pip install -r requirements.txt
    else
        echo "No setup.py file or requirements.txt found"
    fi

    #install pytest library
    pip install pytest

    echo "End time : "
    timestamp

    #run tests
    
    ((idx++))

done < $URL_FILE
