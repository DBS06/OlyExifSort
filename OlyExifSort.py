#!/usr/bin/python3

import argparse
import re
import exiftool
import os
import fnmatch
import sys
import re
import shutil
import pathlib

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


class ReturnStatus(IntEnum):
    SUCCESS = 0
    ERROR = 1
    INVALID_PATH = 2
    NO_SEQUENCES_FOUND = 3
    NO_IMAGES_FOUND = 4
    NO_FILES = 5


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
    aeBrkt = list()
    wbBrkt = list()
    flBrkt = list()
    mfBrkt = list()
    isoBrkt = list()
    sequence = list()
    stackedImage = StackedImage.NO

    for e in metadata:
        if e["File:FileType"] == "ORF" or e["File:FileType"] == "JPEG":
            # extract drive-mode bytes
            driveModeBytes = [int(k)
                              for k in e["MakerNotes:DriveMode"].split(" ")]

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

                if len(sequence) > 0:
                    if (entry.num == 1 or entry.num != (sequence[-1].num + 1)) and \
                            len(sequence) > 0 and \
                            entry.file["File:FileName"].split(".")[0] != sequence[-1].file["File:FileName"].split(".")[0]:

                        if sequence[0].brktMode == BrktMode.AEA:
                            aeaBrkt.append(sequence)
                        if sequence[0].brktMode == BrktMode.FOC:
                            focBrkt.append(sequence)
                        if sequence[0].brktMode == BrktMode.AE:
                            aeBrkt.append(sequence)
                        if sequence[0].brktMode == BrktMode.WB:
                            wbBrkt.append(sequence)
                        if sequence[0].brktMode == BrktMode.FL:
                            flBrkt.append(sequence)
                        if sequence[0].brktMode == BrktMode.MF:
                            mfBrkt.append(sequence)
                        if sequence[0].brktMode == BrktMode.ISO:
                            isoBrkt.append(sequence)
                        sequence = list()

                if entry.brktMode == BrktMode.AEA or entry.brktMode == BrktMode.FOC:
                    sequence.append(entry)

    # Needs to be done to add the last found sequence
    if len(sequence) > 0:
        if sequence[0].brktMode == BrktMode.AEA:
            aeaBrkt.append(sequence)
        if sequence[0].brktMode == BrktMode.FOC:
            focBrkt.append(sequence)
        if sequence[0].brktMode == BrktMode.AE:
            aeBrkt.append(sequence)
        if sequence[0].brktMode == BrktMode.WB:
            wbBrkt.append(sequence)
        if sequence[0].brktMode == BrktMode.FL:
            flBrkt.append(sequence)
        if sequence[0].brktMode == BrktMode.MF:
            mfBrkt.append(sequence)
        if sequence[0].brktMode == BrktMode.ISO:
            isoBrkt.append(sequence)

    return aeaBrkt, focBrkt, aeBrkt, wbBrkt, flBrkt, mfBrkt, isoBrkt


def moveBracketing(moveList, path, mode):

    mainDirLabel = ""
    subDirLabel = ""

    if mode == BrktMode.AEA:
        mainDirLabel = "HDRs"
        subDirLabel = "HDR"
    if mode == BrktMode.FOC:
        mainDirLabel = "FOCs"
        subDirLabel = "FOC"
    if mode == BrktMode.AE:
        mainDirLabel = "AEs"
        subDirLabel = "AE"
    if mode == BrktMode.WB:
        mainDirLabel = "WBs"
        subDirLabel = "WB"
    if mode == BrktMode.FL:
        mainDirLabel = "FLs"
        subDirLabel = "FL"
    if mode == BrktMode.MF:
        mainDirLabel = "MFs"
        subDirLabel = "MF"
    if mode == BrktMode.ISO:
        mainDirLabel = "ISOs"
        subDirLabel = "ISO"

    print("Move %s Bracketing Sequences" % (subDirLabel))

    mainDirName = os.path.basename(path)
    targetMainDirName = mainDirName + "_" + mainDirLabel
    targetMainDirPath = os.path.join(path, targetMainDirName)
    subDirNameMask = mainDirName + "_" + subDirLabel + "_"

    moveBrktCount = 0
    moveBrktCountOffset = 0

    if os.path.exists(targetMainDirPath):
        print("preexisting folder '" + targetMainDirName + "' found")
        existingBrktFolders = fnmatch.filter(
            os.listdir(targetMainDirPath), subDirNameMask + '*')
        if (len(existingBrktFolders) > 0):
            existingBrktFolders.sort(reverse=True)
            lastHdrFolder = existingBrktFolders[0]
            moveBrktCountOffset = int(
                existingBrktFolders[0].replace(subDirNameMask, ''))

    if not os.path.exists(targetMainDirPath):
        os.makedirs(targetMainDirPath)

    for seq in moveList:
        pathExists = True
        # Create sub-directory in hdr-directory if it does not already exists
        # if directory already exists, try next higher number for directory
        while pathExists:
            moveBrktCount += 1
            dirname = "%s%03d" % (
                subDirNameMask, moveBrktCount + moveBrktCountOffset)
            targetDirPath = os.path.join(targetMainDirPath, dirname)
            pathExists = os.path.exists(targetDirPath)

        isLastImageStacked = False

        if mode == BrktMode.FOC:
            isLastImageStacked = seq[-1].stackedImage.name == "FocusStacked"

            if isLastImageStacked:
                lastImg = seq[-1]
                sourcePath = lastImg.file["SourceFile"]
                targetPath = os.path.join(
                    targetDirPath, lastImg.file["File:FileName"])

                fileEnding = pathlib.Path(lastImg.file["File:FileName"]).suffix
                targetPathCopy = "%s_%s_%03d%s" % (os.path.join(targetMainDirPath, lastImg.file["File:FileName"].replace(
                    fileEnding, "")), subDirLabel, moveBrktCount + moveBrktCountOffset, fileEnding)

                print("Makedir: %s" % (dirname))
                os.makedirs(targetDirPath)
                shutil.copy2(sourcePath, targetPathCopy)

        for img in seq:
            sourcePath = img.file["SourceFile"]
            targetPath = os.path.join(
                targetDirPath, img.file["File:FileName"])

            if not isLastImageStacked:
                fileEnding = pathlib.Path(img.file["File:FileName"]).suffix
                # Create copy path for the first image from the Sequence
                # -> the script copies the first image from the Sequence to the HDR/FOC-Main-Folder and appends the folder name to the file name
                # -> makes it easier to look through the Sequences and to identify which folder has the remaining images from the sequence
                targetPathCopy = "%s_%s_%03d%s" % (os.path.join(targetMainDirPath, img.file["File:FileName"].replace(
                    fileEnding, "")), subDirLabel, moveBrktCount + moveBrktCountOffset, fileEnding)

                # if target directory does not exists create it and copy the first image from the HDR-Sequence
                if not os.path.exists(targetDirPath):
                    print("Makedir: %s" % (dirname))
                    os.makedirs(targetDirPath)
                    shutil.copy2(sourcePath, targetPathCopy)

                isLastImageStacked = True

            # Move the Sequence to the folder and inform the user about it
            print("Move: " + img.file["File:FileName"])
            # move image to target directory
            shutil.move(sourcePath, targetPath)

        print(" ")


def executeExifRead(path):
    retStatus = ReturnStatus.ERROR
    aeaBrkt = list()
    focBrkt = list()
    aeBrkt = list()
    wbBrkt = list()
    flBrkt = list()
    mfBrkt = list()
    isoBrkt = list()

    with exiftool.ExifTool() as et:
        # SourceFile
        # File:Filename
        # MakerNotes:DriveMode

        if not os.path.exists(path):
            retStatus = ReturnStatus.INVALID_PATH
            print(f'given path "{path}" is invalid!')
            print(f'aborting!')

        else:
            numOfFiles = next(os.walk(path))[2]
            print(f'Number of Files: {len(numOfFiles)}')

            if len(numOfFiles) != 0:
                print(f'scanning image EXIF-Data...')
                print(f'Please Note: Depending on the number of images, pc performance and storage rw speed this takes some time! Even up to a couple of minutes...')

                metadata = et.execute_json(
                    '-filename', '-DriveMode', '-FileType', '-StackedImage', path)

                # sort metadata list by filename
                metadata.sort(key=lambda x: x["File:FileName"])

                print(f'scanning image EXIF-Data finished!')

                if len(metadata) == 0:
                    retStatus = ReturnStatus.NO_IMAGES_FOUND
                    print(f'no images found!')
                else:
                    print(f'start grouping images to sequences...')

                    try:
                        aeaBrkt, focBrkt, aeBrkt, wbBrkt, flBrkt, mfBrkt, isoBrkt = groupBracketing(
                            metadata)

                        print(f'HDR sequences found: ' + str(len(aeaBrkt)))
                        print(f'FOC sequences found: ' + str(len(focBrkt)))
                        print(f'AE sequences found: ' + str(len(aeBrkt)))
                        print(f'WB sequences found: ' + str(len(wbBrkt)))
                        print(f'FL sequences found: ' + str(len(flBrkt)))
                        print(f'MF sequences found: ' + str(len(mfBrkt)))
                        print(f'ISO sequences found: ' + str(len(isoBrkt)))
                        print("")
                        printSequences(aeaBrkt, "HDR")
                        printSequences(focBrkt, "FOC")
                        printSequences(aeBrkt, "AE")
                        printSequences(wbBrkt, "WB")
                        printSequences(flBrkt, "FL")
                        printSequences(mfBrkt, "MF")
                        printSequences(isoBrkt, "ISO")

                        if (len(aeaBrkt) > 0 or len(focBrkt) > 0 or len(aeBrkt) > 0 or len(wbBrkt) > 0 or len(flBrkt) > 0 or len(mfBrkt) > 0 or len(isoBrkt) > 0):
                            retStatus = ReturnStatus.SUCCESS
                        else:
                            retStatus = ReturnStatus.NO_SEQUENCES_FOUND

                    except KeyError:
                        print("An KeyError exception occurred!")
                        retStatus = ReturnStatus.ERROR
                    except:
                        print("An exception occurred!")
                        retStatus = ReturnStatus.ERROR
            else:
                retStatus = ReturnStatus.NO_FILES
                print(f'There are no files in this folder!')

    return retStatus, aeaBrkt, focBrkt, aeBrkt, wbBrkt, flBrkt, mfBrkt, isoBrkt


def printSequences(seq, name):

    if len(seq):
        print(f'# {name} Sequences:')
    seqCnt = 0
    for gr in seq:
        seqCnt += 1
        print(f'{name} #{seqCnt}')
        for el in gr:
            print(
                f'{el.file["File:FileName"]}: {el.brktMode.name} {el.driveMode.name} #{el.num}')
        print('')


def moveSequences(path, aeaBrkt, focBrkt, aeBrkt, wbBrkt, flBrkt, mfBrkt, isoBrkt):
    if len(aeaBrkt) > 0:
        moveBracketing(aeaBrkt, path, BrktMode.AEA)
        print("Moving AEA-Bracketing Sequences Finished!")
        print("")

    if len(focBrkt) > 0:
        moveBracketing(focBrkt, path, BrktMode.FOC)
        print("Moving FOC-Bracketing Sequences Finished!")
        print("")

    if len(aeBrkt) > 0:
        moveBracketing(aeBrkt, path, BrktMode.AE)
        print("Moving AE-Bracketing Sequences Finished!")
        print("")

    if len(wbBrkt) > 0:
        moveBracketing(wbBrkt, path, BrktMode.WB)
        print("Moving WB-Bracketing Sequences Finished!")
        print("")

    if len(flBrkt) > 0:
        moveBracketing(flBrkt, path, BrktMode.FL)
        print("Moving FL-Bracketing Sequences Finished!")
        print("")

    if len(mfBrkt) > 0:
        moveBracketing(mfBrkt, path, BrktMode.MF)
        print("Moving MF-Bracketing Sequences Finished!")
        print("")

    if len(isoBrkt) > 0:
        moveBracketing(isoBrkt, path, BrktMode.ISO)
        print("Moving ISO-Bracketing Sequences Finished!")
        print("")

    print("")
    print("SUCCESS!")


def main_build(args, params):
    retStatus, aeaBrkt, focBrkt, aeBrkt, wbBrkt, flBrkt, mfBrkt, isoBrkt = executeExifRead(
        args.path)

    status = ""
    if (retStatus == ReturnStatus.SUCCESS):
        status = "Search for Sequences finished!"
    elif (retStatus == ReturnStatus.ERROR):
        status = "Search for Sequences ended with an unknown Error!"
    elif (retStatus == ReturnStatus.INVALID_PATH):
        status = "Given Path is invalid!"
    elif (retStatus == ReturnStatus.NO_IMAGES_FOUND):
        status = "No images found in given folder!"
    elif (retStatus == ReturnStatus.NO_FILES):
        status = "No files found in given folder!"
    elif (retStatus == ReturnStatus.NO_SEQUENCES_FOUND):
        status = "No Bracketing-Sequences found in given folder!"
    print(status)

    if (len(aeaBrkt) > 0 or len(focBrkt) > 0 or len(aeBrkt) > 0 or len(wbBrkt) > 0 or len(flBrkt) > 0 or len(mfBrkt) > 0 or len(isoBrkt) > 0):
        moveSequences(args.path, aeaBrkt, focBrkt, aeBrkt,
                      wbBrkt, flBrkt, mfBrkt, isoBrkt)


def main(argv):
    """
    main routine
    """
    params = defaultdict(list)
    args = parse_command_line_arguments(argv)
    return main_build(args, params)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
