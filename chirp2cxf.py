import csv

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
        if Duplex == "-":
            Transmit = float(Frequency) - float(Offset)
        Transmit = float(Frequency) + float(Offset)
        Transmit = round(Transmit,6)



        
        
        # Do something with the variables
        print(Location, " ", Name, " ", Frequency," ", Duplex, " ",Offset, " ",Transmit)
