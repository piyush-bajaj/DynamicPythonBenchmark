#!/usr/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}

echo "Starting the testing of python projects already installed"

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
    cd "$PROJ_DIR"
else
    echo "Please perform setup install first"
    exit
fi

WORK_DIR=$(pwd)

#run a while loop to activate vm for all projects and execute tests
idx=1
while read line
do
    echo $line

    parts=($line)
    URL=${parts[0]}
    FLAGS=${parts[1]}

    #change to working directory
    cd $WORK_DIR
    #go into the project directory
    cd "project$idx"
    #activate virtual env
    if [[ $1 == "ubuntu" ]]
    then
        source vm/bin/activate
    elif [[ $1 == "docker" ]]
    then
        source vm/local/bin/activate
    fi

    #run tests
    if [[ $2 == "tests" ]]
    then
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

    #instrument code for dynapyt analysis
    elif [[ $2 == "dynapyt.instrument" ]]
    then
		echo "Run DynaPyt instrumentation"
		#python -m dynapyt.run_instrumentation --directory ./test/PythonRepos/rich --analysis $3
    elif [[ $2 == "dynapyt.analysis" ]]
    then
		echo "Run DynaPyt Analysis"
		#python -m dynapyt.run_analysis --entry run_all_tests.py --analysis $3
	elif [[ $2 == "dynapyt" ]]
		echo "Run Dynapyt instrumentation and analysis"
		#python -m dynapyt.run_all --directory ./test/PythonRepos/rich --entry ./test/PythonRepos/rich/run_all_tests.py --analysis TraceAll
    fi

    ((idx++))
	deactivate

done < "$URL_FILE"
