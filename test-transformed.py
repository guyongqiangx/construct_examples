#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump
from construct.lib.binary import bytes2bits, bits2bytes


def test_Transformed():
    #               subcon,    decodefunc, decodeamount, encodefunc, encodeamount
    d = Transformed(Bytes(16), bytes2bits, 2,            bits2bytes, 2)
    x = d.parse(b"\x00\x00\xff\xff")
    print(x)

    data = d.build(x)
    print(data)

    print('-' * 20)
    d = Transformed(BytesInteger(8), bytes2bits, 1,            bits2bytes, 1)
    x = d.parse(b"\xff\xff\x00")
    print(x)

    data = d.build(x)
    print(data)


def test_ByteSwapped():
    d = ByteSwapped(Bytes(4))
    x = d.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08")
    print(x)
    d = ByteSwapped(Bytes(8))
    x = d.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08")
    print(x)

    print('-' * 20)
    d = ByteSwapped(Array(2, Int32ul))
    x = d.parse(b"\x01\x02\x03\x04\x05\x06\x07\x08")
    print(x)
    print('+' * 10)
    d = Int32ul
    x = d.parse(b"\x08\x07\x06\x05")
    print(x)
    x = d.parse(b"\x04\x03\x02\x01")
    print(x)



if __name__ == '__main__':
    # test_Transformed()
    test_ByteSwapped()