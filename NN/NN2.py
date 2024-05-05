import sys;  args = sys.argv[1:]
import math
import random




def performTransferFunc(transferFunction,val):
    if transferFunction == 1:
        return val

    if transferFunction == 2:
        return val * (val>0)
    if transferFunction == 3:
        return 1/(1+math.exp(-val))
    if transferFunction == 4:
        return (1/(1+math.exp(-val)))* 2 -1




def dotProduct(v1,v2):
    allProds = []
    for i, n in enumerate(v1):
        allProds.append(n*v2[i])
    return sum(allProds)



def feedForward(inps,weights,transferFunction): #returns all node values starting with inputs all the way to final node, along with weights for every layer
    nodeVals = []
    

    nodeVals.append(inps)
    mostRecentXs = inps
    #print(weights,inps)
    for n in range(len(weights)-1):
        numNodesInNextLayer = int(len(weights[n])/len(mostRecentXs))
        nodesInNextLayer = []
        inc = 0
        for i in range(numNodesInNextLayer):
            dotProdded = dotProduct(mostRecentXs, weights[n][inc:inc + len(mostRecentXs)])
            inc +=len(mostRecentXs)
            #transferred = dotProdded
            transferred = performTransferFunc(3,dotProdded)
            nodesInNextLayer.append(transferred)
        nodeVals.append(nodesInNextLayer)
        mostRecentXs = nodesInNextLayer
    penultimateLayer = nodeVals[-1]
    inc = 0
    finalLayer = []

    for i in range(numNodesInNextLayer):
        dotProdded = dotProduct(penultimateLayer, weights[-1][inc:inc + len(penultimateLayer)])
        inc +=len(penultimateLayer)
        finalLayer.append(dotProdded)
    nodeVals.append(finalLayer)


    return nodeVals


def transferDeriv(transferFunction,val,x = True): # if x is false then it is the y value
    if transferFunction == 3:
        if x == True:
            return performTransferFunc(val) * (1-performTransferFunc(val))
        else:
            return val * (1-val)


def backProp(nodeVals,weights,transferFunction, realOutput):        
    negativeGradient = []
    for i in range(len(weights)):
        newLayer = []
        for u in range(len(weights[i])):
            newLayer.append(0)
        negativeGradient.append(newLayer)

    errorWRTy = []
    for i in range(len(nodeVals)):
        newLayer = []
        for u in range(len(nodeVals[i])):
            newLayer.append(0)
        errorWRTy.append(newLayer)

    #last layer for negative gradient will always be 1 less than last layer for nodeVals
    errorWRTy[-1][0] = realOutput[0]-nodeVals[-1][0] #can change this for all nodes
    negativeGradient[-1][0]  = nodeVals[-2][0] *  realOutput[0]-nodeVals[-1][0]
    inc = 0
    for layer in range(len(errorWRTy)-2,-1,-1):
        if inc == 0: # layer is the second to last layer
            for i in range(len(errorWRTy[layer])):
                errorWRTy[layer][i] = errorWRTy[layer+1][i]*weights[layer][i] * transferDeriv(3,nodeVals[layer][i],True)




        else:
            for i in range(len(errorWRTy[layer])):
                pass
        inc +=1











def main():
    fileName = args[0]
    linesOfFile = open(args[0]).read().splitlines()
    allInputs = []
    realOutputs = []

    for line in linesOfFile:
        splitted = line.split("=>")
        left = splitted[0]
        right  = splitted[1]
        inps = left.split(" ")
        newinps= []
        for i in range(len(inps)):
            if inps[i] != "":
                newinps.append(inps[i])
        inps = newinps
        inps = [int(i) for i in inps]
        outs = right.split(" ")
        newouts = []
        for i in range(len(outs)):
            if outs[i]:
                newouts.append(outs[i])
        outs = newouts
        outs = [int(i) for i in outs]
        allInputs.append(inps)
        realOutputs.append(outs)
    


    numInputs = len(allInputs[0])
    nodeCts = [numInputs+1,2,1,1]
    initialWeights = []
    for i in range(len(nodeCts)-1):
        ct = nodeCts[i]
        numWts = ct * nodeCts[i+1]
        wts = []
        for n in range(numWts):
            wts.append(random.random())
        initialWeights.append(wts)

    layerCtStr = "Layer counts: "
    for i in nodeCts:
        layerCtStr+=str(i) + " "
    for i in range(len(allInputs)):
        allInputs[i].insert(0,1) #putting bias of 1 into the beginning (0th index)
    weights = initialWeights
    for epoch in range(1):
        for ind, currInps in enumerate(allInputs):
            
            #do forward prop to get network
            nodeVals = feedForward(currInps,weights,3)
            # print(nodeVals)
            # print(weights)
            backProp(nodeVals,weights,3,realOutputs[ind])
            #do backprop 
        





if __name__ == '__main__': main()


# Anmol Karan, pd 3, 2025            
