#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump


def test_Context():
    d = Struct(
        'x' / Computed(1),
        'inner' / Struct(
            'inner2' / Struct(
                'x' / Computed(this._root.x),
                'z' / Computed(this._params.z),
                'zz' / Computed(this._root._.z),
            ),
        ),
        Probe(),
    )
    setGlobalPrintPrivateEntries(True)
    x = d.parse(b'', z=2)

    print(repr(x))
    print(x)


if __name__ == '__main__':
    test_Context()