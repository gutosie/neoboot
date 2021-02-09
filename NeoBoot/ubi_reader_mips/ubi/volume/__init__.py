#!/usr/bin/python
from ubi import display
from ubi.block import sort, get_blocks_in_list

class description(object):

    def __init__(self, vol_id, vol_rec, block_list):
        self._vol_id = vol_id
        self._vol_rec = vol_rec
        self._name = self._vol_rec.name
        self._block_list = block_list

    def __repr__(self):
        return 'Volume: %s' % self.name

    def _get_name(self):
        return self._name

    name = property(_get_name)

    def _get_vol_id(self):
        return self._vol_id

    vol_id = property(_get_vol_id)

    def _get_block_count(self):
        return len(self._block_list)

    block_count = property(_get_block_count)

    def _get_vol_rec(self):
        return self._vol_rec

    vol_rec = property(_get_vol_rec)

    def _get_block_list(self):
        return self._block_list

    block_list = property(_get_block_list)

    def get_blocks(self, blocks):
        return get_blocks_in_list(blocks, self._block_list)

    def display(self, tab = ''):
        display.volume(self, tab)

    def reader(self, ubi):
        last_leb = 0
        for block in sort.by_leb(self.get_blocks(ubi.blocks)):
            if block == 'x':
                last_leb += 1
                yield '\xff' * ubi.leb_size
            else:
                last_leb += 1
                yield ubi.file.read_block_data(ubi.blocks[block])


def get_volumes(blocks, layout_info):
    volumes = {}
    vol_blocks_lists = sort.by_vol_id(blocks, layout_info[2])
    for vol_rec in blocks[layout_info[0]].vtbl_recs:
        vol_name = vol_rec.name.strip('\x00')
        if vol_rec.rec_index not in vol_blocks_lists:
            vol_blocks_lists[vol_rec.rec_index] = []
        volumes[vol_name] = description(vol_rec.rec_index, vol_rec, vol_blocks_lists[vol_rec.rec_index])

    return volumes