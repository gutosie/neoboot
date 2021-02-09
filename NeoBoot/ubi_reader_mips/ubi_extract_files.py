#!/usr/bin/python

import os
import sys
import argparse
from ubi import ubi, get_peb_size
from ubifs import ubifs
from ubi_io import ubi_file, leb_virtual_file
from ui.common import extract_files, output_dir
if __name__ == '__main__':   
    description = 'Extract contents of UBI image.'
    usage = 'ubi_extract_files.py [options] filepath'
    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument('-l', '--log-file', dest='logpath', help='Log output to file output/LOGPATH. (default: ubifs_output.log)')
    parser.add_argument('-k', '--keep-permissions', action='store_true', dest='permissions', help='Maintain file permissions, requires running as root. (default: False)')
    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', help='Suppress warnings and non-fatal errors. (default: False)')
    parser.add_argument('-p', '--peb-size', type=int, dest='block_size', help='Specify PEB size.')
    parser.add_argument('-o', '--output-dir', dest='output_path', help='Specify output directory path.')
    parser.add_argument('filepath', help='File to extract contents of.')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()
    if args.filepath:
        path = args.filepath
        if not os.path.exists(path):
            parser.error("File path doesn't exist.")
    if args.output_path:
        output_path = args.output_path
    else:
        img_name = os.path.splitext(os.path.basename(path))[0]
        output_path = os.path.join(output_dir, img_name)
    if args.logpath:
        log_to_file = True
        log_file = args.logpath
    else:
        log_to_file = None
        log_file = None
    if args.block_size:
        block_size = args.block_size
    else:
        block_size = get_peb_size(path)
    perms = args.permissions
    quiet = args.quiet
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    ufile = ubi_file(path, block_size)
    uubi = ubi(ufile)
    for image in uubi.images:
        for volume in image.volumes:
            vol_out_path = os.path.join(output_path, volume)
            if not os.path.exists(vol_out_path):
                os.makedirs(vol_out_path)
            elif os.listdir(vol_out_path):
                parser.error('Volume output directory is not empty. %s' % vol_out_path)
            ufsfile = leb_virtual_file(uubi, image.volumes[volume])
            uubifs = ubifs(ufsfile)
            uubifs.log.log_file = log_file
            uubifs.log.log_to_file = log_to_file
            uubifs.log.quiet = quiet
            print 'Writing to: %s' % vol_out_path
            extract_files(uubifs, vol_out_path, perms)

    sys.exit(0)