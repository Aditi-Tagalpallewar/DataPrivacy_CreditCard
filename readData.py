ATTNAME = ["Account_Number", "Card_Number", "Name", "Age", "Email", "Zip_Code", "Account_Balance", "Card_Limit"]


def readdata(filename):
    records = []
    with open(filename, 'r') as rf:
        for line in rf:
            line = line.strip()
            if not line:
                continue
            line = [a.strip() for a in line.split(',')]
            intidx = [ATTNAME.index(colname) for colname in ('Age', 'Account_Balance', 'Card_Limit')]
            for idx in intidx:
                try:
                    line[idx] = int(line[idx])
                except:
                    print('attribute %s, value %s, cannot be converted to number' % (ATTNAME[idx], line[idx]))
                    line[idx] = -1
            for idx in range(len(line)):
                if line[idx] == '' or line[idx] == '?':
                    line[idx] = '*'
            records.append(line)
    return records


def copy_with_exclude_idx(records, tgtidx):
    """
    generate a new list of records without the target idx: tgtidx

    Arguments:
            records {[list of list]} -- [original records]
            tgtidx {[int]} -- [target idx will be excluded from records]

    Returns:
            [list of list] -- [copy of records excluding the tgtidx record]
    """

    return [record for idx, record in enumerate(records) if idx != tgtidx]


def getDataToList(fileName):
    fileData = []
    with open(fileName, 'r') as data:
        fileData.append(ATTNAME)
        for line in data:
            row = line.strip()
            if not line:
                continue
            row = [a.strip() for a in line.split(',')]
            fileData.append(row)
    return fileData.copy()


def printDataset(fileName, rows=20):
    data = getDataToList(fileName)
    for index in range(1, rows):
        line = "\t".join(data[index])
        print(f"{line}\n")