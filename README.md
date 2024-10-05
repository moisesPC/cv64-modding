In the project's root, place an unmodified Castlevania 64 (USA v1.0) ROM, and rename it to `cv64.z64`

Run the following command to build the ROM: `cmake -S . -B build && cmake --build build --target rom`

Use the following command to clean: `cmake --build build --target clean_all`