# chirp2cxf
A utility to convert from CHIRP CSV export files to the CXF file format used by the Quansheng UV-K5 radio CPS

Only CTCSS translation is implemented, I'm happy for someone that can test DCS to help, I don't use it.

With this utility will create a new backup file for the Quansheng "Portable Radio CPS" program. Load this into the Quansheng CPS and write to the radio.

The input files will be a generic 'donor' save file from the Quansheng CPS, and a CSV export from CHIRP. Backup your Quansheng radio to the CPS to create the .cxf file.

 Be careful to use the "File->Export as CSV" option in Chirp and not the entire Chirp save file for your radio.The Chirp export CSV only contains the channel information.

The input CXF file will contain everything else you need to configure your Quansheng UV-K5 such as radio settings, scan lists, dtmf things etc.

This utility inserts the CHIRP CSV information into your donor CXF file and provides a result file with the CHIRP channels included. Take this file and load into the Quansheng CPS to program your radio.

To make life a whole lot easier for folks, I have ported the CHIRP2cxf Chirp conversion utility for the UK-K5 to .NET so it's a regular Windows app.

There's a link to it on Github and its stored on Google drive so you have to download the ZIP with the .exe file from there (it was too big for Github).

The fundamental code is the same as the previous Python version so if there were bugs in that then they'll be in this too.

I'm not a professional software writer so forgive the regular things like the exe being unknown to Windows and throwing up all kinds of warnings, you'll have to take your own view on that.

If anyone can help with advice on hosting, signing and distribution of this then I'm all ears 🙂

Any issues and bugs with the conversion process then please let me know.

If you have Python 3 installed the command can be run as:

"python chirp2cxf.py chirpfile.csv quanshengfile.cxf" (The result Quansheng CPS file is written to a new file.)

09/05/23: this file is new and untested. Testing and refinement assistance is most welcome
