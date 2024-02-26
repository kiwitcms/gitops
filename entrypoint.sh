#!/bin/sh -l

echo "Hello $1"
time=$(date)

echo "**** DEBUG from inside the container"
export
echo "---- END -----"

echo "---- mounted filesystems"
mount
echo "----- end"

echo "++++ triggering event"
cat "$GITHUB_EVENT_PATH"
echo "+++++ END"

echo "++++ list $GITHUB_WORKSPACE"
ls -laR "$GITHUB_WORKSPACE"
echo "+++++ END"

echo "time=$time" >>"$GITHUB_OUTPUT"
