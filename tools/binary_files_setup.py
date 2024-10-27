# This file does an initial YAML parsing to `binary_files` in order to setup the temporary Makefiles 
# that will allow the binaries to be compiled wwith the specified parameters.

import sys
import yaml
import os

def binary_files_setup():
    with open(sys.argv[1], 'r') as file:
        config = yaml.safe_load(file)
    
    binary_files = config.get('binary_files', [])
    
    for binary in binary_files:
        name = binary['name']
        files = binary['files']
        vram = binary['vram']
        dont_compile = binary.get('dont_compile', False)
        
        output_dir = os.path.join('build', os.path.dirname(name))
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f'{output_dir}/{os.path.basename(name)}.mk', 'w') as makefile:
            makefile.write(f"VRAM = {vram}\n")
            makefile.write(f"FILES = {' '.join(files)}\n")
            makefile.write(f"OUTPUT = {os.path.join(output_dir, os.path.basename(name))}.bin\n")
            makefile.write(f"DONT_COMPILE = {'1' if dont_compile else '0'}\n")

if __name__ == "__main__":
    binary_files_setup()
