#!/usr/bin/python
from ubifs import extract
from ubifs.defines import *

def index(ubifs, lnum, offset, inodes = {}):
    chdr = extract.common_hdr(ubifs, lnum, offset)
    if chdr.node_type == UBIFS_IDX_NODE:
        idxn = extract.idx_node(ubifs, lnum, offset + UBIFS_COMMON_HDR_SZ)
        for branch in idxn.branches:
            index(ubifs, branch.lnum, branch.offs, inodes)

    elif chdr.node_type == UBIFS_INO_NODE:
        inon = extract.ino_node(ubifs, lnum, offset + UBIFS_COMMON_HDR_SZ)
        ino_num = inon.key['ino_num']
        if ino_num not in inodes:
            inodes[ino_num] = {}
        inodes[ino_num]['ino'] = inon
    elif chdr.node_type == UBIFS_DATA_NODE:
        datn = extract.data_node(ubifs, lnum, offset + UBIFS_COMMON_HDR_SZ, chdr.len)
        ino_num = datn.key['ino_num']
        if ino_num not in inodes:
            inodes[ino_num] = {}
        if 'data' not in inodes[ino_num]:
            inodes[ino_num]['data'] = []
        inodes[ino_num]['data'].append(datn)
    elif chdr.node_type == UBIFS_DENT_NODE:
        dn = extract.dent_node(ubifs, lnum, offset + UBIFS_COMMON_HDR_SZ)
        ino_num = dn.key['ino_num']
        if ino_num not in inodes:
            inodes[ino_num] = {}
        if 'dent' not in inodes[ino_num]:
            inodes[ino_num]['dent'] = []
        inodes[ino_num]['dent'].append(dn)