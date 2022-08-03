#!/usr/bin/env python3

import os

from construct import *
from construct.lib import hexdump

# system/libufdt/utils/src/dt_table.h
DtTableHeader = Struct(
    "magic" / Hex(Const(0xd7b7ab1e, Int32ub)),
    "total_size" / Int32ub,
    "header_size" / Int32ub,
    "dt_entry_size" / Int32ub,
    "dt_entry_count" / Int32ub,
    "dt_entry_offset" / Int32ub,
    "page_size" / Int32ub,
    "version" / Int32ub
)

DtTableEntry = Struct(
    "dt_size" / Int32ub,
    "dt_offset" / Int32ub,
    "id" / Int32ub,
    "rev" / Int32ub,
    "custom" / Array(4, Int32ub)
)

DtTableEntryV1 = Struct(
    "dt_size" / Int32ub,
    "dt_offset" / Int32ub,

    "id" / Int32ub,
    "rev" / Int32ub,
    "flags" / Int32ub,

    "custom" / Array(3, Int32ub)
)

DtImage = Struct(
    "table_header" / DtTableHeader,
    "table_entry" / Array(this.table_header.dt_entry_count, DtTableEntry),
    # Other Stuff like ftd
)


def parse_dtbo(filename):
    with open(filename, 'rb') as f:
        data = f.read(1024)
        header = Debugger(DtImage).parse(data)
        print(header)


if __name__ == "__main__":
    # parse_dtbo(r"data/dtbo.inuvik.img")
    parse_dtbo(r"data/dtbo.avb.img")