# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/mobilitylab/Pangolin

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/mobilitylab/Pangolin/build

# Utility rule file for install-mime-info.

# Include the progress variables for this target.
include tools/VideoViewer/CMakeFiles/install-mime-info.dir/progress.make

tools/VideoViewer/CMakeFiles/install-mime-info: tools/VideoViewer/VideoViewer
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && mkdir -p /root/.local/share/mime/packages/
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && mkdir -p /root/.local/share/applications/
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && mkdir -p /root/.local/share/icons/hicolor/scalable/mimetypes/
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && cp /home/mobilitylab/Pangolin/tools/VideoViewer/application-x-pango.xml /root/.local/share/mime/packages/
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && cp /home/mobilitylab/Pangolin/tools/VideoViewer/application-x-pango.svg /root/.local/share/icons/hicolor/scalable/mimetypes/
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && cp /home/mobilitylab/Pangolin/build/tools/VideoViewer/pango.desktop /root/.local/share/applications/
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && gtk-update-icon-cache /root/.local/share/icons/hicolor -f -t
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && update-mime-database /root/.local/share/mime
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && update-desktop-database /root/.local/share/applications

install-mime-info: tools/VideoViewer/CMakeFiles/install-mime-info
install-mime-info: tools/VideoViewer/CMakeFiles/install-mime-info.dir/build.make

.PHONY : install-mime-info

# Rule to build all files generated by this target.
tools/VideoViewer/CMakeFiles/install-mime-info.dir/build: install-mime-info

.PHONY : tools/VideoViewer/CMakeFiles/install-mime-info.dir/build

tools/VideoViewer/CMakeFiles/install-mime-info.dir/clean:
	cd /home/mobilitylab/Pangolin/build/tools/VideoViewer && $(CMAKE_COMMAND) -P CMakeFiles/install-mime-info.dir/cmake_clean.cmake
.PHONY : tools/VideoViewer/CMakeFiles/install-mime-info.dir/clean

tools/VideoViewer/CMakeFiles/install-mime-info.dir/depend:
	cd /home/mobilitylab/Pangolin/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/mobilitylab/Pangolin /home/mobilitylab/Pangolin/tools/VideoViewer /home/mobilitylab/Pangolin/build /home/mobilitylab/Pangolin/build/tools/VideoViewer /home/mobilitylab/Pangolin/build/tools/VideoViewer/CMakeFiles/install-mime-info.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/VideoViewer/CMakeFiles/install-mime-info.dir/depend

