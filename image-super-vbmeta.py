#!/usr/bin/env python3

from construct import *

# Android R: system/core/fs_mgr/libvbmeta/super_vbmeta_format_c.h
SuperVBMetaHeader = Struct(
    "magic" / Const(0x5356424d, Int32ul),
    "major_version" / Int16ul,
    "minor_version" / Int16ul,
    "header_size" / Int32ul,
    "total_size" / Int32ul,
    "checksum" / Bytes(32),
    "descriptors_size" / Int32ul,
    "in_use" / Int32ul,
    Padding(72)     # reserved[72]
)

VBMetaDescriptor = Struct(
    "descriptor" / Struct(
        "vbmeta_index" / Int8ul,
        "vbmeta_name_length" / Int32ul,
        Padding(48)     # reserved[48]
        ),
    "partition_name" / PaddedString(this.descriptor.vbmeta_name_length, "utf8")
)

if __name__ == "__main__":
    pass