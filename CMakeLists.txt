cmake_minimum_required(VERSION 3.27)
project(DonkeyKong LANGUAGES CXX)

# Basic project configuration
set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES ON)

# Prevent in-source builds
if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not allowed.")
endif()

# Project directory structure
set(PROJECT_SRC_DIR ${PROJECT_SOURCE_DIR}/src)
set(PROJECT_INC_DIR ${PROJECT_SOURCE_DIR}/include)

# Output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# C++ standard settings
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build type and compiler flags
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_DEBUG_INIT "-Wall")
set(CMAKE_CXX_FLAGS_RELEASE_INIT "-Wall")

# Project definitions and includes
add_definitions(-DPROJECTPATH=\"${PROJECT_SOURCE_DIR}\")
include_directories(${PROJECT_INC_DIR})

# Source files
file(GLOB SOURCES "${PROJECT_SRC_DIR}/*.cpp")
list(REMOVE_ITEM SOURCES "${PROJECT_SRC_DIR}/Wrapper.cpp")

# Fetch and include dependencies
include(FetchContent)

# SFML dependency
FetchContent_Declare(
    SFML
    GIT_REPOSITORY https://github.com/SFML/SFML.git
    GIT_TAG 3.0.1
    GIT_SHALLOW ON
    EXCLUDE_FROM_ALL
    SYSTEM
)
FetchContent_MakeAvailable(SFML)

# JSON dependency (use single-include ZIP to avoid long path issues in full repo)
FetchContent_Declare(
    json
    URL https://github.com/nlohmann/json/releases/download/v3.11.2/include.zip
    URL_HASH SHA256=e5c7a9f49a16814be27e4ed0ee900ecd0092bfb7dbfca65b5a421b774dccaaed
)
FetchContent_Populate(json)

add_library(nlohmann_json INTERFACE)
target_include_directories(nlohmann_json INTERFACE ${json_SOURCE_DIR}/single_include)
add_library(nlohmann_json::nlohmann_json ALIAS nlohmann_json)

# Pybind11 dependency
set(PYBIND11_FINDPYTHON ON)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.12.0
)
FetchContent_MakeAvailable(pybind11)

# Main library
add_library(DonkeyKongLib ${SOURCES})
target_link_libraries(DonkeyKongLib PUBLIC 
    SFML::Graphics 
    nlohmann_json::nlohmann_json
)

# Main executable
add_executable(DonkeyKong Main.cpp)
target_link_libraries(DonkeyKong PRIVATE DonkeyKongLib)

# Python module
pybind11_add_module(DonkeyKongPy src/Wrapper.cpp)
target_link_libraries(DonkeyKongPy PRIVATE 
    DonkeyKongLib 
    pybind11::module
)

# Python module properties
set_target_properties(DonkeyKongPy PROPERTIES
    OUTPUT_NAME "DonkeyKongPy"
    SUFFIX ".pyd"
)