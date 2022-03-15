#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump
from construct.lib.py3compat import integers2bytes
import zlib


# gpt_header = Struct(
#     "header" / RawCopy(Struct(
#         "signature" / Const(b'EFI PART'),
#         "revision" / Int32ul,
#         "header_size" / Int32ul,
#     )),
#     # Probe(),
#     # "header_crc32" / Checksum(Bytes(4),
#     #                           lambda data: crc32(data),
#     #                           this.header.data),  # Hex(Int32ul),
# )
#
#
# gpt = Struct(
#     Padding(512), # "mbr" / Bytes(512),         # LBA0, Protective MBR
#     "header" / RawCopy(Struct(
#         "signature" / Const(b'EFI PART'),       # Bytes(8)
#         "revision" / Int32ul,                   # Bytes(4)
#         "header_size" / Int32ul,                # Bytes(4)
#     )),
#     "header_crc32" / Bytes(4)
#     # Probe(),
#     # "header_crc32" / Checksum(Bytes(4),
#     #                           lambda data: crc32(data),
#     #                           this.header.data),  # Hex(Int32ul),
# )

def get_gpt_header_data(header, offset):
    data = bytearray(header)
    data[offset:offset+4] = 0
    print(hexdump(data, 16))
    return data

gpt_header = Struct(
    "header" / RawCopy(Struct(
        "signature" / Const(b'EFI PART'),
        "revision" / Hex(Int32ub),
        "header_size" / Int32ul,
        "header_crc32_offset" / Tell,
        "header_crc32" / Padding(4),  # Hex(Int32ul),
        # Probe(),
        Padding(4),
        "lba_current" / Int64ul,
        "lba_backup" / Int64ul,
        "lba_usable_first" / Int64ul,
        "lba_usable_last" / Int64ul,
        "guid" / Bytes(16),
        "part_entry_lba" / Int64ul,
        "part_entry_number" / Int32ul,
        "part_entry_single_size" / Int32ul,
        "part_arrray_crc32" / Hex(Int32ul)
    )),
    "header_crc32" / Pointer(this.header.value.header_crc32_offset,
                             Checksum(Bytes(4),
                                      lambda data: zlib.crc32(data),
                                      get_gpt_header_data(this.header.data, this.header.value.header_crc32_offset))),
    Padding(512 - this.header.value.header_size)
)

gpt = Struct(
    Padding(512), # "mbr" / Bytes(512),         # LBA0, Protective MBR
    "gpt_header" / gpt_header,  # LBA1, GPT Header
)


if __name__ == '__main__':
    setGlobalPrintFullStrings(True)

    mygpt = gpt.parse_file(r'data/gpt.bin')
    print(mygpt)
    print(hexdump(mygpt.gpt_header.header.data, 16))

