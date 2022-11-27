#!/usr/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}
echo "Starting the installation, setup and running of python projects and their test suites"

#current working directory
WORK_DIR=$(pwd)

echo "Please provide the complete location of url file"
#read URL_FILE
URL_FILE=$WORK_DIR/github-url.txt

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

WORK_DIR=$(pwd)

#run a while loop to create vm for all projects
idx=1
while read line
do
    echo $line

    parts=($line)
    URL=${parts[0]}
    FLAGS=${parts[1]}

    echo "\n--------------Setup Start Time--------------\n" 
    timestamp
    echo "\n--------------Setup Start Time--------------\n"

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
        if [[ $URL == "https://github.com/spotify/dh-virtualenv.git" ]]
        then
            sed -i.bak '0,/invoke==0.13.0/s//invoke/' dev-requirements.txt  #fix for dependency conflict issue
        fi
        echo "Running pip install requirements"
        pip install -r $REQ_FILE
    fi

    #install pytest library
    pip install pytest

    echo "\n--------------Setup End Time--------------\n"
    timestamp
    echo "\n--------------Setup End Time--------------\n"

    #run tests
    echo "\n--------------Test Time Start--------------\n"
    timestamp
    echo "\n--------------Test Time Start--------------\n"
    
    #if [ $URL == "https://github.com/lorien/grab.git" ]
    if [ $FLAGS == "r" ]
    then
        python runtest.py --test-all    #tests for grab project are not named correctly and run from a py file
    elif [ $FLAGS == "rt" ]
    then
        TEST_FOLDER=${parts[3]}
        pytest $TEST_FOLDER
    elif [ $FLAGS == "t" ]
    then
        TEST_FOLDER=${parts[2]}
        pytest $TEST_FOLDER
    fi

    echo "\n--------------Test Time End--------------\n"
    timestamp
    echo "\n--------------Test Time End--------------\n"

    ((idx++))

done < "$URL_FILE"
