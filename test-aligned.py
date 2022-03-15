#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump


ali = Struct(
    Padding(512),
    "header" / Bytes(4),
    "offset" / Tell,
    "rest" / Aligned(528, Byte)
)

if __name__ == '__main__':
    setGlobalPrintFullStrings(True)

    mygpt = ali.parse_file(r'data/gpt.bin')
    print(mygpt)