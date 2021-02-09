#!/usr/bin/python
import re
import struct
from ubifs.defines import *
from ubifs import nodes
from ubifs.nodes import extract
from ubifs.log import log

class ubifs:

    def __init__(self, ubifs_file):
        self.log = log()
        self._file = ubifs_file
        self._sb_node = extract.sb_node(self, UBIFS_COMMON_HDR_SZ)
        self._min_io_size = self._sb_node.min_io_size
        self._leb_size = self._sb_node.leb_size
        self._mst_node = extract.mst_node(self, 1, UBIFS_COMMON_HDR_SZ)
        self._mst_node = extract.mst_node(self, 2, UBIFS_COMMON_HDR_SZ)

    def _get_file(self):
        return self._file

    file = property(_get_file)

    def _get_superblock(self):
        return self._sb_node

    superblock_node = property(_get_superblock)

    def _get_master_node(self):
        return self._mst_node

    master_node = property(_get_master_node)

    def _get_master_node2(self):
        return self._mst_node

    master_node2 = property(_get_master_node2)

    def _get_leb_size(self):
        return self._leb_size

    leb_size = property(_get_leb_size)

    def _get_min_io_size(self):
        return self._min_io_size

    min_io_size = property(_get_min_io_size)


def get_leb_size(path):
    f = open(path, 'rb')
    f.seek(0, 2)
    file_size = f.tell() + 1
    f.seek(0)
    block_size = 0
    for i in range(0, file_size, FILE_CHUNK_SZ):
        buf = f.read(FILE_CHUNK_SZ)
        for m in re.finditer(UBIFS_NODE_MAGIC, buf):
            start = m.start()
            chdr = nodes.common_hdr(buf[start:start + UBIFS_COMMON_HDR_SZ])
            if chdr and chdr.node_type == UBIFS_SB_NODE:
                sb_start = start + UBIFS_COMMON_HDR_SZ
                sb_end = sb_start + UBIFS_SB_NODE_SZ
                if chdr.len != len(buf[sb_start:sb_end]):
                    f.seek(sb_start)
                    buf = f.read(UBIFS_SB_NODE_SZ)
                else:
                    buf = buf[sb_start:sb_end]
                sbn = nodes.sb_node(buf)
                block_size = sbn.leb_size
                f.close()
                return block_size

    f.close()
    return block_size