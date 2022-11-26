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

    parts=($line)
    URL=${parts[0]}
    FLAGS=${parts[1]}

    echo "Start time :" 
    timestamp

    #change to working directory
    cd $WORK_DIR
    #create directory for project
    mkdir -p "project$idx"
    #clone the repo to project directory
    git clone "$URL" "project$idx"
    #go into the project directory
    cd "project$idx"
    #create virtual env name vm
    virtualenv vm
    #activate virtual env
    source vm/bin/activate
    #install using setup.py file or requirements.txt

    if [ -e setup.py ]
    then
        echo "Running setup install"
        python setup.py install
    #elif [ -e requirements.txt ]
    #then
    #    find ./ -name '*requirements.txt' -or -name 'requirements*.txt' -exec pip install -r {} \;
    #    pip install -r requirements.txt
    #else
    #    echo "No setup.py file or requirements.txt found"
    fi

    if [[ $FLAGS == "r" || $FLAGS == "rt" ]]
    then
        REQ_FILE=${parts[2]}
        echo "Running pip install requirements"
        pip install -r $REQ_FILE
    fi

    #install pytest library
    pip install pytest

    echo "End time : "
    timestamp

    #run tests
    #if [ $URL == "https://github.com/lorien/grab.git" ]
    if [ $FLAGS == "r" ]
    then
        python runtest.py --test-all
    elif [ $FLAGS == "rt" ]
    then
        TEST_FOLDER=${parts[3]}
        pytest $TEST_FOLDER
    elif [ $FLAGS == "t" ]
    then
        TEST_FOLDER=${parts[2]}
        pytest $TEST_FOLDER
    fi    

    ((idx++))

done < $URL_FILE
