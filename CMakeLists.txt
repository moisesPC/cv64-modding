cmake_minimum_required(VERSION 3.10)
project(cv64_modding)

# Set directories
set(SRC_DIR src)
set(ASM_DIR asm)
set(BUILD_DIR build)
set(SEC_CUSTOM_SRC_DIR ${SRC_DIR}/sec_custom)
set(ASM_N64_WRAP ${BUILD_DIR}/armips_n64_wrapper.asm)
set(ROM_IN cv64.z64)
set(ROM_OUT cv64_mod.z64)

# Set tools
set(CMAKE_C_COMPILER ${CMAKE_SOURCE_DIR}/tools/n64chain/bin/mips64-elf-gcc)
set(CMAKE_AR ${CMAKE_SOURCE_DIR}/tools/n64chain/bin/mips64-elf-ar)
set(AS ${CMAKE_SOURCE_DIR}/tools/armips/armips)
set(CALC_CHECKSUM ${CMAKE_SOURCE_DIR}/tools/calcchecksum.py)
set(PYTHON python3)

# Include directories
include_directories(include include/ultra64 include/game)

# Compiler flags
set(CMAKE_C_FLAGS "-Wall -O3 -mtune=vr4300 -march=vr4300 -mabi=32 -fomit-frame-pointer -G0 -Wno-comment")

# Locate all .c files within SEC_CUSTOM_SRC_DIR
file(GLOB_RECURSE SEC_CUSTOM_C_FILES ${SEC_CUSTOM_SRC_DIR}/*.c)

# Create object files
add_library(sec_custom_objects OBJECT ${SEC_CUSTOM_C_FILES})

# Create build directory if it doesn't exist
file(MAKE_DIRECTORY ${BUILD_DIR})

# Custom command to generate the wrapper ASM file
add_custom_command(
    OUTPUT ${ASM_N64_WRAP}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${BUILD_DIR}
    COMMAND ${CMAKE_COMMAND} -E echo ".n64" > ${ASM_N64_WRAP}
    COMMAND ${CMAKE_COMMAND} -E echo ".open \\\"../${ROM_IN}\\\", \\\"../${ROM_OUT}\\\", 0" >> ${ASM_N64_WRAP}
    COMMAND ${CMAKE_COMMAND} -E echo ".include \\\"../${ASM_DIR}/main.asm\\\"" >> ${ASM_N64_WRAP}
    COMMAND ${CMAKE_COMMAND} -E echo ".close" >> ${ASM_N64_WRAP}
    COMMENT "Generating armips N64 wrapper"
)

# Create the archive
add_custom_command(
    OUTPUT ${BUILD_DIR}/sec_custom.a
    COMMAND ${CMAKE_AR} rcs ${BUILD_DIR}/sec_custom.a $<TARGET_OBJECTS:sec_custom_objects>
    DEPENDS sec_custom_objects
    COMMENT "Creating sec_custom.a archive"
)

# Generate the final ROM
add_custom_command(
    OUTPUT ${CMAKE_SOURCE_DIR}/${ROM_OUT}
    COMMAND ${AS} ${ASM_N64_WRAP} -root .
    COMMAND ${PYTHON} ${CALC_CHECKSUM} ${CMAKE_SOURCE_DIR}/${ROM_OUT}
    DEPENDS ${BUILD_DIR}/sec_custom.a ${ROM_IN} ${ASM_N64_WRAP}
    COMMENT "Generating final ROM: ${ROM_OUT}"
)

# Add custom target for the ROM
add_custom_target(rom ALL DEPENDS ${CMAKE_SOURCE_DIR}/${ROM_OUT})

# Rename the clean target to avoid conflicts
add_custom_target(clean_all
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${BUILD_DIR}
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_SOURCE_DIR}/${ROM_OUT}
    COMMENT "Cleaning up build directories and files"
)
