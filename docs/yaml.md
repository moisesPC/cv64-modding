# YAML
A YAML file (named `config.yml`, and located in the root of the repository) is used to assist on the creation and insertion of code and assests.

This file has the following structure (all numbers are written in hexadecimal):

## objects
Allows you to change different settings for objects.

Note that, at the moment, it isn't possible to add objects, so the ons you create must replace pre-existing ones from the game.

### Example
```yaml
objects:
  - name: obj_test
    raw_id: 0x1F
    entrypoint:
      build/src/objects/obj_test/obj_test_overlay.bin.elf: objTest_entrypoint
    files_info:
      - { 0x09, 0x00001000 }
    files_info_ptr: 0xA3CA0
```

### name
The name of the object

### raw_id
The raw ID of the object. This is, the ID of the object without the object flags, such as 0x2000 (map overlay). 

The range of IDs goes from 1 to 0x22A, both inclusive.

### entrypoint
The VRAM address of the function that serves as an entrypoint for this object's code. You can specify this in two ways:
* By directly inputting the VRAM address:

```yaml
entrypoint: 0x0F000000
```

* By retrieving the address automatically from an ELF file:

```yaml
entrypoint: path/to/elf/file: function_name
```

### files_info
This defines a list of file IDs that are associated with the object. These files are loaded into memory when the object spawns, and usually contain code and assets used by the object.

Each entry is made by:
* a Nisintema-Ichigo table file ID.
* an alignment value for said file when it's loaded into memory.

```yaml
files_info:
      - { FILE_1_ID, FILE_1_ALIGNMENT }
      - { FILE_2_ID, FILE_2_ALIGNMENT }
      ...
```

### files_info_ptr
This is the ROM address where the `files_info` array will be placed at.

At the moment, the ROM address specified can only be an address inside the `main` segment (ROM addresses going from 0x1060 to 0xA8420)

This is because the VRAM address is calculated automatically based on the VRAM address associated to the main segment (0x80000460)

```yaml
files_info_ptr: 0xA3CA0
```

## binary_files
Allows specified files to be compiled, linked and stripped into binaries, to then inject them into the ROM.

This can be any file, including source code files, assets, binaries, etc.

### Example
```yaml
binary_files:
  - name: src/static/static_segment
    files: 
      - "src/static/static_segment.c"
    vram: 0x803FB270  # SEC_STATIC_RAM
    rom: 0x00BB2D88   # SEC_STATIC_ROM
    is_ni_file: false

  - name: src/objects/obj_test/obj_test_overlay
    files: 
      - "src/objects/obj_test/obj_test.c"
    vram: 0x0F000000
    follows-rom: src/static/static_segment
    is_ni_file: true
    file_id: 0x09

  - name: assets/custom_test_grid/custom_test_grid
    files: 
      - "assets/custom_test_grid/custom_test_grid.c"
    vram: 0x06000000
    follows-rom: src/objects/obj_test/obj_test_overlay
    is_ni_file: true
    file_id: 0x5C
```

### name
The name of the final, compiled file (without the file extension).

This is also the directory (relative to `build/`) where the build artifacts will be located at.

### files
A list of files that will be included into the final binary. For source code files, all of the files specified on this param will be combined into one single binary file after building.

### rom
ROM address where the final binary file will be injected at.

### follows-rom
This param makes it so that the file will be injected in ROM right after another.

For example:
```yaml
name: assets/custom_test_grid/custom_test_grid
    follows-rom: src/objects/obj_test/obj_test_overlay
```
This will place the file `assets/custom_test_grid/custom_test_grid` right after the file `src/objects/obj_test/obj_test_overlay` in the ROM.

### vram
Entrypoint VRAM address for the file. This dictates the address where the final file should be loaded in VRAM in order to make it work properly.

### is_ni_file
If `true`, the file will be injected as a Nisitenma-Ichigo file, which is compressed and has a file ID associated to it.

### file_id
This is the file ID in the Nisitenma-Ichigo table, assuming that `is_ni_file` is set to `true`. Note that file IDs range from 1 to 0xFE, both inclusive.

### dont_compile
If set to `true`, the file won't be compiled, and will just be injected into the ROM.

## binary_files
Changes the settings associated to the game's maps.

### Example
```yaml
maps:
  - name: build/assets/custom_test_grid/custom_test_grid
    id: 0x1D
    file_id: 0x5C
    assets_file_elf: build/assets/custom_test_grid/custom_test_grid.bin.elf
    actor_list: actor_list
    music_id: 0x11
    has_skybox: false
    load_pickable_item_assets: true
    file_buffer_extra_size: 0x1800
```

### name (TODO: change this parameter's name)
This is the path to the `build/` directory where the map binaries will be located at. 

### id
The ID of the map you wanna change its settings to. Ranges from 0 to 0x1D, both inclusive.

### file_id
The file ID for  the map's assets in the Nisitenma-Ichigo table.

### assets_file_elf
Path to the map assets ELF file. This is used to get the VRAM address of some specific elements from the assets file.

### actor_list
This is the symbol in the map assets's source code file that contains the actor list. Make sure it's named exactly like in the source code file, as this is used to retrieve the VRAM address of the actor list from the `assets_file_elf` ELF file.

#### Example
Actor list definition in the map assets's source code file:
```c
const ActorConfig my_custom_map_actor_list[] = {
    {{-100, 0,  -70},  MOD_OBJ_TEST, 0,  0, 0,  01, 00},
    END_ACTOR_LIST
};
```
In the YAML:
```yaml
actor_list: my_custom_map_actor_list
```

### music_id
The sound ID that will play on the background when in the map. If you OR this value with 0x8000, you will instead silence the specified sound ID.

### has_skybox
If set to `true`, the skybox assets will be loaded when spawning the map. Note that this won't make the skybox itself appear.

The object ID for the skybox must be specified in the map's non-priximity actor list in order to make the skybox appear.

### load_pickable_item_assets
If set to `true`, the game will load the assets file that contains the pickable item models. This is required if any entities in your map are able to spawn the `Interactables` object.

### (Optional) file_buffer_extra_size
When the map assets file is allocated into memory, the game adds a bit more size to the total allocated space for said file to ensure we don't run out of memory somehow.

This param specifies the size in bytes for this extra space. If you think you may be running out of memory when loading the map, try changing this param.
