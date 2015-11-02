#!/usr/bin/python
# -*- coding: utf-8 -*-

""" shuffle multiple gzipped files. """

import argparse
import random
import os
import os.path
import subprocess
import re
import itertools
import sys
import fileinput
import gzip
import logging
import traceback

def out_file_count(s):
    n = int(s)
    if n < 1:
        raise ValueError('Bad output files count')
    return n

def iterate_lines_in_input_files(files_list):
    """ iterate over multiple input files """
    return fileinput.input(files_list, openhook=gzip.open)

def shuffle(out_name_prefix, nfiles, length, files, to_dir='.'):
    """ randomly shuffle and output multiple files """
    n = sum(1 for _ in iterate_lines_in_input_files(files))
    k = length * nfiles
    k_selected = 0
    writers = [subprocess.Popen('gzip -c', stdout=open('{0}/{1}{2}.log.gz'.format(to_dir, out_name_prefix, fno+1), 'w'), stdin=subprocess.PIPE, shell=True) for fno in xrange(nfiles)]
    for i, line in enumerate(iterate_lines_in_input_files(files)):
        if k - k_selected >= random.random() * (n - i):
            writers[k_selected % nfiles].stdin.write(line)
            k_selected += 1
    for wr in writers:
        wr.stdin.close()
        wr.wait()


def main():
    logger = logging.getLogger('shuffle_app')
    logger.setLevel(logging.DEBUG)

    methods = {'shuffle': shuffle}

    parser = argparse.ArgumentParser()
    parser.add_argument('output_name', type=str, help='Name of generated output files')
    parser.add_argument('nfiles', type=out_file_count, help='Count of generated files')
    parser.add_argument('length', type=int, help='Count of lines in one generated file')
    parser.add_argument('files', type=str, nargs='+', help='Input files')
    parser.add_argument('--to-dir', default='.')
    parser.add_argument('--method', default='shuffle', choices=methods.keys())
    args = parser.parse_args()
    try:
        logger.debug('start shuffling input files')
        methods[args.method](
                args.output_name,
                args.nfiles,
                args.length,
                args.files,
                to_dir=args.to_dir)
    except Exception as exc:
        logger.error('exception shuffling files: %s', traceback.format_exc(exc))

if __name__ == '__main__':
    main()

