.PHONY: all clean inject_binaries

PYTHON = python3
BUILD_DIR = build

all: parse_yaml compile_binaries inject_binaries

parse_yaml:
	$(PYTHON) tools/parse_yaml.py

compile_binaries:
	$(PYTHON) tools/compile_binaries.py

inject_binaries:
	$(PYTHON) tools/inject_binaries.py

clean:
	rm -rf $(BUILD_DIR)