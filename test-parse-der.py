#!/usr/bin/env python3

from construct import *
from construct.lib.hex import *


pubder = r"data/key0_pub.der"
prvder = r"data/key0.der"


universal_tag = Enum(BitsInteger(5),
                     boolean=1,
                     integer=2,
                     bit_string=3,
                     octet_string=4,
                     null=5,
                     object_identifier=6,
                     object_descriptor=7,
                     external=8,
                     real=9,
                     enumerated=10,
                     utf8_string=12,
                     relative_oid=13,
                     sequence=16,
                     set=17,
                     numberic_string=18,
                     printable_string=19,
                     teletex_string=20,
                     videotex_string=21,
                     ia5_string=22,
                     utc_time=23,
                     generalized_time=24,
                     graphic_string=25,
                     visible_string=26,
                     general_string=27,
                     universal_string=28,
                     character_string=29,
                     bmp_string=30,
                     reserved=31)

application_tag = BitsInteger(5)
context_specific_tag = BitsInteger(5)
private_tag = BitsInteger(5)

der_format = Struct(
    "header" / Struct(
        "id" / BitStruct(
            "tag" / Enum(BitsInteger(2),
                           universal=0,
                           application=1,
                           specific=2,
                           private=3),
            "flag" / Enum(Bit,
                          primitive=0,
                          constructed=1),
            "number" / Switch(this.tag,
                              {
                                  "universal": universal_tag,
                                  "application": application_tag,
                                  "specific": context_specific_tag,
                                  "private": private_tag,
                              })
        ),
        "len" / BitStruct(
            "indicator" / Bit,
            "data" / BitsInteger(7),
            "value" / IfThenElse(this.indicator == 0, Computed(this.data), BitsInteger(8 * this.data)),
        ),
        "size" / Computed(2 + this.len.indicator * this.len.data),
    ),
    "payload" / Struct(
        "data" / Bytes(this._.header.len.value),
        "size" / Computed(this._.header.len.value),
    ),
)


def test_der_format():
    import os
    with open(pubder, 'rb') as file:
        data = file.read()
    item = der_format.parse(data)
    print(item)
    print(hexdump(item.payload.data, 16))
    #print(hexdump(item.header, 16))
    os.system('rm -rf data/der-payload.bin')
    with open('data/der-payload.bin', 'wb') as w:
        w.write(item.payload.data)


if __name__ == "__main__":
    test_der_format()