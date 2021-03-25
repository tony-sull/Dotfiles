#!/bin/bash
# Get the current status of nordvpn
status=$(nordvpn status | grep -E 'Status: ' | awk -F': ' '{print $2}')

if [ $status == 'Connected' ]; then
    echo  $(nordvpn status | grep -E 'Country: ' | awk -F': ' '{print $2}')
else
    echo  Disconnected
fi

exit 0
