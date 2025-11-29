cmake_minimum_required(VERSION 3.10)
project(SecureVoteSystem VERSION 2.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set output directory for executables
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../bin)

# Include directories
include_directories(include)

# Find all source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Create executable
add_executable(SecureVoteSystem main.cpp ${SOURCES})

# Add threading support
find_package(Threads REQUIRED)
target_link_libraries(SecureVoteSystem Threads::Threads)

# Set output name
set_target_properties(SecureVoteSystem PROPERTIES OUTPUT_NAME "SecureVoteSystem")
