#!/usr/bin/bash

ROOT_DIR=$(pwd)

#update the dynapyt source from the forked repo.
if [[ ! -d DynaPyt ]]
then
    git clone https://github.com/piyush-bajaj/DynaPyt.git $ROOT_DIR/DynaPyt
else
    git pull
fi

cd $ROOT_DIR/DynaPyt

#checkout the lastest code and analysis from the custom branch
git checkout piyush-bajaj-dypybench-analysis
