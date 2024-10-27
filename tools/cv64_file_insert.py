# This file handles injecting Nisintema-Ichigo files into the ROM

import sys
from liblzkn64 import compress_buffer

# Constants
ROM_size = [0x04004200, 0x00C00000]		# 64 MB for decompressed ROMs, 12 MB for compressed ROM
numberNIFiles = 254

# Offsets
## 0 = USA v1.0, 1 = USA v1.1, 2 = USA v1.2, 3 = JPN, 4 = EUR
NisitenmaIchigo_tableStartAddr = [0x95C34, 0x95C34, 0x95FB4, 0x979C4, 0x965B4]
fileSizeTable_startAddr = [0x95430, 0x95430, 0x957B0, 0x971C0, 0x95DB0]

# Write a file buffer to the ROM data
def writeFile(romData, inputFile, addr):
    romData[addr:addr+len(inputFile)] = inputFile

# Patch the Nisitenma-Ichigo table entry corresponding to the file ID
# with the start and end addresses of the new injected file
# 1 entry in the table = size 0x8
def patchNITableAddresses(romData, fileStartAddr, fileEndAddr, fileID, compressFlag, version):
    compFlagNI = 0x00000000

    tableEntryAddr = NisitenmaIchigo_tableStartAddr[version] + (8 * fileID)

    if compressFlag:
        compFlagNI = 0x80000000
    
    romData[tableEntryAddr:tableEntryAddr+4] = (compFlagNI | fileStartAddr).to_bytes(4, 'big')
    romData[tableEntryAddr+4:tableEntryAddr+8] = fileEndAddr.to_bytes(4, 'big')

# Patch table containing the file sizes with the file size of the new injected file (decompressed)
# 1 entry in the table = size 0x8
def patchFileSizeTable(romData, fileSize, fileID, version):
    tableEntryAddr = fileSizeTable_startAddr[version] + (8 * fileID)
    segmentID = int.from_bytes(romData[tableEntryAddr:tableEntryAddr+4], 'big') & 0xFF000000  # Get segment ID of the file
    romData[tableEntryAddr+4:tableEntryAddr+8] = (segmentID | fileSize).to_bytes(4, 'big')      # Write segment ID | file size

def checkArgsErrors():
    if compressFlag != 0 and compressFlag != 1:
        raise Exception('The "compressFlag" can only be 0 (False) or 1 (True)')
    if injectionOffset > ROM_size[compressFlag]:
        raise Exception('Invalid injection offset')
    if fileID > numberNIFiles or fileID <= 0:
        raise Exception('Invalid file ID')

def modify_rom_data(romData, fileBuffer, injectionOffset, fileID, compressFlag, version):
    # Ensure fileBuffer is a bytearray
    fileBuffer = bytearray(fileBuffer)

    decompressedSize = len(fileBuffer)

    if compressFlag:
        fileBuffer = bytearray(compress_buffer(fileBuffer, False))

    fileBufferSize = len(fileBuffer)

    fileEndAddr = injectionOffset + fileBufferSize
    if fileEndAddr > ROM_size[compressFlag]:
        raise Exception(f'The file to inject is too big, or it doesn\'t fit entirely if injected at: {hex(injectionOffset)}')

    writeFile(romData, fileBuffer, injectionOffset)
    patchNITableAddresses(romData, injectionOffset, fileEndAddr, fileID, compressFlag, version)
    patchFileSizeTable(romData, decompressedSize, fileID, version)

    return romData

if __name__ == "__main__":
	# This part is left for demonstration purposes.
	# In actual use, you would call modify_rom_data() with appropriate parameters.
	print("CV64 Nisitenma-Ichigo File Injector")
	print("This script now modifies ROM data directly. Call modify_rom_data() with appropriate parameters.")

	print("\nArguments for modify_rom_data() :")
	print("1. romData (bytearray): The ROM data as a bytearray that you want to modify.")
	print("2. fileBuffer (bytes): The binary data of the file to inject into the ROM.")
	print("3. injectionOffset (int): The address in the ROM where the file will be injected.")
	print("4. fileID (int): The ID of the file to replace in the ROM's table (0-253).")
	print("5. compressFlag (int): Set to 1 to compress the injected file, or 0 for uncompressed.")
	print("6. version (int): The version of the ROM, where 0 = USA v1.0, 1 = USA v1.1, 2 = USA v1.2, 3 = JPN, 4 = EUR.")
