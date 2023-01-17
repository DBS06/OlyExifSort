# OlyExifSort

This Script detects and sorts images which where taken with AEA/HDR- and Focus-Bracketing-Mode with an Olympus/OM-System camera. This script is intended to simplify the sort-out process, after you come back from a photo session. See "Usage/Recommended Workflow" for more information

## Usage/Recommended Workflow
I use the script to identify the image-sequences which where taken with the HDR- and Focus-Bracketing-Mode. I usually copy the images from a photo session in one folder and name it i.e. "Vienna", then I start the script. After this, I have the "normal" taken photos and the photos taken with AEA- and HDR-Bracketing-Mode separated. <br>
**In short I recommend the following workflow**:
- Create a folder and paste your images which you want to sort inside of this folder.<br>
**Note**: use a folder name which should be final, because the subfolders will be named like that!<br>
- Call script with:<br>
`python .\OlyExifSort.py -p C:\\path\\to\\your\\folder`<br>
- After the script is finished, start with sorting out your photos.<br>
**Attention**: I recommend to not delete any of the images before you start the script!<br>

**Note: use the script at your own risk! The script does not delete anything, therefore it shouldn't be risky at all!**

## What does this script do

This script extracts with the help of exiftool, the EXIF-Data. In specific it looks only at the `MakerNotes:DriveMode` EXIF-Data and groups the images based on the bracketing sequences from AEA- and FOC-Mode.<br>
**Note: Depending on the number of images, pc performance and storage rw speed this takes some time! Even up to a couple of minutes!**<br>
I never used the rest of the Bracketing-Modes, if someone wants to use/sort other modes, pls write an issue and provide example images, or create a pull-request.<br>
After the search is completed, the scripts starts to move the images to specific folders. You can see an example here:

## Before:

All images, which should to be sorted, are in the same folder. It doesn't matter if there are images, which do not belong to a AEA- or FOC-Sequence.
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
The images which do not belong to a sequence are still in the main folder.<br>
All images which where taken with FOC-Bracketing are in `[main-folder-name]_FOCs`.<br>
All images which where taken with AEA-Bracketing are in `[main-folder-name]_HDRs`.<br>
There you can see preview-images which are named like `[...]_FOC_XXX.xxx` or `[...]_HDR_XXX.xxx`.<br>
In case of FOC-Bracketing, this images are either the camera internal stacked images, or if this does not exist, the first image of a sequence. This depends on your camera settings, or the sequence was interrupted or unsuccessful.<br>
In case of AEA-Bracketing it is always the first image of a sequence.<br>
This preview-images makes it easier and faster to look through the sequences and to identify which folder has which sequence.<br>
In the folders `[main-folder-name]_FOC_XXX` or `[main-folder-name]_HDR_XXX` you will find the single images of a sequence.<br><br>

**Note:** If there are already sorted images in the main folder, the script starts the numbering with the highest free number.

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
- clone or download repository
- execute: `pip install -r requirements.txt`
- add `[...]/bin/exiftool.exe` to System-Path 

## Tested Cameras
- Olympus OM-D E-M1 Mark II

I am not able to test this with different Olympus/OM-System cameras, because I don't have access to another model.

## Nice 2 Have
- a complied executable
- an GUI which allows to set some of the settings

If anyone hast time to do this I would really appreciate it!