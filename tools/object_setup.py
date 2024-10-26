import yaml
import struct
from elftools.elf.elffile import ELFFile

# Constants
FUNCTION_POINTERS_OFFSET = 0x92E70  # Starting address for function pointers - 1
VRAM_POINTERS_OFFSET = 0x94030       # Starting address for VRAM pointers
FUNCTION_POINTERS_COUNT = 554         # Total number of function pointers
FILES_INFO_PTR_OFFSET = 0x5588       # ROM address where files_info data starts

def read_rom(filename):
    """Read the entire ROM file into a bytearray."""
    with open(filename, 'r+b') as rom_file:
        return bytearray(rom_file.read())

def write_to_rom(rom_data, offset, data):
    """Write data to the ROM at the specified offset."""
    rom_data[offset:offset + len(data)] = data

def get_vram_address(rom_address):
    """Convert a ROM address to a VRAM address."""
    return (0x80000460 - 0x00001060) + rom_address

def get_symbol_address(elf_path, symbol_name):
    """Get the address of a symbol from an ELF file."""
    with open(elf_path, 'rb') as f:
        elf = ELFFile(f)
        symtab = elf.get_section_by_name('.symtab')
        if not symtab:
            raise ValueError(f"No symbol table found in {elf_path}")
        
        symbols = symtab.get_symbol_by_name(symbol_name)
        if not symbols:
            raise ValueError(f"Symbol {symbol_name} not found in {elf_path}")
        
        return symbols[0]['st_value']

def process_config(rom_data, config_path):
    """Process the configuration file and update the ROM data accordingly."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    for obj in config['objects']:
        raw_id = int(obj['raw_id'], 16) if isinstance(obj['raw_id'], str) else obj['raw_id']
        
        # Handle entrypoint
        if isinstance(obj['entrypoint'], dict):
            elf_path, symbol_name = next(iter(obj['entrypoint'].items()))
            entrypoint = get_symbol_address(elf_path, symbol_name)
        else:
            entrypoint = obj['entrypoint']

        # Write entrypoint to function pointers array
        write_to_rom(rom_data,
                     FUNCTION_POINTERS_OFFSET + (raw_id * 4),
                     struct.pack('>I', entrypoint))  # Write as big-endian

        # Create files_info struct
        files_info_raw_data = bytearray()
        files_info = obj['files_info']

        for i, (file_id, alignment) in enumerate(files_info):
            if i == len(files_info) - 1:  # Last entry
                file_id |= 0x40000000  # OR with 0x40000000
            
            # Append file ID and alignment to raw data
            files_info_raw_data.extend(struct.pack('>I', file_id))
            files_info_raw_data.extend(struct.pack('>I', alignment))

        # Write files_info struct to ROM at files_info_ptr
        files_info_ptr = obj['files_info_ptr']
        
        print(f"Files Info Pointer: {hex(files_info_ptr)}")
        
        write_to_rom(rom_data,
                     files_info_ptr,
                     files_info_raw_data)

        # Convert files_info_ptr to VRAM address and write it to VRAM pointers array
        vram_address = get_vram_address(files_info_ptr)
        
        print(f"VRAM Address for ID {raw_id}: {hex(vram_address)}")
        
        if vram_address < 0 or vram_address > 0xFFFFFFFF:
            raise ValueError(f"VRAM address {hex(vram_address)} is out of range.")
        
        print(f"Writing VRAM address to offset: {hex(VRAM_POINTERS_OFFSET + (raw_id * 4))}")
        write_to_rom(rom_data,
                     VRAM_POINTERS_OFFSET + (raw_id * 4),
                     struct.pack('>I', vram_address))  # Write as big-endian

def main():
    rom_filename = 'output_mod.z64'  # Path to your ROM file
    config_filename = 'config.yml'  # Path to your YAML config file

    rom_data = read_rom(rom_filename)
    process_config(rom_data, config_filename)

    with open(rom_filename, 'r+b') as rom_file:
        rom_file.write(rom_data)

if __name__ == "__main__":
    main()