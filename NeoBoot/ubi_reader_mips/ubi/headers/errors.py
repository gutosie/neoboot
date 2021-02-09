#!/usr/bin/python
from zlib import crc32
from ubi.defines import *

def ec_hdr(ec_hdr, buf):
    if ec_hdr.hdr_crc != ~crc32(buf[:-4]) & 4294967295L:
        ec_hdr.errors.append('crc')
    return ec_hdr


def vid_hdr(vid_hdr, buf):
    vid_hdr.errors = []
    if vid_hdr.hdr_crc != ~crc32(buf[:-4]) & 4294967295L:
        vid_hdr.errors.append('crc')
    return vid_hdr


def vtbl_rec(vtbl_rec, buf):
    likely_vtbl = True
    if vtbl_rec.name_len != len(vtbl_rec.name.strip('\x00')):
        likely_vtbl = False
    elif vtbl_rec.vol_type not in (1, 2):
        likely_vtbl = False
    if vtbl_rec.crc != ~crc32(buf[:-4]) & 4294967295L:
        vtbl_rec.errors.append('crc')
    if not likely_vtbl:
        vtbl_rec.errors = ['False']
    return vtbl_rec