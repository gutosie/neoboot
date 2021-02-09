#!/usr/bin/python
import lzo
import struct
import zlib
from ubifs.defines import *
ino_types = ['file',
 'dir',
 'lnk',
 'blk',
 'chr',
 'fifo',
 'sock']
node_types = ['ino',
 'data',
 'dent',
 'xent',
 'trun',
 'pad',
 'sb',
 'mst',
 'ref',
 'idx',
 'cs',
 'orph']
key_types = ['ino',
 'data',
 'dent',
 'xent']

def parse_key(key):
    hkey, lkey = struct.unpack('<II', key[0:UBIFS_SK_LEN])
    ino_num = hkey & UBIFS_S_KEY_HASH_MASK
    key_type = lkey >> UBIFS_S_KEY_BLOCK_BITS
    khash = lkey
    return {'type': key_type,
     'ino_num': ino_num,
     'khash': khash}


def decompress(ctype, unc_len, data):
    if ctype == UBIFS_COMPR_LZO:
        return lzo.decompress(''.join(('\xf0', struct.pack('>I', unc_len), data)))
    elif ctype == UBIFS_COMPR_ZLIB:
        return zlib.decompress(data, -11)
    else:
        return data