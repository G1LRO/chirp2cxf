# chirp2cxf
A utility to convert from CHIRP CSV export files to the CXF file format used by the Quansheng radio CPS

With this utility you can create a backup file for the Quansheng "Portable Radio CPS" program.

The input files will be a generic 'donor' save file from the Quansheng CPS, and a CSV export from CHIRP

The Chirp export CSV only contains the channel informaiton.

The input CXF file will contain everything else you need to configure your Quansheng UV-K5 such as radio settings, dtmf things etc.

This utility inserts the CHIRP CSV information into your donor CXF file and provides a result file with the CHIRP channels included. Take this file and load into the Quansheng CPS to program your radio.

A compiled exe file is available, unzip the folder in one directory and run chirp2cxf.exe with the following parameters:

chirp2cxf.exe chirpfile.csv quanshengfile.cxf

The result is written to a new file.
