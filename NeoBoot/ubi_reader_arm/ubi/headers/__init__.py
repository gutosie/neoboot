#!/usr/bin/python
import struct
from ubi.defines import *
from ubi.headers import errors

class ec_hdr(object):

    def __init__(self, buf):
        fields = dict(zip(EC_HDR_FIELDS, struct.unpack(EC_HDR_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

        setattr(self, 'errors', [])

    def __repr__(self):
        return 'Error Count Header'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class vid_hdr(object):

    def __init__(self, buf):
        fields = dict(zip(VID_HDR_FIELDS, struct.unpack(VID_HDR_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

        setattr(self, 'errors', [])

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))

    def __repr__(self):
        return 'VID Header'


class vtbl_rec(object):

    def __init__(self, buf):
        fields = dict(zip(VTBL_REC_FIELDS, struct.unpack(VTBL_REC_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

        setattr(self, 'errors', [])
        setattr(self, 'rec_index', -1)

    def __repr__(self):
        return 'Volume Table Record: %s' % getattr(self, 'name')

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


def extract_ec_hdr(buf):
    ec_hdr_buf = buf
    ec_hdr_ret = ec_hdr(ec_hdr_buf)
    errors.ec_hdr(ec_hdr_ret, ec_hdr_buf)
    return ec_hdr_ret


def extract_vid_hdr(buf):
    vid_hdr_buf = buf
    vid_hdr_ret = vid_hdr(vid_hdr_buf)
    errors.vid_hdr(vid_hdr_ret, vid_hdr_buf)
    return vid_hdr_ret


def extract_vtbl_rec(buf):
    data_buf = buf
    vtbl_recs = []
    vtbl_rec_ret = ''
    for i in range(0, UBI_MAX_VOLUMES):
        offset = i * UBI_VTBL_REC_SZ
        vtbl_rec_buf = data_buf[offset:offset + UBI_VTBL_REC_SZ]
        if len(vtbl_rec_buf) == UBI_VTBL_REC_SZ:
            vtbl_rec_ret = vtbl_rec(vtbl_rec_buf)
            errors.vtbl_rec(vtbl_rec_ret, vtbl_rec_buf)
            if len(vtbl_rec_ret.errors) == 0:
                vtbl_rec_ret.rec_index = i
                vtbl_recs.append(vtbl_rec_ret)

    return vtbl_recs