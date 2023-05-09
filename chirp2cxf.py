import csv
import sys


try:
    chirpfile = sys.argv[1]
    cxffile = sys.argv[2]

except IndexError:
    # Handle missing arguments
    print("Usage: chirp2cxf.exe chirpfile.csv quanshengfile.cxf")
    sys.exit(1)    

#chirpfile = 'chirp.csv'
#cxffile = 'que.cxf'


if "csv" in chirpfile:
    print (chirpfile, 'opened for reading')
else:
    print (chirpfile,"is not a .csv file")
    sys.exit()

    
if "cxf" in cxffile:
    print (cxffile, 'opened for reading')
else:
    print (cxffile,"is not a .cxf file")
    sys.exit()


targetfile = "processed_"+cxffile


print ('Output will be written to',targetfile)

#ctcss data
ctcss_tones = [
    67.0, 69.3, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5,
    94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3,
    131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 159.8, 162.2, 165.5, 167.9,
    171.3, 173.8, 177.3, 179.9, 183.5, 186.2, 189.9, 192.8, 196.6, 199.5,
    203.5, 206.5, 210.7, 218.1, 225.7, 229.1, 233.6, 241.8, 250.3
    ]

#set these varibles if the CtCss is not in the table
AnaTxCTCIndex=0
AnaRxCTCIndex=0




#copy top parf of CXF file to the new file

with open(cxffile, 'r') as input_file:
    # open the output file for writing
    with open(targetfile, 'w') as output_file:
        # read each line from the input file
        for line in input_file:
            # write the line to the output file
            output_file.write(line)
            # check if the line contains the target word
            if '<Channels_MR>' in line:
                # if so, stop reading and writing
                break



print ("First part of cxf file written")

# Open the CSV file
with open(chirpfile, mode='r') as csv_file:
    
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
        if float(rToneFreq) in ctcss_tones:
            AnaTxCTCIndex = ctcss_tones.index(float(rToneFreq))
        if float(cToneFreq) in ctcss_tones:
            AnaRxCTCIndex = ctcss_tones.index(float(cToneFreq))


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
        
        
        # Do something with the variables
        #print(Location, " ", Name, " ", Rxfreq," ", Duplex, " ",Offset, " ",Txfreq, "rToneFreq =", AnaTxCTCIndex)

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



        with open(targetfile, 'a') as output_file:
            output_file.write ('    <Channel Name=\"'+Name+'\" chanIndex=\"'+str(chanIndex)+'\">\n')
            output_file.write ('      <BandWidth>'+str(Bandwidth)+'</BandWidth>\n')
            output_file.write ('      <TxFreq>'+str(TxFreq)+'</TxFreq>\n')
            output_file.write ('      <RxFreq>'+str(RxFreq)+'</RxFreq>\n')
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

        print ("Channel",chanIndex,"converted")

# Open the input file again
with open(cxffile, 'r') as infile:
    # Read all the lines into a list
    lines = infile.readlines()

# Open the output file for appending
with open(targetfile, 'a') as outfile:
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
print ("End of xcf file written to processed_"+cxffile )
print ("'73 from G1LRO")
