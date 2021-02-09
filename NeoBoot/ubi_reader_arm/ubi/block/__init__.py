#!/usr/bin/python
import re
from ubi import display
from ubi.defines import *
from ubi.headers import *

class description(object):

    def __init__(self, block_buf):
        self.file_offset = -1
        self.peb_num = -1
        self.leb_num = -1
        self.size = -1
        self.vid_hdr = None
        self.is_internal_vol = False
        self.vtbl_recs = []
        self.ec_hdr = extract_ec_hdr(block_buf[0:UBI_EC_HDR_SZ])
        if not self.ec_hdr.errors:
            self.vid_hdr = extract_vid_hdr(block_buf[self.ec_hdr.vid_hdr_offset:self.ec_hdr.vid_hdr_offset + UBI_VID_HDR_SZ])
            self.is_internal_vol = self.vid_hdr.vol_id >= UBI_INTERNAL_VOL_START
            if self.vid_hdr.vol_id >= UBI_INTERNAL_VOL_START:
                self.vtbl_recs = extract_vtbl_rec(block_buf[self.ec_hdr.data_offset:])
            self.leb_num = self.vid_hdr.lnum
        self.is_vtbl = bool(self.vtbl_recs) or False
        self.is_valid = not self.ec_hdr.errors and not self.vid_hdr.errors
        return

    def __repr__(self):
        return 'Block: PEB# %s: LEB# %s' % (self.peb_num, self.leb_num)

    def display(self, tab = ''):
        display.block(self, tab)


def get_blocks_in_list(blocks, idx_list):
    return {i:blocks[i] for i in idx_list}


def extract_blocks(ubi):
    blocks = {}
    start_peb = 0
    ubi.file.seek(ubi.file.start_offset)
    peb_count = 0
    cur_offset = 0
    for i in range(ubi.file.start_offset, ubi.file.end_offset, ubi.file.block_size):
        buf = ubi.file.read(ubi.file.block_size)
        if buf.startswith(UBI_EC_HDR_MAGIC):
            blk = description(buf)
            blk.file_offset = i
            blk.peb_num = ubi.first_peb_num + peb_count
            blk.size = ubi.file.block_size
            blocks[blk.peb_num] = blk
            peb_count += 1
        else:
            cur_offset += ubi.file.block_size
            ubi.first_peb_num = cur_offset / ubi.file.block_size
            ubi.file.start_offset = cur_offset

    return blocks