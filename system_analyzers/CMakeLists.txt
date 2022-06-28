cmake_minimum_required(VERSION 3.0.2)
project(system_analyzers)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  diagnostic_aggregator
  diagnostic_msgs
  pluginlib
  roscpp
  xmlrpcpp
  mur_common
)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES system_analyzers
 CATKIN_DEPENDS diagnostic_aggregator diagnostic_msgs pluginlib roscpp xmlrpcpp mur_common
)

###########
## Build ##
###########

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

file(GLOB_RECURSE ANALYZER_SRCS src/analyzer/*.cpp)
add_library(${PROJECT_NAME} ${ANALYZER_SRCS})
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES})
