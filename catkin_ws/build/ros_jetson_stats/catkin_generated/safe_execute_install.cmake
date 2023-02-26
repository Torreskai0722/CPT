execute_process(COMMAND "/home/mobilitylab/catkin_ws/build/ros_jetson_stats/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/mobilitylab/catkin_ws/build/ros_jetson_stats/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
