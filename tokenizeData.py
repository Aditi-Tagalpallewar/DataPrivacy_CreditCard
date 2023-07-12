from faker import Faker
from readData import ATTNAME, getDataToList, printDataset


def tokenize(fileName):
    newFileData = getDataToList(fileName)

    indexName = ATTNAME.index("Name")
    indexEmail = ATTNAME.index("Email")

    newFaker = Faker()
    for rowIndex in range(1, len(newFileData)):
        newFileData[rowIndex][indexName] = newFaker.name()
        newFileData[rowIndex][indexEmail] = newFaker.email()

    with open(f"tokenized {fileName}", "w") as newData:
        for row in newFileData:
            temp = ",".join(row)
            newData.write(f"{temp}\n")

    # printDataset(f"tokenized {fileName}", rows=20)

tokenize("dataset.csv")