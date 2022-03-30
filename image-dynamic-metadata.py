#!/usr/bin python3

from construct import *

LP_PARTITION_RESERVED_BYTES = 4096

LP_GEOMETRY_SIZE = 4096

LP_METADATA_HEADER_SIZE = 256
LP_METADATA_SIZE = 65536

LpMetadataGeometry = Struct(
    "magic" / Hex(Const(0x616c4467, Int32ul)),
    "struct_size" / Int32ul,
    "checksum" / Hex(Bytes(32)),
    "metadata_max_size" / Int32ul,
    "metadata_slot_count" / Int32ul,
    "logical_block_size" / Int32ul,
)

LpMetadataTableDescriptor = Struct(
    "offset" / Int32ul,
    "num_entries" / Int32ul,
    "entry_size" / Int32ul
)

# Android Q, v10.0
LpMetadataHeaderV1_0 = Struct(
    "magic" / Hex(Const(0x414c5030, Int32ul)),
    "major_version" / Int16ul,
    "minor_version" / Int16ul,
    "header_size" / Int32ul,
    "header_checksum" / Hex(Bytes(32)),
    "tables_size" / Int32ul,
    "tables_checksum" / Hex(Bytes(32)),
    "partitions" / LpMetadataTableDescriptor,
    "extents" / LpMetadataTableDescriptor,
    "groups" / LpMetadataTableDescriptor,
    "block_devices" / LpMetadataTableDescriptor
)

# Android R, v10.2
LpMetadataHeaderV1_2 = Struct(
    "magic" / Hex(Const(0x414c5030, Int32ul)),
    "major_version" / Int16ul,
    "minor_version" / Int16ul,
    "header_size" / Int32ul,
    "header_checksum" / Hex(Bytes(32)),
    "tables_size" / Int32ul,
    "table_checksum" / Hex(Bytes(32)),
    "partitions" / LpMetadataTableDescriptor,
    "extents" / LpMetadataTableDescriptor,
    "groups" / LpMetadataTableDescriptor,
    "block_devices" / LpMetadataTableDescriptor,
    "flags" / Int32ul,
    Padding(124)
)

LpMetadataHeader = Struct(
    "magic" / Hex(Const(0x414c5030, Int32ul)),
    "major_version" / Int16ul,
    "minor_version" / Int16ul,
    "header_size" / Int32ul,
    "header_checksum" / Hex(Bytes(32)),
    "tables_size" / Int32ul,
    "table_checksum" / Hex(Bytes(32)),
    "partitions" / LpMetadataTableDescriptor,
    "extents" / LpMetadataTableDescriptor,
    "groups" / LpMetadataTableDescriptor,
    "block_devices" / LpMetadataTableDescriptor,
    # Android R, v10.2
    "flags" / If(this.minor_version >= 2, Int32ul),
    If(this.minor_version >= 2, Padding(124)),
)

LpMetadataPartition = Struct(
    "name" / PaddedString(36, "ascii"),
    "attributes" / Int32ul,
    "first_extent_index" / Int32ul,
    "num_extents" / Int32ul,
    "group_index" / Int32ul
)

LpMetadataExtent = Struct(
    "num_sectors" / Int64ul,
    "target_type" / Enum(Int32ul,
                         DM_LINEAR=0,
                         DM_ZERO=1),
    "target_data" / Int64ul,
    "target_source" / Int32ul
)

LpMetadataPartitionGroup = Struct(
    "name" / PaddedString(36, "ascii"),
    "flags" / Int32ul,
    "maximum_size" / Int64ul
)

LpMetadataBlockDevice = Struct(
    "first_logic_sector" / Int64ul,
    "alignment" / Int32ul,
    "alignment_offset" / Int32ul,
    "size" / Int64ul,
    "partition_name" / PaddedString(36, "ascii"),
    "flags" / Int32ul
)

LpMetaData = Struct(
    "header" / LpMetadataHeader,
    "partitions" / Array(this.header.partitions.num_entries, LpMetadataPartition),
    "extents" / Array(this.header.extents.num_entries, LpMetadataExtent),
    "groups" / Array(this.header.groups.num_entries, LpMetadataPartitionGroup),
    "devices" / Array(this.header.block_devices.num_entries, LpMetadataBlockDevice),
)

"""
LpMetaLayout = Struct(
    Bytes(LP_PARTITION_RESERVED_BYTES),
    "gemometry" / Padded(LP_GEOMETRY_SIZE, LpMetadataGeometry),
    "gemometry_backup" / Padded(LP_GEOMETRY_SIZE, LpMetadataGeometry),
    "metadata" / Padded(LP_METADATA_SIZE, LpMetaData),
    "metadata_backup" / Padded(LP_METADATA_SIZE, LpMetaData),
)
"""
LpMetaLayout = Struct(
    Bytes(LP_PARTITION_RESERVED_BYTES),
    "gemometry" / Padded(LP_GEOMETRY_SIZE, LpMetadataGeometry),
    "gemometry_backup" / Padded(LP_GEOMETRY_SIZE, LpMetadataGeometry),
    "metadata" / Padded(LP_METADATA_SIZE, LpMetaData),
    # "metadata_backup" / Array(this.gemometry.metadata_slot_count * 2 - 1, Padded(LP_METADATA_SIZE, LpMetaData))
    Bytes((this.gemometry.metadata_slot_count * 2 - 1) * LP_METADATA_SIZE)
)

def parse_metadata(filename):
    with open(filename, 'rb') as f:
        data = f.read(0x300000)
        meta = LpMetaLayout.parse(data)
        print(meta)


if __name__ == "__main__":
    # parse_metadata(r"data/super-raw-meta-1.0-q.bin")
    parse_metadata(r"data/super-raw-meta-1.2-r.bin")
