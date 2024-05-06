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
        if x == False:
            return performTransferFunc(3,val) * (1-performTransferFunc(3,val))
        else:
            return val * (1-val)


def backProp(nodeVals,weights,transferFunction, realOutput): 
     
    negativeGradient = []
    for i in range(len(weights)):
        newLayer = []
        for _ in range(len(weights[i])):
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
    negativeGradient[-1][0]  = nodeVals[-2][0] *  (realOutput[0]-nodeVals[-1][0])
    inc = 0
    for layer in range(len(errorWRTy)-2,0,-1):
 

        if inc == 0: # layer is the second to last layer
            for i in range(len(errorWRTy[layer])):
                errorWRTy[layer][i] = errorWRTy[layer+1][i]*weights[layer][i] * transferDeriv(3,nodeVals[layer][i],True)



        else:
            for i in range(len(nodeVals[layer])):
                #wtsForDotProduct = [ind for ind ,v in enumerate(weights[layer]) if ind%len(errorWRTy[layer]) == i]

                dotProdded = dotProduct(errorWRTy[layer+1],weights[layer][i::len(nodeVals[layer])]) #otherwise maybe use slicing if wtsForDotProduct doesnt work
                #dotProdded = dotProduct(errorWRTy[layer+1],wtsForDotProduct)
                errorWRTy[layer][i] = dotProdded * transferDeriv(3,nodeVals[layer][i],True)
        inc +=1
    
    

    for ind, layer in enumerate(errorWRTy):
        if ind == 0:
            continue
        for i in range(len(negativeGradient[ind-1])):
            
            negativeGradient[ind-1][i] = layer[int(i/len(nodeVals[ind-1]))]* nodeVals[ind-1][i%len(nodeVals[ind-1])]
    #print(negativeGradient)
    return negativeGradient
   










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
    
    alpha = 0.1

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


    print(layerCtStr)
    for i in range(len(allInputs)):
        allInputs[i].append(1) #putting bias of 1 
    weights = initialWeights
    bestError = 100000
    for epoch in range(1,20001):
        totalError = 0



        for ind, currInps in enumerate(allInputs):
            
            #do forward prop to get network
            #print(currInps)
            nodeVals = feedForward(currInps,weights,3)



            #the following chunk calculates error
            summDiffs = 0
            for i in realOutputs[ind]:
                for u in nodeVals[-1]:
                    summDiffs+= (i-u) *(i-u)
            summDiffs = summDiffs/2
            totalError +=summDiffs


            # print(nodeVals)
            # print(weights)
            #do backprop 
            negativeGradient = backProp(nodeVals,weights,3,realOutputs[ind])


            for i,layer in enumerate(negativeGradient):  #updating weights
                #print(layer)
                l = []
                for u,wt in enumerate(negativeGradient[i]):
                    #pass
                     l.append(weights[i][u]+ alpha * negativeGradient[i][u])
                weights[i] = l
          
                    #print(weights)
            #print(negativeGradient)
        if totalError> .099:
            initialWeights = []
            for i in range(len(nodeCts)-1):
                ct = nodeCts[i]
                numWts = ct * nodeCts[i+1]
                wts = []
                for n in range(numWts):
                    wts.append(random.random())
                initialWeights.append(wts)
            weights = initialWeights
        if totalError< bestError:
            bestError = totalError
            print(f"err: ",totalError)
            finStr = ""
            #print(weights)
            for layer in weights:
                finStr = ""
                for wt in layer:
                    finStr += str(wt) + " "
                print(finStr)
            print("\n")
        
        # if epoch%10000==0 :
        #     print(f"err: ",totalError)
        #     finStr = ""
        #     #print(weights)
        #     for layer in weights:
        #         finStr = ""
        #         for wt in layer:
        #             finStr += str(wt) + " "
        #         print(finStr)
        #     print("\n")



if __name__ == '__main__': main()


# Anmol Karan, pd 3, 2025            
