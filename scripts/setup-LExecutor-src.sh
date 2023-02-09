#!/usr/bin/bash

ROOT_DIR=$(pwd)

#update the LExecutor source from the forked repo.
if [[ ! -d Lexecutor ]]
then
    git clone https://github.com/michaelpradel/LExecutor.git $ROOT_DIR/LExecutor
    cd $ROOT_DIR/LExecutor
else
    cd $ROOT_DIR/LExecutor
    git pull
fi

