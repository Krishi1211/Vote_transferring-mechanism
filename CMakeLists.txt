cmake_minimum_required(VERSION 3.10)
project(SecureVoteSystem VERSION 1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(include)

# Find all source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Create executable
add_executable(SecureVoteSystem ${SOURCES})

# Add threading support if needed
find_package(Threads REQUIRED)
target_link_libraries(SecureVoteSystem Threads::Threads)
