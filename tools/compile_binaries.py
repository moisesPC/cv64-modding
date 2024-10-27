import os
import subprocess

INCLUDE_DIRS = [
    'include',
    'include/ultra64',
    'include/game',
    'src',
    'assets',
]

def compile_binaries():
    for root, _, files in os.walk('build'):
        for file in files:
            if file.endswith('.mk'):
                makefile_path = os.path.join(root, file)
                compile_binary(makefile_path)

def compile_binary(makefile_path):
    with open(makefile_path, 'r') as makefile:
        variables = dict(line.strip().split(' = ') for line in makefile if '=' in line)
    
    vram_decimal = int(variables['VRAM'])
    vram = hex(vram_decimal)
    files = variables['FILES'].split()
    output = variables['OUTPUT']

    script_dir = os.path.dirname(os.path.abspath(__file__))
    linker_ld_path = os.path.join(script_dir, '..', 'linker', 'linker.ld')
    repo_root = os.path.dirname(script_dir)
    
    include_flags = [f'-I{os.path.join(repo_root, dir)}' for dir in INCLUDE_DIRS]
    
    # Get the directory of the output file
    output_dir = os.path.dirname(output)
    
    # Compile
    object_files = []
    for source_file in files:
        # Use basename to get just the filename, and place it in the output directory
        object_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(source_file))[0]}.o")
        subprocess.run(['mips64-elf-gcc', '-c', '-G0', '-mabi=32', '-march=vr4300', '-mtune=vr4300', 
                        '-mfix4300', '-O2', '-fno-toplevel-reorder', '-fomit-frame-pointer', '-std=c17', '-mlong-calls',
                        '-DF3DEX_GBI_2', '-D_LANGUAGE_C',
                        '-fno-common', *include_flags,
                        source_file, '-o', object_file])
        object_files.append(object_file)
    
    # Link to create .elf
    subprocess.run(['mips64-elf-ld', '-o', f"{output}.elf", f"--defsym=VRAM_ADDRESS={vram}", f"-e 0x{vram[2:]}", '-T', linker_ld_path, '--just-symbols', 'extern.ld', *object_files])
    
    # Create a combined .o file
    subprocess.run(['mips64-elf-ld', '-r', '-o', f"{output}.o", *object_files])
    
    # Strip and create binary
    # We do '--set-section-flags', '.bss=alloc,load,contents'
    # in order to allocate the bss (in order to not have to allocate it manually in code, but has the disadvantage of increasing the file size)
    subprocess.run(['mips64-elf-objcopy', '-O', 'binary', '-j', '.text', '-j', '.data', '-j', '.rodata', '-j', '.bss', '--set-section-flags', '.bss=alloc,load,contents', f"{output}.elf", output])

if __name__ == "__main__":
    compile_binaries()
