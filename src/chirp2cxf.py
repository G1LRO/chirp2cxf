#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright 2023 G1LRO, OM0WT

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import csv
import sys
from loguru import logger
import argparse
from argparse import RawTextHelpFormatter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

disclaimer_box = """
chirp2cxf v1.0

A utility to convert from CHIRP CSV export files to the CXF file format used by the Quansheng UV-K5 radio CPS

CTCSS and DCS translation is implemented

With this utility will create a new backup file for the Quansheng "Portable Radio CPS" program. Load this into the Quansheng CPS and write to the radio.

The input files will be a generic 'donor' save file from the Quansheng CPS, and a CSV export from CHIRP. Backup your Quansheng radio to the CPS to create the .cxf file.

Be careful to use the "File-&gt;Export as CSV" option in Chirp and not the entire Chirp save file for your radio. The Chirp export CSV only contains the channel information and not radio settings etc..

The donor CXF file will contain everything else you need to configure your Quansheng UV-K5 such as radio settings, scan lists, dtmf things etc. and you can edit this further when you load into the Quansheng CPS prior to writing to the radio.

The output file is written to the same directory as the donor cxf file.

This utility inserts the CHIRP CSV information into your donor CXF file and provides a result file with the CHIRP channels included. Take this file and load into the Quansheng CPS to program your radio.

Copyright 2023 G1LRO
Copyright 2023 OM0WT (GUI part, DCS implementation)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

class CXF_Convert():
    #ctcss data
    ctcss_tones = [
        67.0, 69.3, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5,
        94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3,
        131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 159.8, 162.2, 165.5, 167.9,
        171.3, 173.8, 177.3, 179.9, 183.5, 186.2, 189.9, 192.8, 196.6, 199.5,
        203.5, 206.5, 210.7, 218.1, 225.7, 229.1, 233.6, 241.8, 250.3
        ]
    
    dcs_tones = [
        23, 25, 26, 31, 32, 43, 47, 51, 53, 54, 65, 71, 72, 73, 74,114,115,116,122,125,
        131,132,134,143,152,155,156,162,165,172,174,205,212,223,225,226,243,244,245,246,
        251,252,261,263,265,266,271,306,311,315,325,331,343,346,351,364,365,371,411,412,
        413,423,425,431,432,445,446,452,455,464,465,466,503,506,516,521,525,532,546,552,
        564,565,606,612,624,627,631,632,645,652,654,662,664,703,712,723,725,726,731,732,
        734,743,754
    ]
    
    # Files
    _chirpfile = ""
    _cxffile = ""
    _targetfile = ""
    
    #set these varibles if the CtCss is not in the table
    AnaTxCTCIndex=0
    AnaRxCTCIndex=0
    
    def __init__(self, chirpfile, cxffile, targetfile ) -> None:
        self._chirpfile = chirpfile
        self._cxffile = cxffile
        self._targetfile = targetfile


    def csv2cxf(self):
        converted_channels_list = []
        logger.debug(f"CHIRP file: {self._chirpfile}, CXF file: {self._cxffile}, OUTPUT file: {self._targetfile}")
        #copy top parf of CXF file to the new file
        with open(self._cxffile, 'r') as input_file:
            # open the output file for writing
            with open(self._targetfile, 'w') as output_file:
                # read each line from the input file
                for line in input_file:
                    # write the line to the output file
                    output_file.write(line)
                    # check if the line contains the target word
                    if '<Channels_MR>' in line:
                        # if so, stop reading and writing
                        break
        logger.info("First part of cxf file written")
        # Open the CSV file
        with open(self._chirpfile, mode='r') as csv_file:

            # Create a CSV reader object
            csv_reader = csv.DictReader(csv_file)

            # Iterate over each row in the CSV file
            for row in csv_reader:

                # Put each value into a separate variable
                Location = row['Location']
                Name = row['Name']
                Frequency = row['Frequency']
                Duplex = row['Duplex']
                Offset = row['Offset']
                Tone = row['Tone']
                rToneFreq = row['rToneFreq'] #ctcss tone frequency
                cToneFreq = row['cToneFreq']
                DtcsCode = row['DtcsCode']
                DtcsPolarity = row['DtcsPolarity']
                RxDtcsCode = row['RxDtcsCode']
                CrossMode = row['CrossMode']
                TStep = row['TStep']
                Skip = row['Skip']
                Power = row['Power']
                Mode = row['Mode']

                #Start field translation  

                #Check location is ok (<200)
                if float(Location)>200:
                    break
                chanIndex=Location


                #Name goes into <Name>
                Name = Name[:10]


                #Tidy up for <Rxfreq>
                RxFreq = float(Frequency)
                RxFreq = round(RxFreq,6)


                #Calculate Transmit <Txfreq> from Recieve and Offset Xml variable <Txfreq>
                TxFreq = float(Frequency) + float(Offset) #CHIRP sets Offset to 0 if not used
                if Duplex == "-":
                    TxFreq = float(Frequency) - float(Offset)
                TxFreq = round(TxFreq,6)


                #calculate ctcss tone index position for rx and tx tones
                if float(rToneFreq) in self.ctcss_tones:
                    AnaTxCTCIndex = self.ctcss_tones.index(float(rToneFreq))
                if float(cToneFreq) in self.ctcss_tones:
                    AnaRxCTCIndex = self.ctcss_tones.index(float(cToneFreq))


                #Calculate values for <AnaTxCTCFlag> <AnaRxCTCFlag>
                if Tone == "":
                    AnaTxCTCFlag = 0
                    AnaRxCTCFlag = 0
                if Tone == "Tone":
                    AnaTxCTCFlag = 1
                    AnaRxCTCFlag = 0
                if Tone == "TSQL":
                    AnaTxCTCFlag = 1
                    AnaRxCTCFlag = 1
                if Tone == "Cross":
                    if CrossMode == "->Tone":            
                        AnaTxCTCFlag = 0
                        AnaRxCTCFlag = 1
                if Tone == "Cross":
                    if CrossMode == "Tone->Tone":            
                        AnaTxCTCFlag = 1
                        AnaRxCTCFlag = 1
                if Tone == "DTCS":
                    AnaTxCTCFlag = 2
                    AnaRxCTCFlag = 0
                    if DtcsPolarity == "RR":
                        AnaTxCTCFlag = 3
                        # logger.debug(f"RR found for {Name}")
                    # Wrapping leading zeros
                    AnaTxCTCIndex = f"{self.dcs_tones.index(int(DtcsCode))}"
                if Tone == "DTCS-R":
                    AnaRxCTCFlag = 2
                    AnaTxCTCFlag = 0
                    if DtcsPolarity == "RR":
                        AnaRxCTCFlag = 3
                    AnaRxCTCIndex = f"{self.dcs_tones.index(int(RxDtcsCode))}"
                    # logger.debug(f"DCS-R + RR: AnaRxCTCFlag {AnaRxCTCFlag}, AnaRxCTCIndex: {AnaRxCTCIndex} ")
                #Calculate <TxPowerLevel>
                TxPowerLevel = 2 #default to high
                if Power == "4.0W": #Chirp config for a BF=8HP uses these values
                    TxPowerLevel = 1
                if Power == "1.0W":
                    TxPowerLevel = 0

                #calculate the <BandWidth>
                Bandwidth = 0 #default to 25khz
                if Mode == "NFM":
                    Bandwidth = 1



                #Lets print the XML

                #print ('    <Channel Name=\"'+Name+'\" chanIndex=\"'+str(chanIndex)+'\">')
                #print ('      <BandWidth>'+str(Bandwidth)+'</BandWidth>')
                #print ('      <TxFreq>'+str(TxFreq)+'</TxFreq>')
                #print ('      <RxFreq>'+str(RxFreq)+'</RxFreq>')
                #print ('      <TxPowerLevel>'+str(TxPowerLevel)+'</TxPowerLevel>')
                #print ('      <AnaTxCTCFlag>'+str(AnaTxCTCFlag)+'</AnaTxCTCFlag>')
                #print ('      <AnaRxCTCFlag>'+str(AnaRxCTCFlag)+'</AnaRxCTCFlag>')
                #print ('      <AnaTxCTCIndex>'+str(AnaTxCTCIndex)+'</AnaTxCTCIndex>')
                #print ('      <AnaRxCTCIndex>'+str(AnaRxCTCIndex)+'</AnaRxCTCIndex>')
                #print ('      <FreqStep>2</FreqStep>')
                #print ('      <FreqReverseFlag>0</FreqReverseFlag>')
                #print ('      <EncryptFlag>0</EncryptFlag>')
                #print ('      <BusyNoTx>0</BusyNoTx>')
                #print ('      <PTTIdFlag>0</PTTIdFlag>')
                #print ('      <DTMFDecode>0</DTMFDecode>')
                #print ('      <AMChanFlag>0</AMChanFlag>')
                #print ('    </Channel>')
                    
                with open(self._targetfile, 'a') as output_file:
                    output_file.write ('    <Channel Name=\"'+Name+'\" chanIndex=\"'+str(chanIndex)+'\">\n')
                    output_file.write ('      <BandWidth>'+str(Bandwidth)+'</BandWidth>\n')
                    output_file.write ('      <TxFreq>'+str(TxFreq).replace(".",",")+'</TxFreq>\n')
                    output_file.write ('      <RxFreq>'+str(RxFreq).replace(".",",")+'</RxFreq>\n')
                    output_file.write ('      <TxPowerLevel>'+str(TxPowerLevel)+'</TxPowerLevel>\n')
                    output_file.write ('      <AnaTxCTCFlag>'+str(AnaTxCTCFlag)+'</AnaTxCTCFlag>\n')
                    output_file.write ('      <AnaRxCTCFlag>'+str(AnaRxCTCFlag)+'</AnaRxCTCFlag>\n')
                    output_file.write ('      <AnaTxCTCIndex>'+str(AnaTxCTCIndex)+'</AnaTxCTCIndex>\n')
                    output_file.write ('      <AnaRxCTCIndex>'+str(AnaRxCTCIndex)+'</AnaRxCTCIndex>\n')
                    output_file.write ('      <FreqStep>2</FreqStep>\n')
                    output_file.write ('      <FreqReverseFlag>0</FreqReverseFlag>\n')
                    output_file.write ('      <EncryptFlag>0</EncryptFlag>\n')
                    output_file.write ('      <BusyNoTx>0</BusyNoTx>\n')
                    output_file.write ('      <PTTIdFlag>0</PTTIdFlag>\n')
                    output_file.write ('      <DTMFDecode>0</DTMFDecode>\n')
                    output_file.write ('      <AMChanFlag>0</AMChanFlag>\n')
                    output_file.write ('    </Channel>\n')

                logger.info(f"Channel {chanIndex} {Name} converted")
                converted_channels_list.append(f"Converted: {chanIndex} {Name}")
                

        # Open the input file again
        with open(self._cxffile, 'r') as infile:
            # Read all the lines into a list
            lines = infile.readlines()

        # Open the output file for appending
        with open(self._targetfile, 'a') as outfile:
            # Initialize a flag variable to False
            found_keyword = False

            # Loop through the lines and write them to the output file
            for line in lines:
                # Check if the line contains the keyword
                if '</Channels_MR>' in line:
                    # Set the flag variable to True to start copying lines
                    found_keyword = True

                # If the flag variable is True, write the line to the output file
                if found_keyword:
                    outfile.write(line)
        message = f"End of xcf file written to {self._targetfile}"
        logger.info(message)
        logger.info("'73 from G1LRO")
        logger.info("73 from OM0WT")
        return message, converted_channels_list      

class Ui_MainWindow(object):   
    
    # Files
    _chirpfile = ""
    _cxffile = ""
    _targetfile = ""
     
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1145, 707)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_7 = QtWidgets.QFrame(self.centralwidget)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame_7)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser_Disclaimer = QtWidgets.QTextBrowser(self.frame_3)
        self.textBrowser_Disclaimer.setObjectName("textBrowser_Disclaimer")
        self.verticalLayout.addWidget(self.textBrowser_Disclaimer)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.frame = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_selectCHIRPcsvFile = QtWidgets.QPushButton(self.frame)
        self.pushButton_selectCHIRPcsvFile.setObjectName("pushButton_selectCHIRPcsvFile")
        self.verticalLayout_6.addWidget(self.pushButton_selectCHIRPcsvFile)
        self.label_selectCHIRPcsvFile = QtWidgets.QLabel(self.frame)
        self.label_selectCHIRPcsvFile.setObjectName("label_selectCHIRPcsvFile")
        self.verticalLayout_6.addWidget(self.label_selectCHIRPcsvFile)
        self.pushButton_selectCPScxfFile = QtWidgets.QPushButton(self.frame)
        self.pushButton_selectCPScxfFile.setObjectName("pushButton_selectCPScxfFile")
        self.verticalLayout_6.addWidget(self.pushButton_selectCPScxfFile)
        self.label_selectCPScxfFile = QtWidgets.QLabel(self.frame)
        self.label_selectCPScxfFile.setObjectName("label_selectCPScxfFile")
        self.verticalLayout_6.addWidget(self.label_selectCPScxfFile)
        self.verticalLayout_2.addWidget(self.frame)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.frame_6 = QtWidgets.QFrame(self.frame_7)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textBrowser_ConvertedChannels = QtWidgets.QTextBrowser(self.frame_5)
        self.textBrowser_ConvertedChannels.setObjectName("textBrowser_ConvertedChannels")
        self.verticalLayout_3.addWidget(self.textBrowser_ConvertedChannels)
        self.verticalLayout_4.addWidget(self.frame_5)
        self.frame_4 = QtWidgets.QFrame(self.frame_6)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_Convert = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_Convert.setObjectName("pushButton_Convert")
        self.horizontalLayout.addWidget(self.pushButton_Convert)
        self.pushButton_Exit = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.horizontalLayout.addWidget(self.pushButton_Exit)
        self.verticalLayout_4.addWidget(self.frame_4)
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.verticalLayout_5.addWidget(self.frame_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_selectCHIRPcsvFile.clicked.connect(self.selectCHIRPcsv_clicked) # type: ignore
        self.pushButton_selectCPScxfFile.clicked.connect(self.selectCPScxf_clicked) # type: ignore
        self.pushButton_Convert.clicked.connect(self.Convert_clicked) # type: ignore
        self.pushButton_Exit.clicked.connect(self.exitApp) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def exitApp(self):
        app.exit(0)
        

    def doConvert(self):
        """_summary_
        """
        convertor = CXF_Convert(chirpfile=self._chirpfile, cxffile=self._cxffile, targetfile=self._targetfile)
        message, channels = convertor.csv2cxf()
        # self.label_newCPS_file.setText(message)
        self.textBrowser_ConvertedChannels.setText("\n".join(channels))
        MainWindow.setWindowTitle(f"Converted file saved to: {self._targetfile}")
              

    def selectCHIRPcsv_clicked(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        options = QFileDialog.Options()
        _translate = QtCore.QCoreApplication.translate
        filePath, filter = QFileDialog.getOpenFileName(None, "Select CHIRP csv file", "","CSV files (*.csv)", options=options)
        path = QtCore.QFileInfo(filePath).path()
        fileName = QtCore.QFileInfo(filePath).fileName()
        
        logger.debug(f"Filename {filePath}, placeholder: {filter}, path: {path}, basename: {fileName}")
        if filePath:
            if "csv" in filePath:
                self.label_selectCHIRPcsvFile.setText(f"{filePath}")
                # logger.debug(filePath)
                self._chirpfile = filePath  
            else:
                self._chirpfile = None
                self.label_selectCHIRPcsvFile.setText(f"Select CHIRP csv file again,{self._chirpfile} is not a .csv file, try again")
        else:
            self._chirpfile = None

    def selectCPScxf_clicked(self):
        options = QFileDialog.Options()
        filePath, filter = QFileDialog.getOpenFileName(None, "Select CPS .cxf file", "","CXF Files (*.cxf)", options=options)
        path = QtCore.QFileInfo(filePath).path()
        fileName = QtCore.QFileInfo(filePath).baseName()
        if filePath:
            if "cxf" in filePath:
                self.label_selectCPScxfFile.setText(f"{filePath}")
                # logger.debug(filePath)
                self._cxffile = filePath
                self._targetfile = f"{path}/processed_{fileName}.cxf"
            else:
                self.label_selectCPScxfFile.setText(f"Select CPS cxf file,{self._cxffile} is not a .cxf file, try again")
                self._cxffile = None            
        else:
            self._cxffile = None

    def Convert_clicked(self):
        self.doConvert()
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", " Quansheng UV-K5: chirp2cxf convertor"))
        self.textBrowser_Disclaimer.setText(_translate("MainWindow", disclaimer_box))
        self.pushButton_selectCHIRPcsvFile.setText(_translate("MainWindow", "Select CHIRP csv"))
        self.label_selectCHIRPcsvFile.setText(_translate("MainWindow", "CHIRP csv not selected"))
        self.pushButton_selectCPScxfFile.setText(_translate("MainWindow", "Select CPS cxf"))
        self.label_selectCPScxfFile.setText(_translate("MainWindow", "CPS cxf file not selected."))
        self.pushButton_Convert.setText(_translate("MainWindow", "Convert"))
        self.pushButton_Exit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="chirp2cxf",
        description=f"Convert CHIRP csv to Quansheng UV-K5 radio CPS",
        formatter_class=RawTextHelpFormatter,
        epilog="73 de Pavol OM0WT")

    parser.add_argument(
        "-chirpfile",
        dest="chirpfile",
        required=False,
        action='store',
        help="CHIRP csv file",
    )

    parser.add_argument(
        "-cxffile",
        required=False,
        dest="cxffile",
        action='store',
        help="CPS cxf file",
    )

    parser.add_argument(
        "-targetfile",
        dest="targetfile",
        required=False,
        action='store',
        help="Translated CPS cxf file",
    )

    args = parser.parse_args()
    if args.chirpfile and args.cxffile and args.targetfile:
        logger.debug(f"Translating from commandline: CHIRP csv: {args.chirpfile}, CPS cxf {args.cxffile} and translated cxf file: {args.targetfile}")
        convertor = CXF_Convert(chirpfile=args.chirpfile, cxffile=args.cxffile, targetfile=args.targetfile)
        convertor.csv2cxf()
    else:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())