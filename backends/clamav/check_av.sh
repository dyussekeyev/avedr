#!/bin/bash
# Check if clamd is running
if ! pgrep -x "clamd" > /dev/null
then
    echo "clamd is not running. Restarting clamd..."
    /usr/sbin/clamd &
else
    echo "clamd is running."
fi
