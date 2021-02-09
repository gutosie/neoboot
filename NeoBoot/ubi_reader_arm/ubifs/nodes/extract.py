#!/usr/bin/python
from ubifs import nodes
from ubifs.defines import *

def common_hdr(ubifs, lnum, offset = 0):
    ubifs.file.seek(ubifs.leb_size * lnum + offset)
    return nodes.common_hdr(ubifs.file.read(UBIFS_COMMON_HDR_SZ))


def ino_node(ubifs, lnum, offset = 0):
    ubifs.file.seek(ubifs.leb_size * lnum + offset)
    inon = nodes.ino_node(ubifs.file.read(UBIFS_INO_NODE_SZ))
    inon.data = ubifs.file.read(inon.data_len)
    return inon


def mst_node(ubifs, lnum, offset = 0):
    ubifs.file.seek(ubifs.leb_size * lnum + offset)
    return nodes.mst_node(ubifs.file.read(UBIFS_MST_NODE_SZ))


def sb_node(ubifs, offset = 0):
    ubifs.file.seek(offset)
    return nodes.sb_node(ubifs.file.read(UBIFS_SB_NODE_SZ))


def dent_node(ubifs, lnum, offset = 0):
    ubifs.file.seek(ubifs.leb_size * lnum + offset)
    den = nodes.dent_node(ubifs.file.read(UBIFS_DENT_NODE_SZ))
    den.name = '%s' % ubifs.file.read(den.nlen)
    return den


def data_node(ubifs, lnum, offset = 0, node_len = 0):
    ubifs.file.seek(ubifs.leb_size * lnum + offset)
    datn = nodes.data_node(ubifs.file.read(UBIFS_DATA_NODE_SZ))
    datn.offset = ubifs.leb_size * lnum + offset + UBIFS_DATA_NODE_SZ
    datn.compr_len = node_len - UBIFS_COMMON_HDR_SZ - UBIFS_DATA_NODE_SZ
    return datn


def idx_node(ubifs, lnum, offset = 0):
    ubifs.file.seek(ubifs.leb_size * lnum + offset)
    idxn = nodes.idx_node(ubifs.file.read(UBIFS_IDX_NODE_SZ))
    for i in range(0, idxn.child_cnt):
        idxn.branches.append(nodes.branch(ubifs.file.read(UBIFS_BRANCH_SZ)))

    return idxn