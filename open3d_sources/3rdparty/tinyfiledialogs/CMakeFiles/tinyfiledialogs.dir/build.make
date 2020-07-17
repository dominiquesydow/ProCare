# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

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
CMAKE_COMMAND = /usr/bin/cmake3

# The command to remove a file.
RM = /usr/bin/cmake3 -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /opt/open3d/Open3D

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /opt/open3d/Open3D

# Include any dependencies generated for this target.
include 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/depend.make

# Include the progress variables for this target.
include 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/progress.make

# Include the compile flags for this target's objects.
include 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/flags.make

3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.o: 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/flags.make
3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.o: 3rdparty/tinyfiledialogs/tinyfiledialogs.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/opt/open3d/Open3D/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.o"
	cd /opt/open3d/Open3D/3rdparty/tinyfiledialogs && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.o   -c /opt/open3d/Open3D/3rdparty/tinyfiledialogs/tinyfiledialogs.c

3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.i"
	cd /opt/open3d/Open3D/3rdparty/tinyfiledialogs && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /opt/open3d/Open3D/3rdparty/tinyfiledialogs/tinyfiledialogs.c > CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.i

3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.s"
	cd /opt/open3d/Open3D/3rdparty/tinyfiledialogs && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /opt/open3d/Open3D/3rdparty/tinyfiledialogs/tinyfiledialogs.c -o CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.s

# Object files for target tinyfiledialogs
tinyfiledialogs_OBJECTS = \
"CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.o"

# External object files for target tinyfiledialogs
tinyfiledialogs_EXTERNAL_OBJECTS =

lib/libtinyfiledialogs.a: 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/tinyfiledialogs.c.o
lib/libtinyfiledialogs.a: 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/build.make
lib/libtinyfiledialogs.a: 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/opt/open3d/Open3D/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C static library ../../lib/libtinyfiledialogs.a"
	cd /opt/open3d/Open3D/3rdparty/tinyfiledialogs && $(CMAKE_COMMAND) -P CMakeFiles/tinyfiledialogs.dir/cmake_clean_target.cmake
	cd /opt/open3d/Open3D/3rdparty/tinyfiledialogs && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tinyfiledialogs.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/build: lib/libtinyfiledialogs.a

.PHONY : 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/build

3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/clean:
	cd /opt/open3d/Open3D/3rdparty/tinyfiledialogs && $(CMAKE_COMMAND) -P CMakeFiles/tinyfiledialogs.dir/cmake_clean.cmake
.PHONY : 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/clean

3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/depend:
	cd /opt/open3d/Open3D && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /opt/open3d/Open3D /opt/open3d/Open3D/3rdparty/tinyfiledialogs /opt/open3d/Open3D /opt/open3d/Open3D/3rdparty/tinyfiledialogs /opt/open3d/Open3D/3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : 3rdparty/tinyfiledialogs/CMakeFiles/tinyfiledialogs.dir/depend
