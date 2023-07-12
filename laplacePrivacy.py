import numpy
import math
import random
from readData import *


class LaplaceMechanism():
    def __init__(self, records):
        self.records = records
        self.s = self.__calculate_sensitivity()

    def __calculate_sensitivity(self):
        """
        calculate the sensitive value
        it should be the oldest Age / num of records

        Returns:
            [float] -- [sensitive value]
        """

        num, oldAge = 0, -float('inf')
        Ageidx = ATTNAME.index('Age')
        for record in self.records:
            if record[Ageidx] > 35:
                num += 1
                if record[Ageidx] > oldAge:
                    oldAge = record[Ageidx]
        return oldAge / num

    def __laplacian_noise(self, e):
        """
        add laplacian_noise
        """

        return numpy.random.laplace(self.s / e)

    def query_with_dp_Lap(self, e=1, querynum=1000):
        """
        ADDING NOISE TO THE RECORDS
        query averAge Age above 25 with Laplace Mechanism

        Keyword Arguments:
            e {float} -- [epsilon] (default: {1})
            querynum {int} -- [number of queries] (default: {1000})

        Returns:
            [list] -- [randomized query results]
        """

        Ageidx = ATTNAME.index('Age')
        Agegt25 = [record[Ageidx] for record in self.records if record[Ageidx] > 25]
        avgAge = sum(Agegt25) / len(Agegt25)

        res = []
        for _ in range(querynum):
            res.append(round(avgAge + self.__laplacian_noise(e), 2))
        return res

    def calc_groundtruth_Lap(self):
        """
        calculate the true averAge Age above 25 without adding noise

        Returns:
            [float] -- [true averAge Age greater than 25]
        """

        Agesum = 0
        num = 0
        Ageidx = ATTNAME.index('Age')
        for record in self.records:
            if record[Ageidx] > 35:
                Agesum += record[Ageidx]
                num += 1
        return round(Agesum / num, 2)

    def calc_distortion_Lap(self, queryres):
        """
        calcluate the distortion
        use RMSE here

        Arguments:
            queryres {[list]} -- [query result]

        Returns:
            [float] -- [rmse value]
        """

        groundtruth = self.calc_groundtruth_Lap()
        rmse = (sum((res - groundtruth) ** 2 for res in queryres) /
                len(queryres)) ** (1 / 2)
        return rmse


def prove_indistinguishable_Lap(queryres1, queryres2, bucketnum=20):
    """
    prove the indistinguishable for two query results

    Arguments:
        queryres1 {[list]} -- [query 1 result]
        queryres2 {[list]} -- [query 2 result]

    Keyword Arguments:
        bucketnum {int} -- [number of buckets used to calculate the probability] (default: {20})

    Returns:
        [float] -- [probability quotient]
    """

    maxval = max(max(queryres1), max(queryres2))
    minval = min(min(queryres1), min(queryres2))
    count1 = [0 for _ in range(bucketnum)]
    count2 = [0 for _ in range(bucketnum)]
    for val1, val2 in zip(queryres1, queryres2):
        count1[math.floor((val1 - minval + 1) / ((maxval - minval + 1) / bucketnum)) - 1] += 1
        count2[math.floor((val2 - minval + 1) // ((maxval - minval + 1) / bucketnum)) - 1] += 1
    prob1 = list(map(lambda x: x / len(queryres1), count1))
    prob2 = list(map(lambda x: x / len(queryres2), count2))

    res1overres2 = sum(p1 / p2 for p1, p2 in zip(prob1, prob2) if p2 != 0) / bucketnum
    res2overres1 = sum(p2 / p1 for p1, p2 in zip(prob1, prob2) if p1 != 0) / bucketnum
    return res1overres2, res2overres1


def generate_data_for_laplace_mechanism(records):
    """
    generate the three different versions datasets for Laplace Mechanism

    Arguments:
            records {[list of list]} -- [original records for adult datasets]

    Returns:
            three versions datasets for Laplace Mechanism
            oldest Age and youngest Age
    """

    oldestidx, twentysixidx, youngestidx = -1, -1, -1
    oldest, youngest = -float('inf'), float('inf')
    Ageidx = ATTNAME.index('Age')
    for idx, record in enumerate(records):
        """
        Age == -1 means the value is missing in the dataset
        """
        if record[Ageidx] == -1:
            continue
        if record[Ageidx] >= oldest:
            if record[Ageidx] != oldest or random.random() >= 0.5:
                oldestidx, oldest = idx, record[Ageidx]
        if record[Ageidx] <= youngest:
            if record[Ageidx] != youngest or random.random() >= 0.5:
                youngestidx, youngest = idx, record[Ageidx]
        if record[Ageidx] == 35 and (twentysixidx != -1 or random.random() >= 0.5):
            twentysixidx = idx
    version1 = copy_with_exclude_idx(records, oldestidx)
    version2 = copy_with_exclude_idx(records, twentysixidx)
    version3 = copy_with_exclude_idx(records, youngestidx)
    return version1, version2, version3


# eps = [0.5, 1]
# res1000 = {e : [] for e in eps}
# rmse = {e : 0 for e in eps}
# print(res1000, rmse)


def evaluate_laplace_mechanism(eps, dataset):
    """
    Evaluate for Laplace Mechanism
    """
    recordsv0 = readdata(dataset)
    recordsv1, recordsv2, recordsv3 = generate_data_for_laplace_mechanism(recordsv0)

    res1000 = {e: [] for e in eps}
    rmse = {e: 0 for e in eps}

    """
    evaluate for epsilon = 0.5 and 1 for 1000 queries
    """
    printsent = ['original data', 'data removed a record with the oldest Age', 'data removed any record with Age 35', 'data removed any record with the youngest Age']
    i = 0
    for records in (recordsv0, recordsv1, recordsv2, recordsv3):
        print('############ Processing for {} ############'.format(printsent[i]))
        i += 1
        LampMec = LaplaceMechanism(records)
        for e in eps:
            print('query 1000 results with epsilon = {}'.format(e))
            res1000[e].append(LampMec.query_with_dp_Lap(e, querynum=1000))
            rmse[e] = LampMec.calc_distortion_Lap(LampMec.query_with_dp_Lap(e, querynum=4000))

    print('\n')
    for e in eps:
        print('############ Prove the {}-indistinguishable'.format(e))
        for i in range(1, 4):
            tmpresij, tmpresji = prove_indistinguishable_Lap(
                res1000[e][0], res1000[e][i])
            print('** {} ** OVER ** {} **:'.format(printsent[0], printsent[i]))
            print(tmpresij)
            print('** {} ** OVER ** {} **:'.format(printsent[i], printsent[0]))
            print(tmpresji)
            print('exp^e = {}'.format(math.exp(e)))
            print('\n')

    print('############ Measure the distortion (RMSE) ############')
    for e in eps:
        print('RMSE for e = {}: {}'.format(e, rmse[e]))
    print('Distortion of e=1 is smaller than e=0.5 ?: ', True if rmse[1] <= rmse[0.5] else False)
    del recordsv0
    del recordsv1
    del recordsv2
    del recordsv3