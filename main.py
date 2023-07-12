from pandas import DataFrame
from laplacePrivacy import *
# from exponentialPrivacy import *
from readData import *
from tokenizeData import tokenize
from supressData import supress

if __name__ == "__main__":
    # rawFile = input("Enter file name (please specify the path if not in the same directory): ")
    rawFile = "dataset.csv"

    tokenize(rawFile)
    print("Dataset has been Tokenised")

    fileData = []
    with open(f"tokenized {rawFile}", 'r') as data:
        for line in data:
            row = line.strip()
            if not line:
                continue
            row = [a.strip() for a in line.split(',')]
            fileData.append(row)
    fileData.remove(fileData[0])
    
    with open(f"new{rawFile}", "w") as newData:
        for row in fileData:
            temp = ",".join(row)
            newData.write(f"{temp}\n")
    
    supress(f"new{rawFile}")
    print("Dataset has been suppressed ")

    fileData = []
    with open(f"supressed new{rawFile}", 'r') as data:
        for line in data:
            row = line.strip()
            if not line:
                continue
            row = [a.strip() for a in line.split(',')]
            fileData.append(row)
    fileData.remove(fileData[0])
    
    with open(f"new{rawFile}", "w") as newData:
        for row in fileData:
            temp = ",".join(row)
            newData.write(f"{temp}\n")

    rawFile = f"new{rawFile}"

    dataSet = readdata(rawFile)
    print("Final dataset")
    df1 = DataFrame(dataSet, columns=ATTNAME)
    rows = sum(1 for _ in open(rawFile))
    print(f"Number of entries in the data sets are: {rows}")
    df1.head(rows)
    print("\n############################################################## Laplace Mechanism ##############################################################")
    evaluate_laplace_mechanism([0.5, 1], rawFile)
    
    # print('\n\n\n\n\n')
    # print("############################################################## Exponential Mechanism ##############################################################")
    # evaluate_exponential_mechanism([0.5, 1], rawFile)
