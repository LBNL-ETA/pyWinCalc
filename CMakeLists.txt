cmake_minimum_required(VERSION 2.8.12)

set( target_name pywincalc )
project( ${target_name} )

set( JSON_BuildTests OFF CACHE BOOL "")

include(CMakeLists-WinCalc.txt)

add_subdirectory(pybind11)
pybind11_add_module(${target_name} src/pywincalc.cpp)

target_link_libraries( ${target_name} PRIVATE wincalc)

