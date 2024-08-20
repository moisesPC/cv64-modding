ROM_IN  = cv64.z64
ROM_OUT = cv64_mod.z64

PYTHON = python3

CC = tools/n64chain/bin/mips64-elf-gcc
AR = tools/n64chain/bin/mips64-elf-ar
AS = tools/armips/armips
CALC_CHECKSUM = tools/calcchecksum.py

INCLUDES = -Iinclude -Iinclude/ultra64 -Iinclude/game
CFLAGS   = -Wall -O3 -mtune=vr4300 -march=vr4300 -mabi=32 -fomit-frame-pointer -G0 -Wno-comment $(INCLUDES)

BUILD_DIR = build
ASM_DIR   = asm
SRC_DIR   = src

SEC_CUSTOM_SRC_DIR = $(SRC_DIR)/sec_custom
# We use find to recursively get all .c files within `SEC_CUSTOM_SRC_DIR`
SEC_CUSTOM_C_FILES = $(shell find $(SEC_CUSTOM_SRC_DIR) -name '*.c')
SEC_CUSTOM_O_FILES = $(patsubst $(SEC_CUSTOM_SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(SEC_CUSTOM_C_FILES))
# If this directory is modified, it must also be renamed in `main.asm`
SEC_CUSTOM_BINARY  = $(BUILD_DIR)/sec_custom.a

MAIN_ASM = $(ASM_DIR)/main.asm
ASM_N64_WRAP = $(BUILD_DIR)/armips_n64_wrapper.asm

############

.PHONY: rom
rom: $(ROM_OUT)

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
	rm -f $(ROM_OUT)

############

$(ROM_OUT): $(SEC_CUSTOM_BINARY) $(ROM_IN) $(ASM_N64_WRAP)
	$(AS) $(ASM_N64_WRAP) -root .
	$(PYTHON) $(CALC_CHECKSUM) $(ROM_OUT)

$(SEC_CUSTOM_BINARY): $(SEC_CUSTOM_O_FILES) | $(BUILD_DIR)
	$(AR) rcs $(SEC_CUSTOM_BINARY) $(SEC_CUSTOM_O_FILES)

############

$(BUILD_DIR)/%.o: $(SEC_CUSTOM_SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $^ -o $@

############

# Generate a wrapper asm file for armips
# This way we can assign some variables to it from the Makefile
# such as the ROM names

$(ASM_N64_WRAP): Makefile | $(BUILD_DIR)
	printf ".n64\n" > $(ASM_N64_WRAP)
	printf ".open \"$(ROM_IN)\", \"$(ROM_OUT)\", 0\n" >> $(ASM_N64_WRAP)
	printf ".include \"$(MAIN_ASM)\"\n" >> $(ASM_N64_WRAP)
	printf ".close\n" >> $(ASM_N64_WRAP)

############

$(BUILD_DIR):
	mkdir $(BUILD_DIR)
