# Game Manager
Created by: Christopher Wood

## Usage
This is a series of python scripts, meant to take in lists of video games, hardware, and toys-to-life figures and output a SQLite database containing the information.

## Assumptions
The format of the games list is the following:
Game Name | Game Edition | Steam ID | # of Achievements Earned | # of Total Achievements | Playtime | Time to Beat | File Size (bytes) | File Name | Value | Cost | Legal (bool) | Error (bool) | Shameful (bool) | Box Received State | Box Current State | Box Change State (bool) | Paper Materials Received State | Paper Materials Current State | Paper Materials Change State (bool) | Media Received State | Media Current State | Media Change State (bool) | Date Received | Platform | Console

The format of the hardware list is the following:
Hardware Name | Serial Number | Hardware Type | Value | Cost | Box Received State | Box Current State | Box Change State (bool) | Paper Materials Received State | Paper Materials Current State | Paper Materials Change State (bool) | Hardware Received State | Hardware Current State | Hardware Change State (bool) | Date Received | Error (bool) | Console

The format of the toys-to-life list is the following:
Toy Name | Item Type | Value | Cost | Box Received State | Box Current State | Box Change State (bool) | Paper Materials Received State | Paper Materials Current State | Paper Materials Change State (bool) | Toy Received State | Toy Current State | Toy Change State (bool) | Date Received | Error (bool) | Series | Game (in series)

The system will expect files named `games.xlsx`, `hardware.xlsx`, and `toys-to-life.xlsx` to exist in the folder.

The numbering for the "states" of all items is listed in `QualityState.txt`.

The system will create 2 databases on initial run.
The first is an empty database (called `base.db`) which will only be created if it does not exist.
The second is the filled database (`data.db`) which will be created by copying `base.db` and then inputting the data.

## TODO List
- [x] Basic setup
- [ ] Switch to MySQL
- [ ] Move all queries into stored procedures
- [ ] Tune queries
- [ ] Re-analyze database layout
- [ ] Generalize to handle a few other vectors (toys-to-life that contain hardware, bundles, etc.)