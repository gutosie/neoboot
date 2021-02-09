#!/usr/bin/python
import struct
UBI_CRC32_INIT = 4294967295L
UBI_MAX_VOLUMES = 128
UBI_INTERNAL_VOL_START = 2147479551
UBI_EC_HDR_MAGIC = 'UBI#'
EC_HDR_FORMAT = '>4sB3sQIII32sI'
EC_HDR_FIELDS = ['magic',
 'version',
 'padding',
 'ec',
 'vid_hdr_offset',
 'data_offset',
 'image_seq',
 'padding2',
 'hdr_crc']
UBI_EC_HDR_SZ = struct.calcsize(EC_HDR_FORMAT)
UBI_VID_HDR_MAGIC = 'UBI!'
VID_HDR_FORMAT = '>4sBBBBII4sIIII4sQ12sI'
VID_HDR_FIELDS = ['magic',
 'version',
 'vol_type',
 'copy_flag',
 'compat',
 'vol_id',
 'lnum',
 'padding',
 'data_size',
 'used_ebs',
 'data_pad',
 'data_crc',
 'padding2',
 'sqnum',
 'padding3',
 'hdr_crc']
UBI_VID_HDR_SZ = struct.calcsize(VID_HDR_FORMAT)
VTBL_REC_FORMAT = '>IIIBBH128sB23sI'
VTBL_REC_FIELDS = ['reserved_pebs',
 'alignment',
 'data_pad',
 'vol_type',
 'upd_marker',
 'name_len',
 'name',
 'flags',
 'padding',
 'crc']
UBI_VTBL_REC_SZ = struct.calcsize(VTBL_REC_FORMAT)
UBI_VID_DYNAMIC = 1
UBI_VID_STATIC = 2
PRINT_VOL_TYPE_LIST = [0, 'dynamic', 'static']
UBI_VTBL_AUTORESIZE_FLG = 1
UBI_COMPAT_DELETE = 1
UBI_COMPAT_RO = 2
UBI_COMPAT_PRESERVE = 4
UBI_COMPAT_REJECT = 5
PRINT_COMPAT_LIST = [0,
 'Delete',
 'Read Only',
 0,
 'Preserve',
 'Reject']
FILE_CHUNK_SZ = 5242880