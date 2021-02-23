if (NOT EMSCRIPTEN AND NOT CMAKE_HOST_WIN32)
    find_program(CCACHE_PROGRAM ccache)
    if (CCACHE_PROGRAM)
        message(STATUS "Using ccache to increase compile speed: ${CCACHE_PROGRAM}")
        set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
    endif ()
endif()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif ()

#if (CMAKE_BUILD_TYPE STREQUAL Release)
#    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
#endif()

if (EMSCRIPTEN)
    string(APPEND CMAKE_CXX_FLAGS " -c -fexceptions --bind -s DISABLE_EXCEPTION_CATCHING=0 -s FILESYSTEM=0 -s USE_SDL=0 -s USE_SDL_IMAGE=0 -s USE_SDL_TTF=0 -s USE_SDL_NET=0 -s")
    string(APPEND CMAKE_C_FLAGS   " -c -fexceptions --bind -s DISABLE_EXCEPTION_CATCHING=0 -s FILESYSTEM=0 -s USE_SDL=0 -s USE_SDL_IMAGE=0 -s USE_SDL_TTF=0 -s USE_SDL_NET=0 -s")

    set(CMAKE_CXX_FLAGS_RELEASE "-Oz -DNDEBUG -flto")
    set(CMAKE_C_FLAGS_RELEASE   "-Oz -DNDEBUG -flto")

    set(CMAKE_CXX_FLAGS_DEBUG "-g4")
    set(CMAKE_C_FLAGS_DEBUG   "-g4")

    set(CMAKE_AR "emar")
    set(CMAKE_C_CREATE_STATIC_LIBRARY   "<CMAKE_AR> qc <TARGET> <LINK_FLAGS> <OBJECTS>")
    set(CMAKE_CXX_CREATE_STATIC_LIBRARY "<CMAKE_AR> qc <TARGET> <LINK_FLAGS> <OBJECTS>")
endif()
if (UNIX)
    string(APPEND CMAKE_C_FLAGS " -fvisibility=hidden")
    string(APPEND CMAKE_CXX_FLAGS " -fvisibility=hidden -fvisibility-inlines-hidden")
    if (BUILD_SELF_SUFFICIENT AND NOT EMSCRIPTEN)
        if (CMAKE_CXX_COMPILER_ID STREQUAL GNU)
            string(APPEND CMAKE_CXX_FLAGS " -static-libstdc++")
        elseif  (CMAKE_CXX_COMPILER_ID STREQUAL Clang)
            string(APPEND CMAKE_CXX_FLAGS " -Wall -Wextra -stdlib=libc++")
        endif()
    else ()
        list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
    endif ()
endif ()

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if (ENABLE_TESTS)
    enable_testing()
endif ()

if (BUILD_SELF_SUFFICIENT AND NOT EMSCRIPTEN)
    include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/conan.cmake)
endif ()

find_package(Threads REQUIRED)

set(DIST_DIRECTORY ${CMAKE_SOURCE_DIR}/dist)
set(INDIGO_NATIVE_LIBS_DIRECTORY ${DIST_DIRECTORY}/lib)

string(TOLOWER ${CMAKE_SYSTEM_NAME} CMAKE_SYSTEM_NAME_LOWER)