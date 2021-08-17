cmake_minimum_required(VERSION 3.8)

set( CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE ON )

set( target_name pywincalc )
project( ${target_name} )

set(JSON_BuildTests OFF CACHE BOOL "")
set(BUILD_WinCalc_tests OFF CACHE BOOL "")

include(CMakeLists-WinCalc.txt)
include(CMakeLists-pybind11.txt)

pybind11_add_module(${target_name} src/pywincalc.cpp)

target_compile_features(${target_name} PUBLIC cxx_std_17)
target_link_libraries( ${target_name} PRIVATE wincalc)

target_include_directories(${target_name}
    PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)