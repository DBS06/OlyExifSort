#!/usr/bin/python

import exiftool


with exiftool.ExifTool() as et:
    metadata = et.execute_json('-r', '-filename', '-DriveMode', 'D:\\Kanaren\\P\\210906')
    print(metadata)
