#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump


# Varint 中的每个 byte 的最高位 bit 有特殊的含义，
#   - 如果该位为 1，表示后续的 byte 也是该数字的一部分，
#   - 如果该位为 0，则结束。
# 其他的 7 个 bit 都用来表示数字。
def test_VarInt():
    d = Struct('num'/VarInt, 'offset'/Tell)
    x = d.parse(b'\xFF\xFF\xFF\x0FFFFF')
    # x = d.parse(b'\x9f\xc3\xdf\xd5\xd2\x94\x80\xb6\x01')
    print(x)
    data = d.build(x)
    print(data)

    print('-' * 30)

    data = d.build(dict(num=102400))
    print(data)
    x = d.parse(data)
    print(x)


def test_BytesInteger():
    d = BytesInteger(4) or Int32ub
    x = d.parse(b'abcdef')
    print(x)
    data = d.build(x)
    print(data)

    print('*' * 20)

    data = d.build(255)
    print(data)

if __name__ == '__main__':
    # test_VarInt()
    test_BytesInteger()