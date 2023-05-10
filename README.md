# chirp2cxf
A utility to convert from CHIRP CSV export files to the CXF file format used by the Quansheng UV-K5 radio CPS

Only CTCSS translation is implemented, I'm happy for someone that can test DCS to help, I don't use it.

With this utility will create a new backup file for the Quansheng "Portable Radio CPS" program. Load this into the Quansheng CPS and write to the radio.

The input files will be a generic 'donor' save file from the Quansheng CPS, and a CSV export from CHIRP. Backup your Quansheng radio to the CPS to create the .cxf file.

 Be careful to use the "File->Export as CSV" option in Chirp and not the entire Chirp save file for your radio.The Chirp export CSV only contains the channel information.

The input CXF file will contain everything else you need to configure your Quansheng UV-K5 such as radio settings, scan lists, dtmf things etc.

This utility inserts the CHIRP CSV information into your donor CXF file and provides a result file with the CHIRP channels included. Take this file and load into the Quansheng CPS to program your radio.

If you have Python 3 installed the command can be run as:

"python chirp2cxf.py chirpfile.csv quanshengfile.cxf"

A compiled exe file is available, unzip the folder in one directory and run chirp2cxf.exe with the following parameters:

"chirp2cxf.exe chirpfile.csv quanshengfile.cxf"

The result Quansheng CPS file is written to a new file.

09/05/23: this file is new and untested. Testing and refinement assistance is most welcome
