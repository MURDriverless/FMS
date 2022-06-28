#!/bin/bash

cmd="source devel/setup.bash; rosrun serial_publisher serial_publisher"
gnome-terminal --tab --title="serial" -- bash -c "$cmd; bash" &