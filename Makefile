.PHONY: all clean inject_binaries object_setup

PYTHON = python3
ARMIPS = armips
BUILD_DIR = build

INPUT_ROM  := cv64.z64
OUTPUT_ROM := cv64_mod.z64
CONFIG_YML := config.yml

all: binary_files_setup compile_binaries inject_asm inject_binaries maps_setup object_setup calcchecksum

binary_files_setup:
	$(PYTHON) tools/binary_files_setup.py $(CONFIG_YML)

compile_binaries:
	$(PYTHON) tools/compile_binaries.py

inject_binaries:
	$(PYTHON) tools/inject_binaries.py $(OUTPUT_ROM) $(CONFIG_YML)

maps_setup:
	$(PYTHON) tools/maps_setup.py $(OUTPUT_ROM) $(CONFIG_YML)

object_setup:
	$(PYTHON) tools/object_setup.py $(OUTPUT_ROM) $(CONFIG_YML)

inject_asm:
	$(ARMIPS) -root . asm/main.asm -strequ INPUTROM "$(INPUT_ROM)" -strequ OUTPUTROM "$(OUTPUT_ROM)"

calcchecksum:
	$(PYTHON) tools/calcchecksum.py $(OUTPUT_ROM)

clean:
	rm -rf $(BUILD_DIR)
	rm -f $(OUTPUT_ROM)
