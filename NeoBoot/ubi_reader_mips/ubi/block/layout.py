#!/usr/bin/python
from ubi.block import sort

def group_pairs(blocks, layout_blocks_list):
    layouts_grouped = [[blocks[layout_blocks_list[0]].peb_num]]
    for l in layout_blocks_list[1:]:
        for lnd in layouts_grouped:
            if blocks[l].vtbl_recs[0].name == blocks[lnd[0]].vtbl_recs[0].name:
                lnd.append(blocks[l].peb_num)
                break
        else:
            layouts_grouped.append([blocks[l].peb_num])

    return layouts_grouped


def associate_blocks(blocks, layout_pairs, start_peb_num):
    seq_blocks = []
    for layout_pair in layout_pairs:
        seq_blocks = sort.by_image_seq(blocks, blocks[layout_pair[0]].ec_hdr.image_seq)
        layout_pair.append(seq_blocks)

    return layout_pairs