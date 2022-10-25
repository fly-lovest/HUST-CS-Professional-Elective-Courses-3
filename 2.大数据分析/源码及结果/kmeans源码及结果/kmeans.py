import csv
import random as rd
import numpy as np
import math
import matplotlib.pyplot as plt


def countDistance(center, sample):
    distance = 0.0
    for i in range(1, 14):
        distance += math.pow(center[i]-sample[i], 2)
    return distance


def get_sse(process_mindata, sampnum):
    ssenum = [0, 0, 0]
    sse = 0
    for i in range(sampnum):
        ssenum[int(process_mindata[i, 1]) - 1] += process_mindata[i, 0]
    for i in range(k):
        sse += ssenum[i]
        print("the ", i+1, ssenum[i])
    print("ALL ", sse)


def get_acc(process_mindata, sampnum):
    cluster1 = [0, 0, 0]
    cluster2 = [0, 0, 0]
    cluster3 = [0, 0, 0]
    # 类1:59  类2:71  类3:48
    for i in range(59):
        index = int(process_mindata[i, 1])
        if index == 1:
            cluster1[0] += 1
        elif index == 2:
            cluster2[0] += 1
        else:
            cluster3[0] += 1
    for i in range(59, 130):
        index = int(process_mindata[i, 1])
        if index == 1:
            cluster1[1] += 1
        elif index == 2:
            cluster2[1] += 1
        else:
            cluster3[1] += 1
    for i in range(130, sampnum):
        index = int(process_mindata[i, 1])
        if index == 1:
            cluster1[2] += 1
        elif index == 2:
            cluster2[2] += 1
        else:
            cluster3[2] += 1
    acc = 0
    acc += max(cluster1[0], cluster1[1], cluster1[2])
    acc += max(cluster2[0], cluster2[1], cluster2[2])
    acc += max(cluster3[0], cluster3[1], cluster3[2])
    acc = acc / sampnum
    print("acc:", acc)


if __name__ == '__main__':
    # 提取数据
    samples = []
    with open('normalizedwinedata.csv') as f:
        read_data = csv.reader(f)
        for row in read_data:
            samples.append(row)
    samples = [[float(x) for x in row] for row in samples]
    sample_num = len(samples)
    # 设定k与初始化k个聚类中心，13维度
    k = 3
    centers = []
    for i in range(k):
        c = []
        c.append(0)  # 占位作用
        for j in range(13):
            c.append(rd.random())
        centers.append(c)
    flag = True
    counter = 0
    process_mindata = np.mat(np.zeros((sample_num, 2)))
    # 矩阵行指示样点，第1列指示过程最小距离，第2列指示所属类簇
    # 设置最大迭代次数为100
    while flag and counter < 100:
        flag = False
        for i in range(sample_num):
            min_distance = 10000.0  # 最短距离
            min_center = 0              # 所属类簇，1，2，3
            for j in range(k):
                distance = countDistance(centers[j], samples[i])
                if distance < min_distance:
                    min_distance = distance
                    min_center = j + 1
            if process_mindata[i, 0] != min_distance or process_mindata[i, 1] != min_center:
                process_mindata[i, 0] = min_distance
                process_mindata[i, 1] = min_center
                flag = True
        # 更新类簇中心
        for i in range(k):
            # 获取当前类簇的样本点
            new_point = []
            for j in range(sample_num):
                if process_mindata[j, 1] == i + 1:
                    new_point.append(samples[j])
            centers = np.array(centers)
            centers[i, :] = np.mean(new_point, axis=0)
        counter += 1
    print("run times:", counter)
    get_sse(process_mindata, sample_num)
    get_acc(process_mindata, sample_num)

    x = 6  # 总酚
    y = 7  # 黄酮
    plt.xlabel('Zong Fen')
    plt.ylabel('Huang Tong')
    plt.axis([0, 1, 0, 1])
    for i in range(sample_num):
        if int(process_mindata[i, 1]) == 1:
            plt.scatter(samples[i][x], samples[i][y], c='r')
        elif int(process_mindata[i, 1]) == 2:
            plt.scatter(samples[i][x], samples[i][y], c='g')
        else:
            plt.scatter(samples[i][x], samples[i][y], c='b')
    plt.show()
    print("DONE")
