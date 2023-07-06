import time
import math


# 计算两个数据点之间的优势差异
def count_diffs(a, b):
    n_better = 0  # 统计a中有多少维度优于b
    n_worse = 0   # 统计a中有多少维度劣于b
    length = len(a)
    for i in range(length):
        n_better += a[i] > b[i]
        n_worse += a[i] < b[i]
    return n_better, n_worse


# 基于BNL算法的天际线查询
def skyline_bnl(input_file):
    data = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            data.append(list(map(float, line.split())))

    skyline_index = [0]  # 初始化天际线的索引列表，初始时包含第一个数据点

    for i in range(1, len(data)):
        to_drop = []    # 用于存储待删除的天际线点的索引列表
        is_dominate = False  # 表示当前数据点是否被其他天际线点支配

        for j in skyline_index:
            n_better, n_worse = count_diffs(data[i], data[j])

            # 如果存在其他天际线点支配当前数据点，则设置is_dominate标志为True，并跳出循环
            if n_worse > 0 and n_better == 0:
                is_dominate = True
                break
            # 如果当前数据点支配其他天际线点，则将其他天际线点添加到待删除列表中
            if n_better > 0 and n_worse == 0:
                to_drop.append(j)

        # 如果当前数据点被其他天际线点支配，则跳过继续处理下一个数据点
        if is_dominate:
            continue

        # 从当前天际线索引列表中去除被支配的数据点，并将当前数据点添加到天际线索引列表中
        skyline_index = list(set(skyline_index).difference(set(to_drop)))
        skyline_index.append(i)

    # 根据天际线索引列表，获取所有天际线数据点
    skyline_points = []
    for index in skyline_index:
        skyline_points.append(data[index])

    return skyline_index, skyline_points


# 计算数据点的熵值并进行SFS排序
def skyline_sfs(input_file):
    data = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_data = list(map(float, line.split()))
            entropy = 0
            for i in range(len(line_data)):
                entropy += math.log(line_data[i] + 1)
            data.append([line_data, entropy])
    data.sort(key=lambda item: item[1], reverse=True)

    # 将排序后的数据点写入文件以备后续使用
    sfsFile = open('data/sfs_pre.txt', 'w')
    for row in data:
        sfsFile.write(" ".join(map(str, row[:-1][0])) + "\n")
    sfsFile.close()

    # 调用基于BNL的天际线查询函数处理S
    return skyline_bnl('data/sfs_pre.txt')

#更改数据集文件
txt = 'data_3'
file = 'data/' + txt + '.txt'

#使用BNL算法进行天际线查询
bnl_start_time = time.time()
bnl_skyline_index, bnl_skyline_points = skyline_bnl(file)
print(f'BNL: {time.time() - bnl_start_time:.3f} seconds')

#将BNL算法的天际线结果写入文件
result_file = open('result/bnl_' + txt + '.txt', 'w')
for row in bnl_skyline_points:
    result_file.write(" ".join(map(str, row[:])) + "\n")
result_file.close()

#使用SFS算法进行天际线查询
sfs_start_time = time.time()
sfs_skyline_index, sfs_skyline_points = skyline_sfs(file)
print(f'SFS: {time.time() - sfs_start_time:.3f} seconds')

#将SFS算法的天际线结果写入文件
result_file = open('result/sfs_' + txt + '.txt', 'w')
for row in sfs_skyline_points:
    result_file.write(" ".join(map(str, row[:])) + "\n")
result_file.close()
