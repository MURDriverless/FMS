#!/bin/bash

title1="tab 1"
title2="tab 2"
title3="tab 3"

# cmd1="source devel/setup.bash; rosrun serial_publisher serial_publisher"
cmd2="source devel/setup.bash; roslaunch mursim_gazebo slow_lap.launch"


# gnome-terminal --tab --title="$title1" -- bash -c "$cmd1; bash" &
gnome-terminal --tab --title="$title1" -- bash -c "$cmd2; bash"
