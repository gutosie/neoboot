#!/usr/bin/python
import struct
from ubifs.defines import *
from ubifs.misc import parse_key

class common_hdr(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_COMMON_HDR_FIELDS, struct.unpack(UBIFS_COMMON_HDR_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

        setattr(self, 'errors', [])

    def __repr__(self):
        return 'UBIFS Common Header'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class sb_node(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_SB_NODE_FIELDS, struct.unpack(UBIFS_SB_NODE_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

    def __repr__(self):
        return 'UBIFS Super Block Node'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class mst_node(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_MST_NODE_FIELDS, struct.unpack(UBIFS_MST_NODE_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

    def __repr__(self):
        return 'UBIFS Master Block Node'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class dent_node(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_DENT_NODE_FIELDS, struct.unpack(UBIFS_DENT_NODE_FORMAT, buf)))
        for key in fields:
            if key == 'key':
                setattr(self, key, parse_key(fields[key]))
            else:
                setattr(self, key, fields[key])

        setattr(self, 'name', '')

    def __repr__(self):
        return 'UBIFS Directory Entry Node'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class data_node(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_DATA_NODE_FIELDS, struct.unpack(UBIFS_DATA_NODE_FORMAT, buf)))
        for key in fields:
            if key == 'key':
                setattr(self, key, parse_key(fields[key]))
            else:
                setattr(self, key, fields[key])

        setattr(self, 'offset', 0)
        setattr(self, 'compr_len', 0)

    def __repr__(self):
        return 'UBIFS Data Node'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class idx_node(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_IDX_NODE_FIELDS, struct.unpack(UBIFS_IDX_NODE_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

        setattr(self, 'branches', [])

    def __repr__(self):
        return 'UBIFS Index Node'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class ino_node(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_INO_NODE_FIELDS, struct.unpack(UBIFS_INO_NODE_FORMAT, buf)))
        for key in fields:
            if key == 'key':
                setattr(self, key, parse_key(fields[key]))
            else:
                setattr(self, key, fields[key])

        setattr(self, 'data', '')

    def __repr__(self):
        return 'UBIFS Ino Node'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))


class branch(object):

    def __init__(self, buf):
        fields = dict(zip(UBIFS_BRANCH_FIELDS, struct.unpack(UBIFS_BRANCH_FORMAT, buf)))
        for key in fields:
            setattr(self, key, fields[key])

    def __repr__(self):
        return 'UBIFS Branch'

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                yield (key, getattr(self, key))