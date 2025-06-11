cmake_minimum_required(VERSION 3.10.0)
project(nycd VERSION 0.1.0 LANGUAGES C CXX)

add_executable(nycd 
Old_structures/main.cpp
Old_structures/doubly_linkedlist.cpp
Old_structures/hash_table.cpp
Old_structures/b_tree.cpp
Old_structures/skip_list.cpp
)

include(CTest)
enable_testing()

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
