.PHONY: all clean inject_binaries object_setup

PYTHON = python3
ARMIPS = armips
BUILD_DIR = build

all: parse_yaml compile_binaries inject_asm inject_binaries maps_setup object_setup calcchecksum

parse_yaml:
	$(PYTHON) tools/parse_yaml.py

compile_binaries:
	$(PYTHON) tools/compile_binaries.py

inject_binaries:
	$(PYTHON) tools/inject_binaries.py

maps_setup:
	$(PYTHON) tools/maps_setup.py

object_setup:
	$(PYTHON) tools/object_setup.py

inject_asm:
	$(ARMIPS) -root . asm/main.asm

calcchecksum:
	$(PYTHON) tools/calcchecksum.py output_mod.z64

clean:
	rm -rf $(BUILD_DIR)
	rm -f output_mod.z64
