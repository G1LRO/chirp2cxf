import csv
#ctcss data
ctcss_tones = [
    67.0, 69.3, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5,
    94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3,
    131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 159.8, 162.2, 165.5, 167.9,
    171.3, 173.8, 177.3, 179.9, 183.5, 186.2, 189.9, 192.8, 196.6, 199.5,
    203.5, 206.5, 210.7, 218.1, 225.7, 229.1, 233.6, 241.8, 250.3
    ]

# Open the CSV file
with open('chirp.csv', mode='r') as csv_file:
    
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
        rToneFreq = row['rToneFreq']
        cToneFreq = row['cToneFreq']
        DtcsCode = row['DtcsCode']
        DtcsPolarity = row['DtcsPolarity']
        RxDtcsCode = row['RxDtcsCode']
        CrossMode = row['CrossMode']
        TStep = row['TStep']
        Skip = row['Skip']
        Power = row['Power']
        
        #Start field translation  
        
        #Calculate Transmit from Recieve and Offset
        Transmit = float(Frequency) + float(Offset)
        if Duplex == "-":
            Transmit = float(Frequency) - float(Offset)
        Transmit = round(Transmit,6)



        
        
        # Do something with the variables
        print(Location, " ", Name, " ", Frequency," ", Duplex, " ",Offset, " ",Transmit)
