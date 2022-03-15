#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump


def test_Array():
    d = Array(5, Byte)
    data = d.build(range(5))
    print(data)
    x = d.parse(data)
    print(repr(x))


def test_GreedyRange():
    d = GreedyRange(Byte)
    data = d.build(range(8))
    print(data)
    x = d.parse(data)
    print(repr(x))


def test_StopIf():
    # d = GreedyRange(FocusedSeq(0, 'x' / Byte, StopIf(this.x == 0)))
    d = GreedyRange(FocusedSeq("x", "x" / Byte, StopIf(this.x == 0)))
    x = d.parse(b"\x01\x02\x00\x03?????")
    print(repr(x))

    print('-' * 20)
    d = Struct("x" / Byte, StopIf(this.x == 0), "y" / Byte)
    x = d.parse(b"\x01\x02")
    print(repr(x))
    x = d.parse(b"\x00\x02\x03\x04")
    print(repr(x))

    print('-' * 20)
    d = Sequence("x" / Byte, StopIf(this.x == 0), "y" / Byte)
    x = d.parse(b"\x01\x02")
    print(repr(x))
    x = d.parse(b"\x00\x02")
    print(repr(x))

    print('-' * 20)
    d = Struct(
        "a" / Byte,
        "b" / Struct("x" / Byte, StopIf(this.x == 0), "y" / Byte),
        "c" / Byte,
    )
    x = d.parse(b"\x01\x02\x03\x04")
    print(repr(x))
    x = d.parse(b"\x01\x00\x03\x04")
    print(repr(x))


def test_RepeatUntil():
    d = RepeatUntil(lambda x, lst, ctx: x > 7, Byte)
    x = d.parse(b"\x01\xff\x02")
    print(repr(x))

    print('-' * 20)
    d = RepeatUntil(lambda x, lst, ctx: lst[-2:] == [0, 0], Byte)
    x = d.parse(b"\x01\x03\x05\x00\x00\xff")
    print(repr(x))


if __name__ == '__main__':
    # test_Array()
    # test_GreedyRange()
    # test_StopIf()
    test_RepeatUntil()