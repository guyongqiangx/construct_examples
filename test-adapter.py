#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump

def test_GUIDAdapter():
    # 6F9619FF-8B86-D011-B42D-00C04FC964FF
    class GUIDAdapter(Adapter):
        def _decode(self, obj, context, path):
            print("_decode:", obj, context, path, sep='\n...')
            s = ''.join(['%02X' % x for x in obj])
            return '{}-{}-{}-{}-{}'.format(s[0:8], s[8:12], s[12:16], s[16:20], s[20:32])

        def _encode(self, obj, context, path):
            return obj

    x = Struct(
        "guid" / GUIDAdapter(Bytes(16))
    )

    data = x.parse(b'\x6F\x96\x19\xFF\x8B\x86\xD0\x11\xB4\x2D\x00\xC0\x4F\xC9\x64\xFF')
    print('~' * 30)
    print(data)
    print('~' * 30)
    print(data.guid)

test_GUIDAdapter()