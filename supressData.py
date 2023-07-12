from readData import ATTNAME, getDataToList, printDataset

def supress(fileName):
    newFileData = getDataToList(fileName)

    indexZipCode = ATTNAME.index("Zip_Code")

    for rowIndex in range(1, len(newFileData)):
        newFileData[rowIndex][indexZipCode] = "411***"

    with open(f"supressed {fileName}", "w") as newData:
        for row in newFileData:
            temp = ",".join(row)
            newData.write(f"{temp}\n")
    
    # printDataset(f"supressed {fileName}", rows=20)

# supressData("dataset.csv")