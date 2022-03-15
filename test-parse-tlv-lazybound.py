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

tlv_item = Struct(
    # 1 byte
    "t" / BitStruct(
        "tag" / Enum(BitsInteger(2),
                           universal=0,
                           application=1,
                           context_specific=2,
                           private=3),
        "flag" / Enum(Bit,
                      primitive=0,
                      constructed=1),
        "number" / Switch(this.tag,
                          {
                              'universal': universal_tag,
                              'application': application_tag,
                              'context_specific': context_specific_tag,
                              'private': private_tag,
                          }),

        "size" / Computed(1),
    ),

    # 1+n bytes
    "l" / BitStruct(
        # indicate single or multi bytes for length
        "indicator" / Bit,
        "meta" / BitsInteger(7),
        "value" / IfThenElse(this.indicator == 0, Computed(this.meta), BitsInteger(8 * this.meta)),

        "size" / Computed(1 + this.indicator * this.meta),
    ),

    "v" / Struct(
        "data" / If(this._.t.flag == "constructed", LazyBound(lambda :tlv_item)),
        "size" / Computed(this._.l.value),
    ),

    "size" / Computed(this.t.size + this.l.size + this.v.size),
)


def test_lazybound():
    #
    # parse public key
    #
    with open(pubder, "rb") as f:
        data = f.read()

    item = tlv_item.parse(data)

    print(item)

if __name__ == '__main__':
    # test_tlv_example()
    test_lazybound()