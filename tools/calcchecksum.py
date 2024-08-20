# Source: https://github.com/Decompollaborate/ipl3checksum
import ipl3checksum
import struct
import sys

CHECKSUM_ROM_OFFSET = 0x00000010
filename = sys.argv[1]

with open(filename, 'r+b') as file:
    romBytes = file.read()
    checksum = ipl3checksum.calculateChecksumAutodetect(romBytes)

    # If this assert fails it is because the library was not able to compute the
    # checksum, probably because the passed rom was too small
    assert checksum is not None

    file.seek(CHECKSUM_ROM_OFFSET)
    for num in checksum:
        file.write(struct.pack('>I', num))  # >I' means big-endian unsigned int (4 bytes)
