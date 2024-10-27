# This file handles injecting binary files (after they're compiled, linked and stripped-out)
# into the output ROM

import sys
import yaml
import os
import cv64_file_insert

def calculate_address(binary_files, current_binary, address_type, processed_files):
    if f'follows-{address_type}' in current_binary:
        follow_name = current_binary[f'follows-{address_type}']
        for binary in binary_files:
            if binary['name'] == follow_name:
                if binary['name'] in processed_files:
                    return processed_files[binary['name']][f'{address_type}_end']
                elif address_type in binary:
                    return binary[address_type]
                else:
                    return calculate_address(binary_files, binary, address_type, processed_files)
    return current_binary.get(address_type)

def inject_binaries():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    
    binary_files = config.get('binary_files', [])
    
    rom_out = sys.argv[1]

    with open(rom_out, 'rb') as rom_file:
        rom_data = bytearray(rom_file.read())

    processed_files = {}

    for binary in binary_files:
        name = binary['name']
        rom_address = calculate_address(binary_files, binary, 'rom', processed_files)
        is_ni_file = binary['is_ni_file']
        file_id = binary.get('file_id', None)  
        
        bin_file_path = f"{os.path.join('build', os.path.dirname(name))}/{os.path.basename(name)}.bin"
        
        if not os.path.exists(bin_file_path):
            print(f"Binary file not found: {bin_file_path}")
            continue
        
        print(f"Injecting into ROM at address {hex(rom_address)} using file: {bin_file_path}")  
        
        if is_ni_file:
            compress_flag = 1  
            version = 0

            with open(bin_file_path, 'rb') as f:
                file_buffer = f.read()

            rom_data = cv64_file_insert.modify_rom_data(
                romData=rom_data,
                fileBuffer=file_buffer,
                injectionOffset=rom_address,
                fileID=file_id,
                compressFlag=compress_flag,
                version=version
            )

            # Calculate the end address after compression
            compressed_size = len(cv64_file_insert.compress_buffer(file_buffer, False))
            rom_end_address = rom_address + compressed_size

            print(f"Injected {bin_file_path} into ROM (Nisitenma-Ichigo)")

        else:
            with open(bin_file_path, 'rb') as binary_file:
                binary_data = binary_file.read()

            rom_data[rom_address:rom_address + len(binary_data)] = binary_data
            rom_end_address = rom_address + len(binary_data)

            print(f"Injected {bin_file_path} directly into ROM at address {hex(rom_address)}")

        # Store the end address for this file
        processed_files[name] = {'rom_end': rom_end_address}

    with open(rom_out, 'wb') as rom_file:
        rom_file.write(rom_data)

if __name__ == "__main__":
    inject_binaries()
