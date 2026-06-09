cmake_minimum_required(VERSION 3.12)

set( CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE ON )

set( target_name wincalcbindings )
project( ${target_name} )

set(JSON_BuildTests OFF CACHE BOOL "")
set(BUILD_WinCalc_tests OFF CACHE BOOL "")

include(CMakeLists-WinCalc.txt)
include(CMakeLists-pybind11.txt)

pybind11_add_module(${target_name}
    src/wincalcbindings.cpp
    src/bindings/gas_bindings.cpp
    src/bindings/pillar_bindings.cpp
    src/bindings/optical_parser_bindings.cpp
    src/bindings/standards_bindings.cpp
    src/bindings/product_data_bindings.cpp
    src/bindings/shading_bindings.cpp
    src/bindings/glazing_system_bindings.cpp
    src/bindings/thmx_bindings.cpp
    src/bindings/cma_bindings.cpp
    src/bindings/bsdf_bindings.cpp
    src/bindings/layers_bindings.cpp
)

target_compile_features(${target_name} PUBLIC cxx_std_17)
target_link_libraries( ${target_name} PRIVATE wincalc)

target_include_directories(${target_name}
    PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)
