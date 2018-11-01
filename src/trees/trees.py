# encoding:utf-8
'''
Created on Oct 12, 2010
Decision Tree Source Code for Machine Learning in Action Ch. 3
@author: Peter Harrington
    ID3决策树算法
'''
import operator
from math import log

import treePlotter


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    # change to discrete values
    return dataSet, labels


def calcShannonEnt(dataSet):
    """
    计算给定数据集的香农熵
    :param dataSet:数据集
    :return: 熵
    """
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:  # the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)  # log base 2
    return shannonEnt


def splitDataSet(dataSet, axis, value):
    """
    按照给定的特征划分数据集
    :param dataSet: 待划分的数据集
    :param axis: 划分数据集的特征
    :param value: 命中的特征值
    :return:
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]  # chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    """
    选择最好的数据集划分方式
    :param dataSet: 数据集
    :return: best特征值的下标
    """
    numFeatures = len(dataSet[0]) - 1  # 最后一列是分类值
    baseEntropy = calcShannonEnt(dataSet)  # 总熵
    bestInfoGain = 0.0;  # 最好的信息增益
    bestFeature = -1
    for i in range(numFeatures):  # iterate over all the features
        featList = [example[i] for example in dataSet]  # 创建唯一的分类标签列表
        uniqueVals = set(featList)  # get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:  # 计算每种划分方式的信息熵
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy  # calculate the info gain; ie reduction in entropy
        if (infoGain > bestInfoGain):  # 信息增益是熵的减少，信息无序度的减少，所以要选熵最小的
            bestInfoGain = infoGain  # if better than current best, set to best
            bestFeature = i
    return bestFeature  # returns an integer


def majorityCnt(classList):
    """
    当数据集已经消耗了所有的特征，分类扔不唯一的时候
    需要在当前数据集中使用多数表决的方法
    :param classList:
    :return:
    """
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    """
    递归的创建决策树
    :param dataSet: 数据集
    :param labels:  标签列表
    :return:
    """
    classList = [example[-1] for example in dataSet]  # 分类列表
    if classList.count(classList[0]) == len(classList):
        return classList[0]  # 所有的类标签相等
    if len(dataSet[0]) == 1:  # 列数等于1，所有的特征值均已经使用完
        return majorityCnt(classList)  # 多数表决
    # 选择最好的划分数据集的特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]  # copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


def classify(inputTree, featLabels, testVec):
    """
    用决策树获取分类(递归)
    :param inputTree: 决策树
    :param featLabels: 特征列表
    :param testVec: 特征值列表
    :return: 记录的分类
    """
    # 获得根节点的特征
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    # 将标签字符串转换为索引数字
    featIndex = featLabels.index(firstStr)
    # 获得特征的值是多少
    key = testVec[featIndex]
    # 获得子树或者叶节点
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        # 如果是叶节点，则返回
        classLabel = valueOfFeat
    return classLabel


def storeTree(inputTree, filename):
    """
    存储决策树(学习结果)
    :param inputTree: 决策树
    :param filename: 文件名称
    """
    import pickle
    fw = open(filename, 'w')
    # 序列化对象并存储
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    """
    读取决策树
    :param filename:文件名称
    :return:
    """
    import pickle
    fr = open(filename)
    return pickle.load(fr)
