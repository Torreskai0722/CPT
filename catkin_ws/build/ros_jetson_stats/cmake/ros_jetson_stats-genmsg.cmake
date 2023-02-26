# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "ros_jetson_stats: 0 messages, 3 services")

set(MSG_I_FLAGS "-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(ros_jetson_stats_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv" NAME_WE)
add_custom_target(_ros_jetson_stats_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_jetson_stats" "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv" ""
)

get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv" NAME_WE)
add_custom_target(_ros_jetson_stats_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_jetson_stats" "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv" ""
)

get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv" NAME_WE)
add_custom_target(_ros_jetson_stats_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_jetson_stats" "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_cpp(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_cpp(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_jetson_stats
)

### Generating Module File
_generate_module_cpp(ros_jetson_stats
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_jetson_stats
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(ros_jetson_stats_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(ros_jetson_stats_generate_messages ros_jetson_stats_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_cpp _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_cpp _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_cpp _ros_jetson_stats_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_jetson_stats_gencpp)
add_dependencies(ros_jetson_stats_gencpp ros_jetson_stats_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_jetson_stats_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services
_generate_srv_eus(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_eus(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_eus(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_jetson_stats
)

### Generating Module File
_generate_module_eus(ros_jetson_stats
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_jetson_stats
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(ros_jetson_stats_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(ros_jetson_stats_generate_messages ros_jetson_stats_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_eus _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_eus _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_eus _ros_jetson_stats_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_jetson_stats_geneus)
add_dependencies(ros_jetson_stats_geneus ros_jetson_stats_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_jetson_stats_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_lisp(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_lisp(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_jetson_stats
)

### Generating Module File
_generate_module_lisp(ros_jetson_stats
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_jetson_stats
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(ros_jetson_stats_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(ros_jetson_stats_generate_messages ros_jetson_stats_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_lisp _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_lisp _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_lisp _ros_jetson_stats_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_jetson_stats_genlisp)
add_dependencies(ros_jetson_stats_genlisp ros_jetson_stats_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_jetson_stats_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages

### Generating Services
_generate_srv_nodejs(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_nodejs(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_nodejs(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_jetson_stats
)

### Generating Module File
_generate_module_nodejs(ros_jetson_stats
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_jetson_stats
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(ros_jetson_stats_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(ros_jetson_stats_generate_messages ros_jetson_stats_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_nodejs _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_nodejs _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_nodejs _ros_jetson_stats_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_jetson_stats_gennodejs)
add_dependencies(ros_jetson_stats_gennodejs ros_jetson_stats_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_jetson_stats_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_py(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats
)
_generate_srv_py(ros_jetson_stats
  "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats
)

### Generating Module File
_generate_module_py(ros_jetson_stats
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(ros_jetson_stats_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(ros_jetson_stats_generate_messages ros_jetson_stats_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/fan.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_py _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/jetson_clocks.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_py _ros_jetson_stats_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/mobilitylab/catkin_ws/src/ros_jetson_stats/srv/nvpmodel.srv" NAME_WE)
add_dependencies(ros_jetson_stats_generate_messages_py _ros_jetson_stats_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_jetson_stats_genpy)
add_dependencies(ros_jetson_stats_genpy ros_jetson_stats_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_jetson_stats_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_jetson_stats)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_jetson_stats
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(ros_jetson_stats_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_jetson_stats)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_jetson_stats
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(ros_jetson_stats_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_jetson_stats)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_jetson_stats
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(ros_jetson_stats_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_jetson_stats)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_jetson_stats
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(ros_jetson_stats_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats
    DESTINATION ${genpy_INSTALL_DIR}
    # skip all init files
    PATTERN "__init__.py" EXCLUDE
    PATTERN "__init__.pyc" EXCLUDE
  )
  # install init files which are not in the root folder of the generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats
    DESTINATION ${genpy_INSTALL_DIR}
    FILES_MATCHING
    REGEX "${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_jetson_stats/.+/__init__.pyc?$"
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(ros_jetson_stats_generate_messages_py std_msgs_generate_messages_py)
endif()
