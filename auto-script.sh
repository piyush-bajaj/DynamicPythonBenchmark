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


