#!/bin/bash

# This script is used to clean unnecessary generated files/folders.

remove_eggs() {
  # The directory path is sent as the first argument
  cd $1
  rm -rf build
  rm -rf *.egg-info
  rm -rf dist
  cd ..
}
remove_eggs_venv_lib_core(){
  cd .venv
  cd Lib
  cd site-packages
  rm -rf $1-0.1-py3.9.egg
  cd ..
  cd ..
  cd ..

}
remove_eggs_venv_lib(){
  cd .venv
  cd Lib
  cd site-packages
  rm $1-0.1-py3.9.egg
  cd ..
  cd ..
  cd ..

}


# remove build files from venv
remove_eggs_venv_lib_core core
remove_eggs_venv_lib json_loader
#remove_eggs_venv_lib visualizer_simple


# remove build files from components
remove_eggs D3Core
#remove_eggs visualizer_simple
remove_eggs loader_json

