#!/usr/bin/python
import struct
UBIFS_NODE_MAGIC = '1\x18\x10\x06'
UBIFS_CRC32_INIT = 4294967295L
UBIFS_MIN_COMPR_LEN = 128
UBIFS_MIN_COMPRESS_DIFF = 64
UBIFS_ROOT_INO = 1
UBIFS_FIRST_INO = 64
UBIFS_MAX_NLEN = 255
UBIFS_MAX_JHEADS = 1
UBIFS_BLOCK_SIZE = 4096
UBIFS_BLOCK_SHIFT = 12
UBIFS_PADDING_BYTE = '\xce'
UBIFS_MAX_KEY_LEN = 16
UBIFS_SK_LEN = 8
UBIFS_MIN_FANOUT = 3
UBIFS_MAX_LEVELS = 512
UBIFS_MAX_INO_DATA = UBIFS_BLOCK_SIZE
UBIFS_LPT_FANOUT = 4
UBIFS_LPT_FANOUT_SHIFT = 2
UBIFS_LPT_CRC_BITS = 16
UBIFS_LPT_CRC_BYTES = 2
UBIFS_LPT_TYPE_BITS = 4
UBIFS_LPT_PNODE = 0
UBIFS_LPT_NNODE = 1
UBIFS_LPT_LTAB = 2
UBIFS_LPT_LSAVE = 3
UBIFS_LPT_NODE_CNT = 4
UBIFS_LPT_NOT_A_NODE = (1 << UBIFS_LPT_TYPE_BITS) - 1
UBIFS_ITYPE_REG = 0
UBIFS_ITYPE_DIR = 1
UBIFS_ITYPE_LNK = 2
UBIFS_ITYPE_BLK = 3
UBIFS_ITYPE_CHR = 4
UBIFS_ITYPE_FIFO = 5
UBIFS_ITYPE_SOCK = 6
UBIFS_ITYPES_CNT = 7
UBIFS_KEY_HASH_R5 = 0
UBIFS_KEY_HASH_TEST = 1
PRINT_UBIFS_KEY_HASH = ['r5', 'test']
UBIFS_SIMPLE_KEY_FMT = 0
UBIFS_S_KEY_BLOCK_BITS = 29
UBIFS_S_KEY_BLOCK_MASK = 536870911
UBIFS_S_KEY_HASH_BITS = UBIFS_S_KEY_BLOCK_BITS
UBIFS_S_KEY_HASH_MASK = UBIFS_S_KEY_BLOCK_MASK
UBIFS_INO_KEY = 0
UBIFS_DATA_KEY = 1
UBIFS_DENT_KEY = 2
UBIFS_XENT_KEY = 3
UBIFS_KEY_TYPES_CNT = 4
UBIFS_SB_LEBS = 1
UBIFS_MST_LEBS = 2
UBIFS_SB_LNUM = 0
UBIFS_MST_LNUM = UBIFS_SB_LNUM + UBIFS_SB_LEBS
UBIFS_LOG_LNUM = UBIFS_MST_LNUM + UBIFS_MST_LEBS
UBIFS_COMPR_FL = 1
UBIFS_SYNC_FL = 2
UBIFS_IMMUTABLE_FL = 4
UBIFS_APPEND_FL = 8
UBIFS_DIRSYNC_FL = 16
UBIFS_XATTR_FL = 32
UBIFS_FL_MASK = 31
UBIFS_COMPR_NONE = 0
UBIFS_COMPR_LZO = 1
UBIFS_COMPR_ZLIB = 2
UBIFS_COMPR_TYPES_CNT = 3
PRINT_UBIFS_COMPR = ['none', 'lzo', 'zlib']
UBIFS_INO_NODE = 0
UBIFS_DATA_NODE = 1
UBIFS_DENT_NODE = 2
UBIFS_XENT_NODE = 3
UBIFS_TRUN_NODE = 4
UBIFS_PAD_NODE = 5
UBIFS_SB_NODE = 6
UBIFS_MST_NODE = 7
UBIFS_REF_NODE = 8
UBIFS_IDX_NODE = 9
UBIFS_CS_NODE = 10
UBIFS_ORPH_NODE = 11
UBIFS_NODE_TYPES_CNT = 12
UBIFS_MST_DIRTY = 1
UBIFS_MST_NO_ORPHS = 2
UBIFS_MST_RCVRY = 4
UBIFS_NO_NODE_GROUP = 0
UBIFS_IN_NODE_GROUP = 1
UBIFS_LAST_OF_NODE_GROUP = 2
UBIFS_FLG_BIGLPT = 2
UBIFS_FLG_SPACE_FIXUP = 4
UBIFS_COMMON_HDR_FORMAT = '<IIQIBB2s'
UBIFS_COMMON_HDR_FIELDS = ['magic',
 'crc',
 'sqnum',
 'len',
 'node_type',
 'group_type',
 'padding']
UBIFS_COMMON_HDR_SZ = struct.calcsize(UBIFS_COMMON_HDR_FORMAT)
UBIFS_KEY_OFFSET = UBIFS_COMMON_HDR_SZ
UBIFS_DEV_DESC_FORMAT = '<IQ'
UBIFS_DEV_DESC_FIELDS = ['new', 'huge']
UBIFS_DEV_DESC_SZ = struct.calcsize(UBIFS_DEV_DESC_FORMAT)
UBIFS_INO_NODE_FORMAT = '<%ssQQQQQIIIIIIIIIII4sIH26s' % UBIFS_MAX_KEY_LEN
UBIFS_INO_NODE_FIELDS = ['key',
 'creat_sqnum',
 'size',
 'atime_sec',
 'ctime_sec',
 'mtime_sec',
 'atime_nsec',
 'ctime_nsec',
 'mtime_nsec',
 'nlink',
 'uid',
 'gid',
 'mode',
 'flags',
 'data_len',
 'xattr_cnt',
 'xattr_size',
 'padding1',
 'xattr_names',
 'compr_type',
 'padding2']
UBIFS_INO_NODE_SZ = struct.calcsize(UBIFS_INO_NODE_FORMAT)
UBIFS_DENT_NODE_FORMAT = '<%ssQBBH4s' % UBIFS_MAX_KEY_LEN
UBIFS_DENT_NODE_FIELDS = ['key',
 'inum',
 'padding1',
 'type',
 'nlen',
 'padding2']
UBIFS_DENT_NODE_SZ = struct.calcsize(UBIFS_DENT_NODE_FORMAT)
UBIFS_DATA_NODE_FORMAT = '<%ssIH2s' % UBIFS_MAX_KEY_LEN
UBIFS_DATA_NODE_FIELDS = ['key',
 'size',
 'compr_type',
 'padding']
UBIFS_DATA_NODE_SZ = struct.calcsize(UBIFS_DATA_NODE_FORMAT)
UBIFS_TRUN_NODE_FORMAT = '<I12sQQ'
UBIFS_TRUN_NODE_FIELDS = ['inum',
 'padding',
 'old_size',
 'new_size']
UBIFS_TRUN_NODE_SZ = struct.calcsize(UBIFS_TRUN_NODE_FORMAT)
UBIFS_PAD_NODE_FORMAT = '<I'
UBIFS_PAD_NODE_FIELDS = ['pad_len']
UBIFS_PAD_NODE_SZ = struct.calcsize(UBIFS_PAD_NODE_FORMAT)
UBIFS_SB_NODE_FORMAT = '<2sBBIIIIIQIIIIIIIH2sIIQI16sI3968s'
UBIFS_SB_NODE_FIELDS = ['padding',
 'key_hash',
 'key_fmt',
 'flags',
 'min_io_size',
 'leb_size',
 'leb_cnt',
 'max_leb_cnt',
 'max_bud_bytes',
 'log_lebs',
 'lpt_lebs',
 'orph_lebs',
 'jhead_cnt',
 'fanout',
 'lsave_cnt',
 'fmt_version',
 'default_compr',
 'padding1',
 'rp_uid',
 'rp_gid',
 'rp_size',
 'time_gran',
 'uuid',
 'ro_compat_version',
 'padding2']
UBIFS_SB_NODE_SZ = struct.calcsize(UBIFS_SB_NODE_FORMAT)
UBIFS_MST_NODE_FORMAT = '<QQIIIIIIIIQQQQQQIIIIIIIIIIII344s'
UBIFS_MST_NODE_FIELDS = ['highest_inum',
 'cmt_no',
 'flags',
 'log_lnum',
 'root_lnum',
 'root_offs',
 'root_len',
 'gc_lnum',
 'ihead_lnum',
 'ihead_offs',
 'index_size',
 'total_free',
 'total_dirty',
 'total_used',
 'total_dead',
 'total_dark',
 'lpt_lnum',
 'lpt_offs',
 'nhead_lnum',
 'nhead_offs',
 'ltab_lnum',
 'ltab_offs',
 'lsave_lnum',
 'lsave_offs',
 'lscan_lnum',
 'empty_lebs',
 'idx_lebs',
 'leb_cnt',
 'padding']
UBIFS_MST_NODE_SZ = struct.calcsize(UBIFS_MST_NODE_FORMAT)
UBIFS_REF_NODE_FORMAT = '<III28s'
UBIFS_REF_NODE_FIELDS = ['lnum',
 'offs',
 'jhead',
 'padding']
UBIFS_REF_NODE_SZ = struct.calcsize(UBIFS_REF_NODE_FORMAT)
UBIFS_BRANCH_FORMAT = '<III%ss' % UBIFS_SK_LEN
UBIFS_BRANCH_FIELDS = ['lnum',
 'offs',
 'len',
 'key']
UBIFS_BRANCH_SZ = struct.calcsize(UBIFS_BRANCH_FORMAT)
UBIFS_IDX_NODE_FORMAT = '<HH'
UBIFS_IDX_NODE_FIELDS = ['child_cnt', 'level']
UBIFS_IDX_NODE_SZ = struct.calcsize(UBIFS_IDX_NODE_FORMAT)
FILE_CHUNK_SZ = 5242880