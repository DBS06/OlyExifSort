#!/usr/bin/python3

import argparse
import re
import exiftool
import os
import fnmatch
import sys
import re

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, IntEnum


class DriveMode(IntEnum):
    SingleShot = 0
    ContinuousShooting = 1
    ExposureBracketing = 2
    WhiteBalanceBracketing = 3
    ExposureWBBracketing = 4
    Bracketing = 5


class DriveModeBytes(IntEnum):
    Mode = 0
    ShotNum = 1
    ModeBits = 2
    ShutterMode = 4


class BrktMode(IntEnum):
    NONE = 0x00
    AE = 0x01
    WB = 0x02
    FL = 0x04
    MF = 0x08
    ISO = 0x10
    AEA = 0x20
    FOC = 0x40


class StackedImage(Enum):
    NO = '0 0'
    LiveComposite = '1 *'
    LiveTimeBulb = '4 *'
    ND2 = '3 2'
    ND4 = '3 4'
    ND8 = '3 8'
    ND16 = '3 16'
    ND32 = '3 32'
    HDR1 = '5 4'
    HDR2 = '6 4'
    TripodHR = '8 8'
    FocusStacked = '9 *'
    HandheldHR = '11 16'


@dataclass
class BrktSequenceEntry:
    driveMode: DriveMode
    brktMode: BrktMode
    stackedImage: StackedImage
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


def groupBracketing(metadata):
    aeaBrkt = list()
    focBrkt = list()
    sequence = list()
    stackedImage = StackedImage.NO

    for e in metadata:
        # extract drive-mode bytes
        driveModeBytes = [int(k) for k in e["MakerNotes:DriveMode"].split(" ")]

        # extract stacked-image type
        for si in StackedImage:
            match = bool(re.match(si.value, e["MakerNotes:StackedImage"]))
            if match:
                stackedImage = si
                break

        # set stacked-image type
        if stackedImage == StackedImage.FocusStacked:
            sequence.append(BrktSequenceEntry(
                DriveMode(driveModeBytes[DriveModeBytes.Mode]),
                BrktMode(driveModeBytes[DriveModeBytes.ModeBits]),
                stackedImage, driveModeBytes[DriveModeBytes.ShotNum],
                e))

        # check if image is part of a bracketing sequence
        if driveModeBytes[DriveModeBytes.Mode] == DriveMode.Bracketing:
            entry = BrktSequenceEntry(
                DriveMode(driveModeBytes[DriveModeBytes.Mode]),
                BrktMode(driveModeBytes[DriveModeBytes.ModeBits]),
                stackedImage, driveModeBytes[DriveModeBytes.ShotNum],
                e)

            if entry.num == 1 and \
               len(sequence) > 0 and \
               entry.file["File:FileName"].split(".")[0] != sequence[0].file["File:FileName"].split(".")[0]:

                if sequence[0].brktMode == BrktMode.AEA:
                    aeaBrkt.append(sequence)
                if sequence[0].brktMode == BrktMode.FOC:
                    focBrkt.append(sequence)
                sequence = list()

            if entry.brktMode == BrktMode.AEA or entry.brktMode == BrktMode.FOC:
                sequence.append(entry)

    return aeaBrkt, focBrkt

    # Needs to be done to add the last found sequence
    if len(sequence) > 0:
        if sequence[0].brktMode == BrktMode.AEA:
            aeaBrkt.append(sequence)
        if sequence[0].brktMode == BrktMode.FOC:
            focBrkt.append(sequence)

def moveBracketing(moveList):
    print('Move Bracketing')

def main_build(args, params):
    with exiftool.ExifTool() as et:
        # SourceFile
        # File:Filename
        # MakerNotes:DriveMode
        metadata = et.execute_json('-filename', '-DriveMode', '-FileType', '-StackedImage',
                                   'C:\\Users\\phst\\Documents\\_REPOS\\Testpics\\')
        # metadata = et.execute_json('-filename', '-DriveMode', args.path)

        aeaBrkt, focBrkt = groupBracketing(metadata)

        seqCnt = 0
        for gr in aeaBrkt:
            seqCnt += 1
            print(f'AEA #{seqCnt}')
            for el in gr:
                print(f'{el.file["File:FileName"]}: {el.brktMode.name} {el.driveMode.name} #{el.num}')
            print('')

        seqCnt = 0
        for gr in focBrkt:
            seqCnt += 1
            print(f'FOC #{seqCnt}')
            for el in gr:
                print(f'{el.file["File:FileName"]}: {el.brktMode.name} {el.driveMode.name} #{el.num}')
            print('')

        # move aea-bracketing
        moveBracketing(aeaBrkt)


def main(argv):
    """
    main routine
    """
    params = defaultdict(list)
    args = parse_command_line_arguments(argv)
    return main_build(args, params)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
