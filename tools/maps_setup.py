import os
import yaml
import subprocess

# Constants
ROM_PATH = "output_mod.z64"
ACTOR_LIST_POINTERS_OFFSET = 0x10D978  # Offset in ROM for actor list pointers
MAP_FILE_INFO_OFFSET = 0x104B60  # Offset in ROM for map_file_info array
MAP_FILE_INFO_SIZE = 12  # Size of map_file_info struct (4 + 4 + 2 + 1 + 1)

def get_vram_address_from_elf(elf_path, symbol_name):
    """Retrieve VRAM address from an ELF file using readelf."""
    try:
        result = subprocess.run(
            ['readelf', '-s', elf_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.splitlines():
            if symbol_name in line:
                parts = line.split()
                vram_address = int(parts[1], 16)
                return vram_address

    except subprocess.CalledProcessError as e:
        print(f"Error reading ELF file: {e}")
    
    return None

def inject_vram_address_into_rom(vram_address, map_id):
    """Inject VRAM address into ROM at specified offset."""
    with open(ROM_PATH, 'r+b') as rom_file:
        rom_file.seek(ACTOR_LIST_POINTERS_OFFSET + (map_id * 4))
        rom_file.write(vram_address.to_bytes(4, byteorder='big'))

def write_map_info_to_rom(map_id, file_id, vram_file_end, load_pickable_item_assets, has_skybox):
    """Write map_file_info struct to ROM at specified offset."""
    offset = MAP_FILE_INFO_OFFSET + (map_id * MAP_FILE_INFO_SIZE)
    
    vram_file_start = 0x06000000
    items_byte = 0x1E if load_pickable_item_assets else 0x00
    skybox_byte = 0x1F if has_skybox else 0x00
    
    data_to_write = bytearray()
    data_to_write.extend(vram_file_start.to_bytes(4, byteorder='big'))
    data_to_write.extend(vram_file_end.to_bytes(4, byteorder='big'))
    data_to_write.extend(file_id.to_bytes(2, byteorder='big'))
    data_to_write.append(items_byte)
    data_to_write.append(skybox_byte)

    with open(ROM_PATH, 'r+b') as rom_file:
        rom_file.seek(offset)
        rom_file.write(data_to_write)

def main():
    with open('config.yml', 'r') as yml_file:
        config = yaml.safe_load(yml_file)

    for map_entry in config.get('maps', []):
        name = map_entry.get('name')
        
        # Handle both integer and string cases for 'id'
        map_id_raw = map_entry.get('id')
        if isinstance(map_id_raw, str):
            map_id = int(map_id_raw, 16)  # Convert hex string to int
        elif isinstance(map_id_raw, int):
            map_id = map_id_raw  # Already an int, no conversion needed
        else:
            raise ValueError(f"Unexpected type for 'id': {type(map_id_raw)}")

        # Handle both integer and string cases for 'file_id'
        map_file_id_raw = map_entry.get('file_id')
        if isinstance(map_file_id_raw, str):
            file_id = int(map_file_id_raw, 16)  # Convert hex string to int
        elif isinstance(map_file_id_raw, int):
            file_id = map_file_id_raw  # Already an int, no conversion needed
        else:
            raise ValueError(f"Unexpected type for 'id': {type(map_file_id_raw)}")

        actor_list_symbol = map_entry.get('actor_list')
        load_pickable_item_assets = map_entry.get('load_pickable_item_assets', False)
        has_skybox = map_entry.get('has_skybox', False)

        elf_path = f"{name}.bin.elf"
        bin_path = f"{name}.bin"

        actor_list_vram_start = get_vram_address_from_elf(elf_path, actor_list_symbol)
        
        if actor_list_vram_start is not None:
            print(f"Injecting VRAM address {hex(actor_list_vram_start)} for actor list '{actor_list_symbol}' in map '{name}' (ID: {hex(map_id)})")
            inject_vram_address_into_rom(actor_list_vram_start, map_id)

            vram_file_end = 0x06000000 | os.path.getsize(bin_path)
            
            print(f"Writing map info for '{name}' (ID: {hex(map_id)}) to ROM.")
            write_map_info_to_rom(map_id, file_id, vram_file_end, load_pickable_item_assets, has_skybox)
        else:
            print(f"Could not find symbol '{actor_list_symbol}' in '{elf_path}'")

if __name__ == "__main__":
    main()
