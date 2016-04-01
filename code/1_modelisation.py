# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

import os
import re
import collections
import random

def cleanS(s):
    s_clean = re.sub(r'([^\s\w]|_)+', ' ', s.lower())
    s_clean = re.sub(' +',' ', ' '.join(s_clean.split("\n")))
    return s_clean

clusters = {"comp.graphics":1, "comp.os.ms-windows.misc":1, "comp.sys.ibm.pc.hardware":1, "comp.sys.mac.hardware":1, \
            "comp.windows.x":1, "rec.autos":2, "rec.motorcycles":2, "rec.sport.baseball":2, "rec.sport.hockey":2, \
            "sci.crypt":3, "sci.electronics":3, "sci.med":3, "sci.space":3, "misc.forsale":4, "talk.politics.misc":5, \
            "talk.politics.guns":5, "talk.politics.mideast":5, "talk.religion.misc":6, "alt.atheism":6, "soc.religion.christian":6}

###
### Preprocessing
###

repo = os.listdir("../20_newsgroups/")

w = open("../data/d.txt", 'w')

for repoTemp in repo:
    fileNames = os.listdir("../20_newsgroups/" + repoTemp)
    for fileName in fileNames:
        fileTemp = open("../20_newsgroups/" + repoTemp + '/' + fileName, 'r')
        content = ' '.join(fileTemp.readlines()).split('Lines:')
        if len(content)>1:
            content = ' '.join(content[1].splitlines())
            classCounter[clusters[repoTemp]] = classCounter.get(clusters[repoTemp], 0) + 1
            
            w.write(str(clusters[repoTemp]) + ' |X ' + cleanS(content) + "\n")
            
###
### Build Train and Test data
###

d = open("../data/d.txt", 'r').readlines()

dByClass = {}
for x in d:
    dByClass[x[0]] = dByClass.get(x[0], []) + [x]
    
for idClass in dByClass.keys():
    random.shuffle(dByClass[idClass])

dTrain = []
dTest = []

for idClass in dByClass.keys():
    for i,v in enumerate(dByClass[idClass]):
        if i < 900:
            dTest += [v]
        else:
            dTrain += [v]
            
random.shuffle(dTrain)
random.shuffle(dTest)

# Save data
wTrain = open("../data/dTrain.txt", 'w')
for x in dTrain:
    wTrain.write(x)
wTrain.close()

wTest = open("../data/dTest.txt", 'w')
for x in dTest:
    wTest.write(x)
wTest.close()

###
### Run Vowpal (initialisation step)
###

# Learn model
os.system("vw ../data/dTrain.txt -c -k -b 26 -f ../models/model0.vw --oaa 6 --passes 3")

# Compute predictions
os.system("vw -i ../models/model0.vw -t ../data/dTest.txt -p ../results/predictions0.txt")

###
### Compute weights
###

def getWeights(fileTrain, filePredictions):
    p = open(fileTrain, "r").readlines()
    p = [int(x[0]) for x in p]    
    clusterFreqTrain = collections.Counter(p)
    
    p = open(filePredictions, "r").readlines()
    p = [int(x[0]) for x in p]    
    clusterFreqTest = collections.Counter(p)
    
    clusterWeight = {str(k):float(clusterFreqTest[k])/float(clusterFreqTrain[k]) for k in clusterFreqTest.keys()}
    return clusterWeight

def addWeights(d, d_new, clusterWeight):
    d_origin = open(d, "r")
    d_all = d_origin.readlines()
    
    d_weighted = open(d_new, "w")
    for x in d_all:
        xSplit = x.split(' ')
        d_weighted.write(x[0] + ' ' + str(clusterWeight.get(x[0], 0)) + ' ' + ' '.join(xSplit[1:]))
    
    d_origin.close()
    d_weighted.close()
    return "weights added"

### Compute 19 Iterations
for iteration in range(1,20):
    print iteration
    clusterWeight = getWeights(fileTrain = "../data/dTrain.txt", filePredictions = "../results/predictions" + str(iteration - 1) + ".txt")
    addWeights("../data/dTrain.txt", "../data/dTrain" + str(iteration) + ".txt", clusterWeight)
    #addWeights("../data/dTest.txt", "../data/dTest" + str(iteration) + ".txt", clusterWeight)
    
    os.system("vw ../data/dTrain" + str(iteration) + ".txt -c -k -b 26 -f ../models/model" + str(iteration) + ".vw --oaa 6 --passes 3")
    os.system("vw -i ../models/model" + str(iteration) + ".vw -t ../data/dTest.txt -p ../results/predictions" + str(iteration) + ".txt")


