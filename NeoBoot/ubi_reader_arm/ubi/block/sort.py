#!/usr/bin/python
def list_by_list(blist, slist):
    slist_blocks = []
    for block in blist:
        if block in slist:
            slist_blocks.append(block)

    return slist_blocks


def by_image_seq(blocks, image_seq):
    seq_blocks = []
    for block in blocks:
        if blocks[block].ec_hdr.image_seq == image_seq:
            seq_blocks.append(block)

    return seq_blocks


def by_range(blocks, block_range):
    peb_range = range(block_range[0], block_range[1])
    return [ i for i in blocks if i in peb_range ]


def by_leb(blocks):
    slist_len = len(blocks)
    slist = ['x'] * slist_len
    for block in blocks:
        if blocks[block].leb_num >= slist_len:
            add_elements = blocks[block].leb_num - slist_len + 1
            slist += ['x'] * add_elements
            slist_len = len(slist)
        slist[blocks[block].leb_num] = block

    return slist
    return sorted(blocks.iterkeys(), key=lambda x: blocks[x].leb_num)


def by_vol_id(blocks, slist = None):
    vol_blocks = {}
    for i in blocks:
        if slist and i not in slist:
            continue
        elif not blocks[i].is_valid:
            continue
        if blocks[i].vid_hdr.vol_id not in vol_blocks:
            vol_blocks[blocks[i].vid_hdr.vol_id] = []
        vol_blocks[blocks[i].vid_hdr.vol_id].append(blocks[i].peb_num)

    return vol_blocks


def clean_bad(blocks, slist = None):
    clean_blocks = []
    for i in range(0, len(blocks)):
        if slist and i not in slist:
            continue
        if blocks[i].is_valid:
            clean_blocks.append(i)

    return clean_blocks


def by_type(blocks, slist = None):
    layout = []
    data = []
    int_vol = []
    unknown = []
    for i in blocks:
        if slist and i not in slist:
            continue
        if blocks[i].is_vtbl and blocks[i].is_valid:
            layout.append(i)
        elif blocks[i].is_internal_vol and blocks[i].is_valid:
            int_vol.append(i)
        elif blocks[i].is_valid:
            data.append(i)
        else:
            unknown.append(i)

    return (layout,
     data,
     int_vol,
     unknown)