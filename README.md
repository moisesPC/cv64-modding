In the project's root, place an unmodified Castlevania 64 (USA v1.0) ROM, and rename it to `cv64.z64`

1. Create a build directory, and access it: `mkdir build && cd build`

2. Run CMake to generate the build files: `cmake ..`

3. Build the project: `cmake --build . --target rom`

- To clean the project: `cmake --build . --target clean_all`