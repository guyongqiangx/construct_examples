#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump
from zlib import crc32


# 6F9619FF-8B86-D011-B42D-00C04FC964FF
class GUIDAdapter(Adapter):
    def _decode(self, obj, context, path):
        # print("_decode:", obj, context, path, sep='\n...')
        s = ''.join(['%02X' % x for x in obj])
        return '{}-{}-{}-{}-{}'.format(s[0:8], s[8:12], s[12:16], s[16:20], s[20:32])

    def _encode(self, obj, context, path):
        return obj


gpt_header = Struct(
    "signature" / Const(b'EFI PART'),
    "revision" / Int32ul,
    "header_size" / Int32ul,
    Probe(),
    "header_crc32" / Int32ul,  # Hex(Int32ul),
    Padding(4),
    "lba_current" / Hex(Int64ul),
    "lba_backup" / Hex(Int64ul),
    "lba_usable_first" / Hex(Int64ul),
    "lba_usable_last" / Hex(Int64ul),
    "guid" / GUIDAdapter(Bytes(16)),  # Bytes(16),
    "part_entry_lba" / Int64ul,
    "part_entry_number" / Int32ul,
    "part_entry_single_size" / Int32ul,
    "part_arrray_crc32" / Hex(Int32ul),
    Padding(512 - this.header_size)
)

partition_entry = Struct(
    "type" / GUIDAdapter(Bytes(16)),  # Bytes(16),  # Partition type GUID
    "guid" / GUIDAdapter(Bytes(16)),  # Bytes(16),  # Unique partition GUID
    "lba_first" / Hex(Int64ul),
    "lba_last" / Hex(Int64ul),
    "flag" / Bytes(8),
    "name" / PaddedString(72, "utf16"),
    # Probe(),
)

gpt = Struct(
    Padding(512), # "mbr" / Bytes(512),         # LBA0, Protective MBR
    "gpt_header" / gpt_header,  # LBA1, GPT Header
    "partitions" / Array(this.gpt_header.part_entry_number, partition_entry)
)

if __name__ == '__main__':
    setGlobalPrintFullStrings(True)

    mygpt = gpt.parse_file(r'data/gpt.bin')
    print(mygpt)

