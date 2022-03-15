```
Output file out/target/product/b604usff/gpt.bin
total_disk_size 0x1c8000000
base_address 0x0
agpt_reserved_size 0x4200
partition 'macadr' start=0x4400, end=0x4400, attr=0x0 size=0x200
partition 'nvram' start=0x4600, end=0x14400, attr=0x0 size=0x10000
partition 'bsu' start=0x14600, end=0xffc00, attr=0x0 size=0xeb800
partition 'misc' start=0x100000, end=0x1ffe00, attr=0x0 size=0x100000
partition 'hwcfg' start=0x200000, end=0x2ffe00, attr=0x0 size=0x100000
partition 'splash' start=0x300000, end=0xeffe00, attr=0x0 size=0xc00000
partition 'eio' start=0xf00000, end=0x10ffe00, attr=0x0 size=0x200000
partition 'metadata' start=0x1100000, end=0x18ffe00, attr=0x0 size=0x800000
partition 'cache' start=0x1900000, end=0x22ffe00, attr=0x1000000000000 size=0xa00000
partition 'boot_i' start=0x2300000, end=0x62ffe00, attr=0x0 size=0x4000000
partition 'boot_e' start=0x6300000, end=0xa2ffe00, attr=0x0 size=0x4000000
partition 'system_i' start=0xa300000, end=0x42cffe00, attr=0x1000000000000 size=0x38a00000
partition 'system_e' start=0x42d00000, end=0x7b6ffe00, attr=0x1000000000000 size=0x38a00000
partition 'vendor_i' start=0x7b700000, end=0x81affe00, attr=0x1000000000000 size=0x6400000
partition 'vendor_e' start=0x81b00000, end=0x87effe00, attr=0x1000000000000 size=0x6400000
partition 'userdata' start=0x87f00000, end=0x1c7ffbc00, attr=0x1000000000000 size=0x1400fbe00
Wrote primary GPT table 'out/target/product/b604usff/gpt.bin'

Primary GPT
signature                    0x5452415020494645
revision                     0x00010000
header_size                  92
header_crc32                 0x120003d3
my_lba                       0x00000001  (0x00000200)
alternate_lba                0x00e3ffff  (0x1c7fffe00)
first_usable_lba             0x00000006  (0x00000c00)
last_usable_lba              0x00e3fffa  (0x1c7fff400)
disk GUID                    b5863648db712119b2c1ff06cb889987
partition_entry_lba          0x00000002  (0x00000400)
num_partition_entries        16
sizeof_partition_entry       0x80
partition_entry_array_crc32  0xb2f78d20

Alternate GPT
signature                    0x5452415020494645
revision                     0x00010000
header_size                  92
header_crc32                 0x6068c6cf
my_lba                       0x00e3ffff  (0x1c7fffe00)
alternate_lba                0x00000001  (0x00000200)
first_usable_lba             0x00000006  (0x00000c00)
last_usable_lba              0x00e3fffa  (0x1c7fff400)
disk GUID                    b5863648db712119b2c1ff06cb889987
partition_entry_lba          0x00e3fffb  (0x1c7fff600)
num_partition_entries        16
sizeof_partition_entry       0x80
partition_entry_array_crc32  0xb2f78d20

Partition p1
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID 1f29ca942b2afede0d527d9c5c91558a
starting_lba     0x00000022   (0x00004400)
ending_lba       0x00000022   (0x00004400)
name             'macadr'

Partition p2
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID 6d8913a6e8e6d3a0339630ec4838d50f
starting_lba     0x00000023   (0x00004600)
ending_lba       0x000000a2   (0x00014400)
name             'nvram'

Partition p3
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID f12a319efe1841fa45f337b3bb1d1061
starting_lba     0x000000a3   (0x00014600)
ending_lba       0x000007fe   (0x000ffc00)
name             'bsu'

Partition p4
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID dbd0a5183ad2c1aa0d4c692c7ba9ab1c
starting_lba     0x00000800   (0x00100000)
ending_lba       0x00000fff   (0x001ffe00)
name             'misc'

Partition p5
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID 1c4acfebe7b9068f98853bd8b4a46cff
starting_lba     0x00001000   (0x00200000)
ending_lba       0x000017ff   (0x002ffe00)
name             'hwcfg'

Partition p6
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID eb95b4d5aa5770fc23bbd1897fa4e840
starting_lba     0x00001800   (0x00300000)
ending_lba       0x000077ff   (0x00effe00)
name             'splash'

Partition p7
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID 884d2fc099f1d31a3eedc538ac258b58
starting_lba     0x00007800   (0x00f00000)
ending_lba       0x000087ff   (0x010ffe00)
name             'eio'

Partition p8
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID 055b508ee98158cccb3ccf30e8090c01
starting_lba     0x00008800   (0x01100000)
ending_lba       0x0000c7ff   (0x018ffe00)
name             'metadata'

Partition p9
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID af4e852f80c347231b8f6ae6cacc5367
starting_lba     0x0000c800   (0x01900000)
ending_lba       0x000117ff   (0x022ffe00)
name             'cache'

Partition p10
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID 721c020b27a73a988c73b02d50707a2d
starting_lba     0x00011800   (0x02300000)
ending_lba       0x000317ff   (0x062ffe00)
name             'boot_i'

Partition p11
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID b227093c23746ffe6ab37b5fafc4076b
starting_lba     0x00031800   (0x06300000)
ending_lba       0x000517ff   (0x0a2ffe00)
name             'boot_e'

Partition p12
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID fe939aea410a746dd352af528d30d057
starting_lba     0x00051800   (0x0a300000)
ending_lba       0x002167ff   (0x42cffe00)
name             'system_i'

Partition p13
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID a6a43e3caa5e7c7f1cb79374b8191c5d
starting_lba     0x00216800   (0x42d00000)
ending_lba       0x003db7ff   (0x7b6ffe00)
name             'system_e'

Partition p14
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID 33c4b94306a1bf68aff4890416fc87d7
starting_lba     0x003db800   (0x7b700000)
ending_lba       0x0040d7ff   (0x81affe00)
name             'vendor_i'

Partition p15
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID cb0a9ec4381be595548a2b7260e704a4
starting_lba     0x0040d800   (0x81b00000)
ending_lba       0x0043f7ff   (0x87effe00)
name             'vendor_e'

Partition p16
Partition Type   GUID a2a0d0ebe5b9334487c068b6b72699c7
Unique Partition GUID bc7a4da66bda67db7ffdd11699c89f64
starting_lba     0x0043f800   (0x87f00000)
ending_lba       0x00e3ffde   (0x1c7ffbc00)
name             'userdata'
```