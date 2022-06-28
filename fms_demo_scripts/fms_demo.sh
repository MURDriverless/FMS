#!/bin/bash

title1="Sensors"
title2="System Analyzers"
title3="FMS"

cmd1="source devel/setup.bash; roslaunch sensors updaters.launch"
cmd2="source devel/setup.bash; roslaunch system_analyzers aggregator.launch"
cmd3="source devel/setup.bash; rosrun fms fms"

source devel/setup.bash

gnome-terminal --tab --title="$title1" -- bash -c "$cmd1; bash" &
gnome-terminal --tab --title="$title2" -- bash -c "$cmd2; bash" &
gnome-terminal --tab --title="$title3" -- bash -c "$cmd3; bash" &