#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump


def test_on_the_fly():
    def printobj(obj, ctx):
        print(obj)
        if ctx._index+1 >= 3:
            raise CancelParsing
    st = Struct(
        "first" / Byte * printobj,
        "second" / Byte,
    )
    d = GreedyRange(st * printobj)
    x = d.parse(b'\x01\x02\x03\x04\x05\x06')
    print(repr(x))
    data = d.build(x)
    print(data)


if __name__ == '__main__':
    test_on_the_fly()