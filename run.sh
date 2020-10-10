#!/bin/bash

# Place your compile and execute script here.
# You can write any bash script that will run on standard linux machines.
# The below script will compile and execute the example.cpp program.

# compile the program in C++
#g++ -std=c++11 ./exampleCode/*.cpp -o sample

# execute the program and pass arguments if they exist
#./sample $1 $2

# Below is an example of how to call a Python script named
# myMain.py using python 3.6 on the campus Linux machines
# with a backup standard Python3 call for your convenience
/linux_apps/python-3.6.1/bin/python3 main.py $1 $2 || python3 main.py $1 $2
