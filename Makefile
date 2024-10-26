.PHONY: all clean inject_binaries object_setup

PYTHON = python3
BUILD_DIR = build

all: parse_yaml compile_binaries inject_binaries object_setup calcchecksum

parse_yaml:
	$(PYTHON) tools/parse_yaml.py

compile_binaries:
	$(PYTHON) tools/compile_binaries.py

inject_binaries:
	$(PYTHON) tools/inject_binaries.py

object_setup:
	$(PYTHON) tools/object_setup.py

calcchecksum:
	$(PYTHON) tools/calcchecksum.py output_mod.z64

clean:
	rm -rf $(BUILD_DIR)
