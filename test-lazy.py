#!/usr/bin/env python3


from construct import *
from construct.lib.hex import hexdump


d = Lazy(Byte)
x = d.parse(b'\x00')
print(x)
print(x())


#
# LazyBound
#
d = Struct(
    "value" / Byte,
    "next" / If(this.value > 0, LazyBound(lambda: d)),  # 这里使用匿名函数: (lambda: d)
)

print(d.parse(b"\x05\x09\x00"))
