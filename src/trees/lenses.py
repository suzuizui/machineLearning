# encoding:utf-8

"""
隐形眼镜推荐
"""
import treePlotter
import trees

fr = open('lenses.txt')
lenses = [instr.strip().split('\t') for instr in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = trees.createTree(lenses, lensesLabels)
print lensesTree
treePlotter.createPlot(lensesTree)
