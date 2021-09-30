#!/usr/bin/python3

import argparse
import re
import exiftool
import os
import sys
from collections import defaultdict


def create_build_parser(parser):
    """
    configures/adds the relevant options to the parser
    :param parser:
    :return:
    """

    parser.add_argument("-p", "--path", default="", metavar="<PATH>",
                        help="specifies the path which should be sorted")
    return parser


def parse_command_line_arguments(argv):
    """
    parse command line arguments
    :return: dictionary containing the arguments (from argparse module)
    """
    parser = argparse.ArgumentParser(
        description="This program views (and maybe saves to a file) SWO output from Jlink."
    )
    parser = create_build_parser(parser)
    args = parser.parse_args(argv)
    return args


def main_build(args, params):
    with exiftool.ExifTool() as et:
        # SourceFile
        # File:Filename
        # MakerNotes:DriveMode
        # metadata = et.execute_json('-filename', '-DriveMode', 'C:\\Users\\phst\\Documents\\_REPOS\\Testpics\\')
        metadata = et.execute_json('-filename', '-DriveMode', args.path)

        for e in metadata:
            driveModeArr = [int(k) for k in e["MakerNotes:DriveMode"].split(" ")]
            if (driveModeArr[0] == 5):
                if (driveModeArr[2] == 32):
                    print(f'ABKT: {e["File:FileName"]}: {e["MakerNotes:DriveMode"]}')
                if (driveModeArr[2] == 64):
                    print(f'FBKT: {e["File:FileName"]}: {e["MakerNotes:DriveMode"]}')


def main(argv):
    """
    main routine
    """
    params = defaultdict(list)
    args = parse_command_line_arguments(argv)
    return main_build(args, params)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
