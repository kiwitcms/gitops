#!/bin/sh -l

echo "Hello $1"
time=$(date)

echo "**** DEBUG from inside the container"
export
echo "---- END -----"

echo "time=$time" >> $GITHUB_OUTPUT
