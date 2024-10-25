import yaml
import os
import subprocess

def inject_binaries():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    
    binary_files = config.get('binary_files', [])
    
    rom_in = 'cv64.z64'  # Specify your input ROM path
    rom_out = 'output_mod.z64'  # Single output ROM for all injections

    # Read the original ROM data
    with open(rom_in, 'rb') as rom_file:
        rom_data = bytearray(rom_file.read())

    for binary in binary_files:
        name = binary['name']
        rom_address = hex(binary['rom'])  # Ensure ROM address is in hex
        is_ni_file = binary['is_ni_file']
        file_id = binary.get('file_id', None)  # Get file_id if it exists
        
        # Construct the path to the generated binary file
        bin_file_path = f"{os.path.join('build', os.path.dirname(name))}/{os.path.basename(name)}.bin"
        
        # Check if the binary file exists before attempting injection
        if not os.path.exists(bin_file_path):
            print(f"Binary file not found: {bin_file_path}")
            continue  # Skip injection if the binary does not exist
        
        print(f"Injecting into ROM at address {rom_address} using file: {bin_file_path}")  # Debug output
        
        if is_ni_file:
            compress_flag = 1  # Set compress flag to 1 for compression
            version = 0  # Set CV64 version to USA v1.0

            subprocess.run([
                'python3', 'tools/cv64_file_insert.py',
                rom_in, rom_out,
                bin_file_path,
                rom_address[2:],  # Convert to hex without "0x"
                hex(file_id)[2:] if file_id is not None else '0',  # Convert to hex without "0x"
                str(compress_flag),
                str(version)
            ])
            print(f"Injected {bin_file_path} into ROM (Nisitenma-Ichigo)")  # Debug output
        else:
            # Directly inject into ROM (replace original data)
            injection_address_int = int(rom_address, 16)  # Convert hex to int for indexing
            
            with open(bin_file_path, 'rb') as binary_file:
                binary_data = binary_file.read()

            rom_data[injection_address_int:injection_address_int + len(binary_data)] = binary_data

            print(f"Injected {bin_file_path} directly into ROM at address {rom_address}")  # Debug output

    # Write the modified ROM data back to a new file
    with open(rom_out, 'wb') as rom_file:
        rom_file.write(rom_data)

if __name__ == "__main__":
    inject_binaries()
