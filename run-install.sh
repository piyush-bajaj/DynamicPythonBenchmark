#!/usr/bin/bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%dT%T.%3N%z" # current time
}
echo "Starting the installation, setup and running of python projects and their test suites"

#root directory
ROOT_DIR=$(pwd)

echo "Please provide the complete location of url file"
#read URL_FILE
URL_FILE=$ROOT_DIR/github-url.txt

# Create project folder to keep all the projects together inside one parent folder
PROJ_DIR=Project
#if folder already present, then cd to the folder
if [ -d "$PROJ_DIR" ]
then
    cd "$PROJ_DIR" 
fi

WORK_DIR=$(pwd)

#run a while loop to create vm for all projects
idx=1
while read line
do
    echo $line

    parts=($line)
    URL=${parts[0]}
    FLAGS=${parts[1]}

    echo "$idx"
    if [[ ! -d "$WORK_DIR/project$idx" ]]
    then
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

        #install using pip install . 
        echo "Running pip install ."
        pip install .

        #install using setup.py file or requirements.txt
        # if [ -e setup.py ]
        # then
        #     echo "Running setup install"
        #     python setup.py install
        # else
        #     echo "Running pip install ."
        #     pip install .
        #elif [ -e requirements.txt ]
        #then
        #    find ./ -name '*requirements.txt' -or -name 'requirements*.txt' -exec pip install -r {} \;
        #    pip install -r requirements.txt
        #else
        #    echo "No setup.py file or requirements.txt found"
        # fi

        if [[ $FLAGS == "r" || $FLAGS == "rt" ]]
        then
            REQ_FILE=${parts[2]}
            if [[ $URL == "https://github.com/spotify/dh-virtualenv.git" ]]
            then
                sed -i.bak '0,/invoke==0.13.0/s//invoke/' dev-requirements.txt  #fix for dependency conflict issue
            # elif [[ $URL == "https://github.com/flask-admin/flask-admin.git" ]]
            # then
            #     sed -i.bak '0,/psycopg2/s//\n/' requirements-dev.txt #fix for dependency issue
            fi
            echo "Running pip install requirements"
            pip install -r $REQ_FILE
        fi

        #some projects need extra requirements for running test suites
        if [[ $URL == "https://github.com/psf/black.git" ]]
        then
            pip install aiohttp #required for running tests
        elif [[ $URL == "https://github.com/errbotio/errbot.git" ]]
        then
            pip install mock #required for running tests
        elif [[ $URL == "https://github.com/PyFilesystem/pyfilesystem2.git" ]]
        then
            pip install parameterized pyftpdlib #required for running tests
        elif [[ $URL == "https://github.com/geopy/geopy.git" ]]
        then
            pip install docutils #required for running tests
        elif [[ $URL == "https://github.com/gawel/pyquery.git" ]]
        then
            pip install webtest #required for running tests
        elif [[ $URL == "https://github.com/elastic/elasticsearch-dsl-py.git" ]]
        then
            pip install pytz #required for running tests
        elif [[ $URL == "https://github.com/marshmallow-code/marshmallow.git" ]]
        then
            pip install pytz simplejson #required for running tests
        elif [[ $URL == "https://github.com/pytest-dev/pytest.git" ]]
        then
            pip install hypothesis xmlschema #required for running tests
        fi

        #install pytest library
        pip install pytest

        #install dynapyt
        pip install dynapyt libcst pytest pytest-xdist aiopg

        echo "\n--------------Setup End Time--------------\n"
        timestamp
        echo "\n--------------Setup End Time--------------\n"

        deactivate
    else
        echo "Project exists"
    fi
    ((idx++))
done < "$URL_FILE"