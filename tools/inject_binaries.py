import yaml
import os
import subprocess

def inject_binaries():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    
    binary_files = config.get('binary_files', [])
    
    rom_in = 'cv64.z64'  
    rom_out = 'output_mod.z64'  

    # Read the original ROM data
    with open(rom_in, 'rb') as rom_file:
        rom_data = bytearray(rom_file.read())

    for binary in binary_files:
        name = binary['name']
        rom_address = hex(binary['rom'])  
        is_ni_file = binary['is_ni_file']
        file_id = binary.get('file_id', None)  
        
        bin_file_path = f"{os.path.join('build', os.path.dirname(name))}/{os.path.basename(name)}.bin"
        
        if not os.path.exists(bin_file_path):
            print(f"Binary file not found: {bin_file_path}")
            continue
        
        print(f"Injecting into ROM at address {rom_address} using file: {bin_file_path}")  
        
        if is_ni_file:
            compress_flag = 1  
            version = 0  

            # Directly modify rom_data instead of using subprocess
            subprocess.run([
                'python3', 'tools/cv64_file_insert.py',
                rom_in,
                rom_out,
                bin_file_path,
                rom_address[2:], 
                hex(file_id)[2:] if file_id is not None else '0', 
                str(compress_flag),
                str(version)
            ])
            print(f"Injected {bin_file_path} into ROM (Nisitenma-Ichigo)")

            # Read the injected data back into rom_data
            injection_address_int = int(rom_address, 16)
            with open(bin_file_path, 'rb') as binary_file:
                binary_data = binary_file.read()
            rom_data[injection_address_int:injection_address_int + len(binary_data)] = binary_data

        else:
            injection_address_int = int(rom_address, 16)  
            
            with open(bin_file_path, 'rb') as binary_file:
                binary_data = binary_file.read()

            # Modify the original ROM data directly
            rom_data[injection_address_int:injection_address_int + len(binary_data)] = binary_data

            print(f"Injected {bin_file_path} directly into ROM at address {rom_address}")

    # Write modified data back to output ROM after all injections are done.
    with open(rom_out, 'wb') as rom_file:  # Open in write mode
        # Print the first 0x10 bytes of the output ROM at offset A8420 from rom_data
        offset_to_print = 0xA8420
        num_bytes = 0x10  # Number of bytes to read

        # Print from rom_data
        print(f"Bytes in rom_data at offset {hex(offset_to_print)}:")
        print(' '.join(f"{rom_data[i]:02x}" for i in range(offset_to_print, offset_to_print + num_bytes)))

        # Write modified data to the output ROM
        rom_file.write(rom_data)

if __name__ == "__main__":
    inject_binaries()
