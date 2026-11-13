cmake_minimum_required(VERSION 3.16)
project(vibematch_distance LANGUAGES CXX)

add_library(vibematch_distance SHARED distance.cpp)
target_compile_features(vibematch_distance PRIVATE cxx_std_17)
set_target_properties(vibematch_distance PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES
    OUTPUT_NAME vibematch_distance
)
