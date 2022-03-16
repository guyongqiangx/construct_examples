#!/usr/bin/env python3

from construct import *
from construct.lib import hexdump

"""
Sparse Image Format and Debug Tool (Android R):
- system/core/libsparse/sparse_format.h
- system/core/libsparse/simg_dump.py
"""

SPARSE_HEADER = Struct(
    "magic" / Hex(Const(0xed26ff3a, Int32ul)),
    "major_version" / Int16ul,
    "minor_version" / Int16ul,
    "file_header_size" / Int16ul,
    "chunk_header_size" / Int16ul,
    "block_size" / Int32ul,
    "total_blocks" / Int32ul,
    "total_chunks" / Int32ul,
    "image_checksum" / Int32ul
)

CHUNK_HEADER = Struct(
    "chunk_type" / Enum(Int16ul,
        RAW = 0xCAC1,
        FILL = 0xCAC2,
        DONT_CARE = 0xCAC3,
        CRC = 0xCAC4
    ),
    Int16ul,                # reserved1
    "chunk_size" / Int32ul,
    "total_size" / Int32ul
)

CHUNK = Struct(
    "header" / RawCopy(CHUNK_HEADER),
    "data" / Switch(this.header.value.chunk_type,
            {
                "RAW": Bytes(this.header.value.total_size - CHUNK_HEADER.sizeof()),
                "FILL": Int32ul,
                "DONT_CARE": Bytes(0),
                "CRC": Hex(Int32ul)
            }
        )
)

SPARSE = Struct(
    "header" / RawCopy(SPARSE_HEADER),
    "chunks" / GreedyRange(CHUNK)
)


def pass_sparse_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
        sparse = SPARSE.parse(data)
        # print(sparse)

        sph = sparse.header.value
        print("*" * 40)
        print("HEADER:")
        print(hexdump(sparse.header.data, 16))
        print("            magic: {}".format(sph.magic))
        print("    major version: {}".format(sph.major_version))
        print("    minor version: {}".format(sph.minor_version))
        print(" file header size: {}".format(sph.file_header_size))
        print("chunk header size: {}".format(sph.chunk_header_size))
        print("       block size: {}".format(sph.block_size))
        print("     total blocks: {}".format(sph.total_blocks))
        print("     total chunks: {}".format(sph.total_chunks))
        print("   image checksum: {}".format(sph.image_checksum))
        print("")

        print("*" * 40)
        i = 0
        for chunk in sparse.chunks:
            print("CHUNK {:d}:".format(i))
            print(hexdump(chunk.header.data, 16))
            header = chunk.header.value
            print("  chunk type: {}".format(header.chunk_type))
            print("  chunk size: {}".format(header.chunk_size))
            print("  total size: {}".format(header.total_size))
            print("")
            i += 1

"""
def hexdump(data, line_size=16, indent=0, prefix=""):
    for i in range(len(data)):
        if i % line_size == 0:
            print("{}{}".format(" " * indent, prefix), end="")
        print("{:02X} ".format(data[i]), end="")
        if i % line_size == (line_size - 1) or i == len(data) - 1:
            print("", end="\n")
"""

if __name__ == "__main__":
    pass_sparse_file("data/cache.img")