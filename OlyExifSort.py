#!/usr/bin/python3

import argparse
import re
import exiftool
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


class BrktMode(Enum):
    AE = 0x01
    WB = 0x02
    FL = 0x04
    MF = 0x08
    ISO = 0x10
    AEA = 0x20
    FOC = 0x40


@dataclass
class BrktSequenceEntry:
    brktType: BrktMode
    num: int
    file: list()


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
        description="this program sorts and moves AE- and Focus-Bracketing sequences"
    )
    parser = create_build_parser(parser)
    args = parser.parse_args(argv)
    return args


def main_build(args, params):
    with exiftool.ExifTool() as et:
        # SourceFile
        # File:Filename
        # MakerNotes:DriveMode
        metadata = et.execute_json('-filename', '-DriveMode', '-FileType',
                                   'C:\\Users\\phst\\Documents\\_REPOS\\Testpics\\')
        # metadata = et.execute_json('-filename', '-DriveMode', args.path)

        aeaBrkt = list()
        focBrkt = list()
        sequence = list()

        for e in metadata:
            driveModeArr = [int(k) for k in e["MakerNotes:DriveMode"].split(" ")]
            if driveModeArr[0] == 5:
                entry = BrktSequenceEntry(BrktMode(driveModeArr[2]), driveModeArr[1], e)

                # and  != sequence[0].file["File:FileName"].split(".")[0]
                if entry.num == 1 and len(sequence) > 0:
                    if entry.file["File:FileName"].split(".")[0] != sequence[0].file["File:FileName"].split(".")[0]:
                        if sequence[0].brktType == BrktMode.AEA:
                            aeaBrkt.append(sequence)
                        if sequence[0].brktType == BrktMode.FOC:
                            focBrkt.append(sequence)
                        sequence = list()

                if entry.brktType == BrktMode.AEA or entry.brktType == BrktMode.FOC:
                    sequence.append(entry)

        # Needs to be done to add the last found sequence
        if len(sequence) > 0:
            if sequence[0].brktType == BrktMode.AEA:
                aeaBrkt.append(sequence)
            if sequence[0].brktType == BrktMode.FOC:
                focBrkt.append(sequence)

        seqCnt = 0
        for gr in aeaBrkt:
            seqCnt += 1
            print(f'AEA #{seqCnt}')
            for el in gr:
                print(f'{el.brktType.name}: {el.file["File:FileName"]}: {el.file["MakerNotes:DriveMode"]}')
            print('')

        seqCnt = 0
        for gr in focBrkt:
            seqCnt += 1
            print(f'FOC #{seqCnt}')
            for el in gr:
                print(f'{el.brktType.name}: {el.file["File:FileName"]}: {el.file["MakerNotes:DriveMode"]}')
            print('')


def main(argv):
    """
    main routine
    """
    params = defaultdict(list)
    args = parse_command_line_arguments(argv)
    return main_build(args, params)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
