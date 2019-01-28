cmake_minimum_required( VERSION 2.8.7 )

cmake_minimum_required(VERSION 2.8.12)
project(cmake_example)

add_subdirectory(pybind11)
pybind11_add_module(cmake_example src/pywincalc.cpp)

set( target_name WCEMultiOptics )

set(CMAKE_CXX_STANDARD 11)

project( ${target_name} )

set(GLOBAL_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)

# Sets global output directory for single configuration
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${GLOBAL_OUTPUT_PATH})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${GLOBAL_OUTPUT_PATH})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${GLOBAL_OUTPUT_PATH})

include(CMakeLists-Windows-CalcEngine.txt)

add_subdirectory(MultiLayerOpticsCMD)


if(MSVC)
	#This sets MT and MTd flags for Debug and Release modes for Windows-CalcEngine library
	target_compile_options(Windows-CalcEngine PRIVATE "/MD$<$<CONFIG:Debug>:d>")
endif()