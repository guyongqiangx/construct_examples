#!/usr/bin/env python3

from construct import *
from construct.lib import hexdump

SHA256_DIGEST_LENGTH = 32

# Android R: system/extras/libfec/include/fec/io.h

fec_header = Struct(
    "magic" / Hex(Const(0xfecfecfe, Int32ul)),
    "version" / Int32ul,
    "size" / Int32ul,
    "roots" / Int32ul,
    "fec_size" / Int32ul,
    "inp_size" / Int32ul,
    "hash" / Bytes(SHA256_DIGEST_LENGTH)
)

if __name__ == "__main__":
    pass