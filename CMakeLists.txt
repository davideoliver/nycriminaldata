cmake_minimum_required(VERSION 3.10.0)
project(nycd VERSION 0.1.0 LANGUAGES C CXX)

add_executable(nycd 
src/main.cpp
src/doubly_linkedlist.cpp
src/hash_table.cpp
src/b_tree.cpp
)

include(CTest)
enable_testing()

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
