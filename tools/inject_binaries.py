import yaml
import os
import cv64_file_insert  # Import the module containing the modify_rom_data function

def inject_binaries():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    
    binary_files = config.get('binary_files', [])
    
    rom_out = 'output_mod.z64'  

    # Read the original ROM data
    with open(rom_out, 'rb') as rom_file:
        rom_data = bytearray(rom_file.read())

    for binary in binary_files:
        name = binary['name']
        rom_address = binary['rom']  # Keep this as an integer
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

            # Read the file to inject
            with open(bin_file_path, 'rb') as f:
                file_buffer = f.read()

            # Call modify_rom_data directly
            rom_data = cv64_file_insert.modify_rom_data(
                romData=rom_data,
                fileBuffer=file_buffer,
                injectionOffset=rom_address,
                fileID=file_id,
                compressFlag=compress_flag,
                version=version
            )

            print(f"Injected {bin_file_path} into ROM (Nisitenma-Ichigo)")

        else:
            with open(bin_file_path, 'rb') as binary_file:
                binary_data = binary_file.read()

            # Modify the original ROM data directly
            rom_data[rom_address:rom_address + len(binary_data)] = binary_data

            print(f"Injected {bin_file_path} directly into ROM at address {hex(rom_address)}")

    # Write modified data back to output ROM after all injections are done.
    with open(rom_out, 'wb') as rom_file:
        rom_file.write(rom_data)

if __name__ == "__main__":
    inject_binaries()
