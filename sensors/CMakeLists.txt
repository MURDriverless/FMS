cmake_minimum_required(VERSION 3.0.2)
project(sensors)

find_package(catkin REQUIRED COMPONENTS
  diagnostic_updater
  rospy
  std_msgs
)

catkin_python_setup()
catkin_package()

catkin_install_python(PROGRAMS scripts/gps_driver scripts/slam_driver
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})