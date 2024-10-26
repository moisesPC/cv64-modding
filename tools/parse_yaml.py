import yaml
import os

def parse_yaml():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    
    binary_files = config.get('binary_files', [])
    
    for binary in binary_files:
        name = binary['name']
        files = binary['files']
        vram = binary['vram']
        
        output_dir = os.path.join('build', os.path.dirname(name))
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f'{output_dir}/{os.path.basename(name)}.mk', 'w') as makefile:
            makefile.write(f"VRAM = {vram}\n")
            makefile.write(f"FILES = {' '.join(files)}\n")
            makefile.write(f"OUTPUT = {os.path.join(output_dir, os.path.basename(name))}.bin\n")

if __name__ == "__main__":
    parse_yaml()
