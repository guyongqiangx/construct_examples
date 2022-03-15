#!/usr/bin/env python3

from construct import *
from construct.lib.hex import hexdump


class RawData:
    def __init__(self, start, end, data):
        self.start = start
        self.end = end
        self.data = data

# class Rawx(Subconstruct):
#
#     def _parse(self, stream, context, path):
#         offset1 = stream_tell(stream)
#         obj = self.subcon._parsereport(stream, context, path)
#         offset2 = stream_tell(stream)
#         stream_seek(stream, offset1)
#         data = stream_read(stream, offset2-offset1)
#         return Container(data=data, value=obj, offset1=offset1, offset2=offset2, length=(offset2-offset1))
#
#     def _build(self, obj, stream, context, path):
#         if obj is None and self.subcon.flagbuildnone:
#             obj = dict(value=None)
#         if 'data' in obj:
#             data = obj['data']
#             offset1 = stream_tell(stream)
#             stream_write(stream, data)
#             offset2 = stream_tell(stream)
#             return Container(obj, data=data, offset1=offset1, offset2=offset2, length=(offset2-offset1))
#         if 'value' in obj:
#             value = obj['value']
#             offset1 = stream_tell(stream)
#             buildret = self.subcon._build(value, stream, context, path)
#             value = value if buildret is None else buildret
#             offset2 = stream_tell(stream)
#             stream_seek(stream, offset1)
#             data = stream_read(stream, offset2-offset1)
#             return Container(obj, data=data, value=value, offset1=offset1, offset2=offset2, length=(offset2-offset1))
#         raise RawCopyError('RawCopy cannot build, both data and value keys are missing')

class Raw(Subconstruct):

    def __init__(self, subcon):
        super(Raw, self).__init__(subcon)

    def _parse(self, stream, context, path):
        start = stream_tell(stream)
        obj = self.subcon._parsereport(stream, context, path)
        end = stream_tell(stream)
        stream_seek(stream, start)
        data = stream_read(stream, end-start)
        obj['raw'] = RawData(start, end, data)

        return obj

    def _build(self, obj, stream, context, path):
        return obj


x = Struct(
    "data" / Raw(Bytes(2)),
)

item = x.parse(b'\x04\x05\x06\x07')