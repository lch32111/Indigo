if (BUILD_STANDALONE)
    # InChI don't have a Conan package yet
    add_subdirectory(inchi)
    add_subdirectory(rapidjson)
    add_subdirectory(zlib)
    add_subdirectory(tinyxml2)
endif()
if (BUILD_INDIGO OR BUILD_INDIGO_UTILS)
    if (BUILD_STANDALONE)
        add_subdirectory(libpng)
        add_subdirectory(pixman)
        if (EMSCRIPTEN)
            add_subdirectory(cairo-wasm)
        else()
            add_subdirectory(cairo)

            # @chanhaeng.lee : added for freetype for windows
            if(WIN32)
                # ignore freetype install
                set(SKIP_INSTALL_HEADERS ON CACHE BOOL "FreeType Ignore Install Headers")
                set(SKIP_INSTALL_ALL ON CACHE BOOL "FreeType Ignore Install All")
                add_subdirectory(freetype)
                add_dependencies(cairo freetype)
            endif()
        endif()
    endif()
endif ()
if (EMSCRIPTEN)
    # Required for base64 encoding
    add_subdirectory(cppcodec)
endif()
if (ENABLE_TESTS)
    add_subdirectory(googletest)
endif()

add_subdirectory(object_threadsafe)

