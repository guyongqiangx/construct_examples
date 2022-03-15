#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump


def test_RawCopy():
    d = RawCopy(Byte)
    x = d.parse(b'\xff')
    print(x)
    data = d.build(x)
    print(data)


def test_Prefixed():
    d = Prefixed(VarInt, GreedyRange(Int32ul))
    x = d.parse(b'\x08abcdefghijklmn')
    print(x)
    data = d.build(x)
    print(data)

    print('-' * 20)

    x = d.parse(b'\x0cabcdefghijklmn')
    print(x)
    data = d.build(x)
    print(data)


def test_PrefixedArray():
    d = PrefixedArray(VarInt, Int32ul)
    x = d.parse(b"\x02abcdefghpwdcced")
    print(x)
    data = d.build(x)
    print(data)


def test_FixedSized():
    d = FixedSized(10, Byte)
    x = d.parse(b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xffabcdef')
    print(x)
    data = d.build(x)
    print(data)

    print('-' * 20)
    d = FixedSized(8, Byte)
    x = d.parse(b'\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\xffabcdef')
    print(x)
    data = d.build(x)
    print(data)


def test_NullTerminated():
    d = NullTerminated(Byte)
    x = d.parse(b'\xff\x01\x00')
    print(x)
    data = d.build(255)
    print(data)

def test_Checksum_1():
    import hashlib
    d = Struct(
        "fields" / RawCopy(Struct(
            Padding(128),
        )),
        "checksum" / Checksum(Bytes(64),
                              lambda data: hashlib.sha512(data).digest(),
                              this.fields.data),
    )
    data = d.build(dict(fields=dict(value={})))
    print(hexdump(data, 16))


def test_Checksum_2():
    import hashlib
    d = Struct(
        "offset" / Tell,
        "checksum" / Padding(64),
        "fields" / RawCopy(Struct(
            Padding(128),
        )),
        "checksum" / Pointer(this.offset, Checksum(Bytes(64),
                               lambda data: hashlib.sha512(data).digest(),
                               this.fields.data)),
    )
    data = d.build(dict(fields=dict(value={})))
    print(hexdump(data, 16))


def test_Compressed():
    d = Prefixed(VarInt, Compressed(GreedyBytes, "zlib"))
    data = d.build(bytes(20))
    print(hexdump(data, 16))
    x = d.parse(data)
    print(x)

if __name__ == '__main__':
    # test_RawCopy()
    # test_Prefixed()
    # test_PrefixedArray()
    # test_FixedSized()
    # test_NullTerminated()
    # test_Checksum_1()
    # test_Checksum_2()
    test_Compressed()