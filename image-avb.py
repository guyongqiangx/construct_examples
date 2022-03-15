import os

from construct import *

# external/avb/libavb/avb_vbmeta_image.h
# AvbVBMetaImageHeader 256 bytes
AvbVBMetaImageHeader = Struct(
    "magic" / Const(b"AVB0"),
    "required_libavb_version_major" / Int32ub,
    "required_libavb_version_minor" / Int32ub,
    "authentication_data_block_size" / Int64ub,
    "auxiliary_data_block_size" / Int64ub,
    "algorithm_type" / Int32ub,
    "hash_offset" / Int64ub,
    "hash_size" / Int64ub,
    "signature_offset" / Int64ub,
    "signature_size" / Int64ub,
    "public_key_offset" / Int64ub,
    "public_key_size" / Int64ub,
    "public_key_metadata_offset" / Int64ub,
    "public_key_metadata_size" / Int64ub,
    "descriptors_offset" / Int64ub,
    "descriptors_size" / Int64ub,
    "rollback_index" / Int64ub,
    "flags" / Int32ul,
    Bytes(4),  # Reserved
    "release_string" / PaddedString(48, "ascii"),
    Bytes(80)  # Padding
)

"""
# external/avb/libavb/avb_descriptor.h
AvbDescriptorTag = Enum(Int64ub,
                     property=0,
                     hashtree=1,
                     hash=2,
                     kernel_cmdline=3,
                     chain_partition=4
                     )
"""

AvbDescriptorHeader = Struct(
    "tag" / Enum(Int64ub,
                 PROPERTY=0,
                 HASHTREE=1,
                 HASH=2,
                 KERNEL_CMDLINE=3,
                 CHAIN_PARTITION=4
                 ),
    "num_bytes_following" / Int64ub
)

# external/avb/libavb/avb_property_descriptor.h
AvbPropertyDescriptor = Struct(
    # "parent_descriptor" / AvbDescriptor,  # tag = 0, size = 32
    "key_num_bytes" / Int64ub,
    "value_num_bytes" / Int64ub
)

# external/avb/libavb/avb_hashtree_descriptor.h
AvbHashtreeDescriptor = Struct(
    # "parent_descriptor" / AvbDescriptor,  # tag = 1, size = 120 + 60(reserved)
    "dm_verify_version" / Int32ub,
    "image_size" / Int64ub,
    "tree_offset" / Int64ub,
    "tree_size" / Int64ub,
    "data_block_size" / Int32ub,
    "hash_block_size" / Int32ub,
    "fec_num_roots" / Int32ub,
    "fec_offset" / Int64ub,
    "fec_size" / Int64ub,
    "hash_algorithm" / Bytes(32),
    "partition_name_len" / Int32ub,
    "salt_len" / Int32ub,
    "root_digest_len" / Int32ub,
    "flags" / Int32ub,
    Bytes(60)  # reserved[60]
)

# external/avb/libavb/avb_hash_descriptor.h
AvbHashDescriptor = Struct(
    # "parent_descriptor" / AvbDescriptor,  # tag = 2, size = 72 + 60(reserved)
    "image_size" / Int64ub,
    "hash_algorithm" / Bytes(32),
    "partition_name_len" / Int32ub,
    "salt_len" / Int32ub,
    "digest_len" / Int32ub,
    "flags" / Int32ub,
    Bytes(60)  # reserved[60]
)

# external/avb/libavb/avb_kernel_cmdline_descriptor.h
AvbKernelCmdlineDescriptor = Struct(
    # "parent_descriptor" / AvbDescriptor,  # tag = 3, size = 24
    "flags" / Int32ub,
    "kernel_cmdline_length" / Int32ub
)

# external/avb/libavb/avb_chain_partition_descriptor.h
AvbChainPartitionDescriptor = Struct(
    # "parent_descriptor" / AvbDescriptor,  # tag = 4, size = 28 + 64(reserved)
    "rollback_index_location" / Int32ub,
    "partition_name_len" / Int32ub,
    "public_key_len" / Int32ub,
    Bytes(64)  # reserved[64]
)


def AlignPadding(length, align):
    return If(length % align > 0, Padding(align - length % align))

AvbDescriptor = Struct(
    "parent_descriptor" / AvbDescriptorHeader,
    "data" / Switch(this.parent_descriptor.tag,
                          {
                              "PROPERTY": Struct(
                                  "descriptor" / AvbPropertyDescriptor,
                                  "key" / PaddedString(this.descriptor.key_num_bytes + 1, "ascii"),
                                  "value" / PaddedString(this.descriptor.value_num_bytes + 1, "ascii"),
                                  "length" / Computed(AvbPropertyDescriptor.sizeof() +
                                                      this.descriptor.key_num_bytes + 1 +
                                                      this.descriptor.value_num_bytes + 1),
                              ),
                              "HASHTREE": Struct(
                                  "descriptor" / AvbHashtreeDescriptor,
                                  "partition_name" / PaddedString(this.descriptor.partition_name_len, "utf8"),
                                  "salt" / Hex(Bytes(this.descriptor.salt_len)),
                                  "root_digest" / Hex(Bytes(this.descriptor.root_digest_len)),
                                  "length" / Computed(AvbHashtreeDescriptor.sizeof() +
                                                      this.descriptor.partition_name_len +
                                                      this.descriptor.salt_len +
                                                      this.descriptor.root_digest_len),
                              ),
                              "HASH": Struct(
                                  "descriptor" / AvbHashDescriptor,
                                  "partition_name" / PaddedString(this.descriptor.partition_name_len, "utf8"),
                                  "salt" / Hex(Bytes(this.descriptor.salt_len)),
                                  "digest" / Hex(Bytes(this.descriptor.digest_len)),
                                  "length" / Computed(AvbHashDescriptor.sizeof() +
                                                      this.descriptor.partition_name_len +
                                                      this.descriptor.salt_len +
                                                      this.descriptor.digest_len),
                              ),
                              "KERNEL_CMDLINE": Struct(
                                  "descriptor" / AvbKernelCmdlineDescriptor,
                                  "kernel_cmdline" / PaddedString(this.descriptor.kernel_cmdline_length, "utf8"),
                                  "length" / Computed(AvbKernelCmdlineDescriptor.sizeof() + this.descriptor.kernel_cmdline_length),
                              ),
                              "CHAIN_PARTITION": Struct(
                                  "descriptor" / AvbChainPartitionDescriptor,
                                  "partition_name" / PaddedString(this.descriptor.partition_name_len, "utf8"),
                                  "public_key" / Hex(Bytes(this.descriptor.public_key_len)),
                                  "length" / Computed(AvbChainPartitionDescriptor.sizeof() +
                                                      this.descriptor.partition_name_len +
                                                      this.descriptor.public_key_len),
                              ),
                          }),
    AlignPadding(this.data.length, 8),
    "size" / Computed(AvbDescriptorHeader.sizeof() + this.parent_descriptor.num_bytes_following)
)

AvbFooter = Struct(
    "magic" / Const(b'AVBf'),
    "version_major" / Int32ub,
    "version_minor" / Int32ub,
    "original_image_size" / Int64ub,
    "vbmeta_offset" / Int64ub,
    "vbmeta_size" / Int64ub,
    Bytes(28)   # reserved[28]
)


def parse_avbfooter_image_file(filename):
    print(AvbFooter.sizeof())
    with open(filename, "rb") as f:
        f.seek(0, os.SEEK_END)
        image_size = f.tell()
        f.seek(image_size - AvbFooter.sizeof())
        data = f.read(AvbFooter.sizeof())
        footer = AvbFooter.parse(data)
        print(footer)

        f.seek(footer.vbmeta_offset)
        data = f.read(footer.vbmeta_size)
        header = AvbVBMetaImageHeader.parse(data)
        print(header)

        auth_block_offset = footer.vbmeta_offset + AvbVBMetaImageHeader.sizeof()
        aux_block_offset  = auth_block_offset + header.authentication_data_block_size
        desc_start_offset = aux_block_offset + header.descriptors_offset

        f.seek(desc_start_offset)
        data = f.read(header.descriptors_size)
        descriptors = GreedyRange(AvbDescriptor).parse(data)
        for d in descriptors:
            print(d)


def parse_vbmeta_image_file(filename):
    with open(filename, "rb") as f:
        data = f.read(AvbVBMetaImageHeader.sizeof())
        # hexdump(data)
        header = AvbVBMetaImageHeader.parse(data)
        print(header)

        aux_block_offset = AvbVBMetaImageHeader.sizeof() + header.authentication_data_block_size
        desc_start_offset = aux_block_offset + header.descriptors_offset

        print("Descriptor Data, range [0x{:04x} - 0x{:04x}], {:d} bytes".format(desc_start_offset,
                                                               desc_start_offset + header.descriptors_size,
                                                               header.descriptors_size))
        f.seek(desc_start_offset)
        data = f.read(header.descriptors_size)
        # hexdump(data)

        AvbDescPattern = GreedyRange(RawCopy(AvbDescriptor))
        descriptors = AvbDescPattern.parse(data)
        for d in descriptors:
            # hexdump(d.data)
            print(d.value)


def hexdump(data, line_size=16, indent=0, prefix=""):
    for i in range(len(data)):
        if i % line_size == 0:
            print("{}{}".format(" " * indent, prefix), end="")
        print("{:02X} ".format(data[i]), end="")
        if i % line_size == (line_size - 1) or i == len(data) - 1:
            print("", end="\n")


if __name__ == "__main__":
    # parse_avbfooter_image_file("data/dtbo.avb.img")
    parse_vbmeta_image_file("data/vbmeta.img")
