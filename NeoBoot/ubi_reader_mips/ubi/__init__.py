#!/usr/bin/python
import re
from ubi.volume import get_volumes
from ubi.block import sort, get_blocks_in_list, extract_blocks
from ubi.defines import *
from ubi import display
from ubi.image import description as image
from ubi.block import layout

class ubi:

    def __init__(self, ubi_file):
        self._file = ubi_file
        self._first_peb_num = 0
        self._blocks = extract_blocks(self)
        self._block_count = len(self.blocks)
        if self._block_count <= 0:
            raise Exception('No blocks found.')
        layout_list, data_list, int_vol_list, unknown_list = sort.by_type(self.blocks)
        self._layout_blocks_list = layout_list
        self._data_blocks_list = data_list
        self._int_vol_blocks_list = int_vol_list
        self._unknown_blocks_list = unknown_list
        arbitrary_block = self.blocks.itervalues().next()
        self._min_io_size = arbitrary_block.ec_hdr.vid_hdr_offset
        self._leb_size = self.file.block_size - arbitrary_block.ec_hdr.data_offset
        layout_pairs = layout.group_pairs(self.blocks, self.layout_blocks_list)
        layout_infos = layout.associate_blocks(self.blocks, layout_pairs, self.first_peb_num)
        self._images = []
        for i in range(0, len(layout_infos)):
            self._images.append(image(self.blocks, layout_infos[i]))

    def _get_file(self):
        return self._file

    file = property(_get_file)

    def _get_images(self):
        return self._images

    images = property(_get_images)

    def _get_data_blocks_list(self):
        return self._data_blocks_list

    data_blocks_list = property(_get_data_blocks_list)

    def _get_layout_blocks_list(self):
        return self._layout_blocks_list

    layout_blocks_list = property(_get_layout_blocks_list)

    def _get_int_vol_blocks_list(self):
        return self._int_vol_blocks_list

    int_vol_blocks_list = property(_get_int_vol_blocks_list)

    def _get_unknown_blocks_list(self):
        return self._unknown_blocks_list

    unknown_blocks_list = property(_get_unknown_blocks_list)

    def _get_block_count(self):
        return self._block_count

    block_count = property(_get_block_count)

    def _set_first_peb_num(self, i):
        self._first_peb_num = i

    def _get_first_peb_num(self):
        return self._first_peb_num

    first_peb_num = property(_get_first_peb_num, _set_first_peb_num)

    def _get_leb_size(self):
        return self._leb_size

    leb_size = property(_get_leb_size)

    def _get_peb_size(self):
        return self.file.block_size

    peb_size = property(_get_peb_size)

    def _get_min_io_size(self):
        return self._min_io_size

    min_io_size = property(_get_min_io_size)

    def _get_blocks(self):
        return self._blocks

    blocks = property(_get_blocks)

    def display(self, tab = ''):
        display.ubi(self, tab)


def get_peb_size(path):
    file_offset = 0
    offsets = []
    f = open(path, 'rb')
    f.seek(0, 2)
    file_size = f.tell() + 1
    f.seek(0)
    for i in range(0, file_size, FILE_CHUNK_SZ):
        buf = f.read(FILE_CHUNK_SZ)
        for m in re.finditer(UBI_EC_HDR_MAGIC, buf):
            start = m.start()
            if not file_offset:
                file_offset = start
                idx = start
            else:
                idx = start + file_offset
            offsets.append(idx)

        file_offset += FILE_CHUNK_SZ

    f.close()
    occurances = {}
    for i in range(0, len(offsets)):
        try:
            diff = offsets[i] - offsets[i - 1]
        except:
            diff = offsets[i]

        if diff not in occurances:
            occurances[diff] = 0
        occurances[diff] += 1

    most_frequent = 0
    block_size = 0
    for offset in occurances:
        if occurances[offset] > most_frequent:
            most_frequent = occurances[offset]
            block_size = offset

    return block_size