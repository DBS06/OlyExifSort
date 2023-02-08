# OlyExifSort

This Script detects and sorts photos which where taken with any Bracketing-Mode with an Olympus/OM-System camera. This script is intended to simplify the sort-out process, after you come back from a photo session. See "Usage/Recommended Workflow" for more information

## Usage/Recommended Workflow
I use the script to identify and separate the photo-sequences which where taken with the HDR- and Focus-Bracketing-Mode. I usually copy the photos from a photo session in one folder and name it i.e. "Vienna", then I start the script. After this, I have the "normal" taken photos and the photos taken with AEA- and HDR-Bracketing-Mode separated.<br><br>
**In short I recommend the following workflow**:
- Create a folder and paste your photos, which you want to sort, inside of this folder.<br>
**Note**: Use a folder name which should be final, because the subfolders will be named like that (see "What does this script do" for more information)!<br>
- Call script with:<br>
`python .\OlyExifSort.py -p "C:\path\to\your\folder"`<br>
or use the GUI<br>
`python .\OlyExifSort_GUI.py"`<br>
or use the corresponding Windows-Executables.<br>
- GUI:<br>
  - Select the folder where you want to sort the photos and click on `Search Sequences`
  - After the search is complete you can see inside the LOG-Output and verify the result.
  - If everything seems ok, click on `Move Sequences` and the found sequences will be moved
- After the script is finished, start with sorting out your photos.<br>
**Attention**: I recommend not to delete any of the photos before you start the script, especially the photos from a HDR- and Focus-Bracketing-Sequences!<br>

**Note: Use the script at your own risk! The script does not delete anything, therefore it shouldn't be risky at all!**

## What does this script do

This script extracts with the help of exiftool, the EXIF-Data. In specific it looks only at the `MakerNotes:DriveMode` EXIF-Data and groups the photos based on the bracketing sequences from AEA- and FOC-Mode.<br>
**Note: Depending on the number of photos, pc performance and storage rw speed this takes some time! Even up to a couple of minutes!**<br>
I never used the rest of the Bracketing-Modes, if someone wants to use/sort other modes, pls write an issue and provide example photos, or create a pull-request.<br>
After the search is completed, the scripts starts to move the photos to specific folders. You can see an example here:

## Before:

All photos, which should to be sorted, are in the same folder. It doesn't matter if there are photos, which do not belong to a Bracketing-Sequence.
```
TestPics:
    IMGA2445.ORF
    IMGA2446.ORF
    IMGA2447.ORF
    IMGA2448.JPG
    IMGA2448.ORF
    IMGA2449.JPG
    IMGA2449.ORF
    IMGA2450.JPG
    IMGA2450.ORF
    IMGA2451.JPG
    IMGA2451.ORF
    IMGA2452.JPG
    IMGA2452.ORF
    IMGA2453.JPG
    IMGA2453.ORF
    IMGA2454.JPG
    IMGA2454.ORF
    IMGA2455.JPG
    IMGA2455.ORF
    IMGA2456.JPG
    IMGA2457.JPG
    IMGA2457.ORF
    IMGA2458.JPG
    IMGA2458.ORF
    [...]
```
## After
The photos which do not belong to a sequence are still in the main folder.<br>
- All photos which where taken with FOC-Bracketing are in `[main-folder-name]_FOCs`.<br>
- All photos which where taken with AEA-Bracketing are in `[main-folder-name]_HDRs`.<br>
- All photos which where taken with AE-Bracketing are in `[main-folder-name]_AEs`.<br>
- All photos which where taken with WB-Bracketing are in `[main-folder-name]_WBs`.<br>
- All photos which where taken with FL-Bracketing are in `[main-folder-name]_FLs`.<br>
- All photos which where taken with MF-Bracketing are in `[main-folder-name]_MFs`.<br>
- All photos which where taken with ISO-Bracketing are in `[main-folder-name]_ISOs`.<br>

There you can see preview-photos which are named like `[...]_FOC_XXX.xxx` or `[...]_HDR_XXX.xxx` and so on.<br>
In case of FOC-Bracketing, this photos are either the camera internal stacked photos, or if this does not exist, the first photo of a sequence. This depends on your camera settings, or the sequence was interrupted or unsuccessful.<br>
In case of AEA-, AE-, WB-, FL-, MF-, ISO-Bracketing-Sequences it is always the first photo of a sequence.<br>
This preview-photos makes it easier and faster to look through the sequences and to identify which folder has which sequence.<br>
In the folders `[main-folder-name]_FOC_XXX` or `[main-folder-name]_HDR_XXX` and etc. you will find the single photos of a sequence.<br><br>

**Note:** If there are already sorted photos in the main folder, the script starts the numbering with the highest free number.

```
TestPics
│   IMGA2445.ORF
│   IMGA2446.ORF
│   IMGA2447.ORF
│   IMGA2600.ORF
│   IMGA2601.ORF
│   IMGA2602.ORF
│   IMGA2603.ORF
│   [...]
│   IMGP7717.ORF
│   IMGP7718.ORF
│
├───TestPics_FOCs
│   │   IMGA2456_FOC_001.JPG
│   │   IMGA2472_FOC_002.JPG
│   │   IMGA2488_FOC_003.JPG
│   │   [...]
│   │   IMGP7697_FOC_063.JPG
│   │
│   ├───TestPics_FOC_001
│   │       IMGA2448.JPG
│   │       IMGA2448.ORF
│   │       IMGA2449.JPG
│   │       IMGA2449.ORF
│   │       IMGA2450.JPG
│   │       IMGA2450.ORF
│   │       IMGA2451.JPG
│   │       IMGA2451.ORF
│   │       IMGA2452.JPG
│   │       IMGA2452.ORF
│   │       IMGA2453.JPG
│   │       IMGA2453.ORF
│   │       IMGA2454.JPG
│   │       IMGA2454.ORF
│   │       IMGA2455.JPG
│   │       IMGA2455.ORF
│   │       IMGA2456.JPG
│   │
│   ├───TestPics_FOC_002
│   │       IMGA2457.JPG
│   │       IMGA2457.ORF
│   │       IMGA2458.JPG
│   │       IMGA2458.ORF
│   │       IMGA2459.JPG
│   │       IMGA2459.ORF
│   │       IMGA2460.JPG
│   │       IMGA2460.ORF
│   │       IMGA2461.JPG
│   │       IMGA2461.ORF
│   │       IMGA2462.JPG
│   │       IMGA2462.ORF
│   │       IMGA2463.JPG
│   │       IMGA2463.ORF
│   │       IMGA2464.JPG
│   │       IMGA2464.ORF
│   │       IMGA2465.JPG
│   │       IMGA2465.ORF
│   │       IMGA2466.JPG
│   │       IMGA2466.ORF
│   │       IMGA2467.JPG
│   │       IMGA2467.ORF
│   │       IMGA2468.JPG
│   │       IMGA2468.ORF
│   │       IMGA2469.JPG
│   │       IMGA2469.ORF
│   │       IMGA2470.JPG
│   │       IMGA2470.ORF
│   │       IMGA2471.JPG
│   │       IMGA2471.ORF
│   │       IMGA2472.JPG
│   │
│   ├───TestPics_FOC_003
│   │       IMGA2473.JPG
│   │       IMGA2473.ORF
│   │       IMGA2474.JPG
│   │       IMGA2474.ORF
│   │       IMGA2475.JPG
│   │       IMGA2475.ORF
│   │       IMGA2476.JPG
│   │       IMGA2476.ORF
│   │       IMGA2477.JPG
│   │       IMGA2477.ORF
│   │       IMGA2478.JPG
│   │       IMGA2478.ORF
│   │       IMGA2479.JPG
│   │       IMGA2479.ORF
│   │       IMGA2480.JPG
│   │       IMGA2480.ORF
│   │       IMGA2481.JPG
│   │       IMGA2481.ORF
│   │       IMGA2482.JPG
│   │       IMGA2482.ORF
│   │       IMGA2483.JPG
│   │       IMGA2483.ORF
│   │       IMGA2484.JPG
│   │       IMGA2484.ORF
│   │       IMGA2485.JPG
│   │       IMGA2485.ORF
│   │       IMGA2486.JPG
│   │       IMGA2486.ORF
│   │       IMGA2487.JPG
│   │       IMGA2487.ORF
│   │       IMGA2488.JPG
│   │
[...]
│   └───TestPics_FOC_063
│           IMGP7687.JPG
│           IMGP7687.ORF
│           IMGP7688.JPG
│           IMGP7688.ORF
│           IMGP7689.JPG
│           IMGP7689.ORF
│           IMGP7690.JPG
│           IMGP7690.ORF
│           IMGP7691.JPG
│           IMGP7691.ORF
│           IMGP7692.JPG
│           IMGP7692.ORF
│           IMGP7693.JPG
│           IMGP7693.ORF
│           IMGP7694.JPG
│           IMGP7694.ORF
│           IMGP7695.JPG
│           IMGP7695.ORF
│           IMGP7696.JPG
│           IMGP7696.ORF
│           IMGP7697.JPG
│
└───TestPics_HDRs
    │   IMGP7676_HDR_001.ORF
    │   IMGP7679_HDR_002.ORF
    │
    ├───TestPics_HDR_001
    │       IMGP7676.ORF
    │       IMGP7677.ORF
    │       IMGP7678.ORF
    │
    └───TestPics_HDR_002
            IMGP7679.ORF
            IMGP7680.ORF
            IMGP7681.ORF
            IMGP7682.ORF
            IMGP7683.ORF
            IMGP7684.ORF
            IMGP7685.ORF
```
## Installation
### Via Script:
- clone or download repository.
- execute: `pip install -r requirements.txt`.
- I recommend using the exiftool version which I deliver within the package, if this is not whished download exiftool from https://exiftool.org/. Nevertheless the folder where the `exiftool.exe` is (within the script it is under `./bin/exiftool.exe`), must be added to System-Path.

### Via Executable (Windows):
- download `OlyExifSort_Win.zip` and extract it anywhere.
- I recommend using the exiftool version which I deliver within the package, if this is not whished download exiftool from https://exiftool.org/. Nevertheless the folder where the `exiftool.exe` is, must be added to System-Path.

## Tested Cameras
- Olympus OM-D E-M1 Mark II
- Olympus OM-D E-M1 Mark III
- OM-System OM1

I am not able to test this with different Olympus/OM-System cameras, because I don't have access to another model.
But I am pretty sure this script works for nearly all of the Olympus/OM-System cameras

## Nice 2 Have
- sort Interval Sh./Time Lapse Sequences (I wasn't able to differentiate the time-lapse sequences from normal taken photos via EXIF-Infos)

## Support
If you want to support me, I would really happy if you would add me on [500px](https://500px.com/p/dbs06) and/or like my photos :blush: