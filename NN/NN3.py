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
    #print(nodeVals)
    penultimateLayer = nodeVals[-1]
    inc = 0
    finalLayer = []
    for i in range(numNodesInNextLayer):
        #dotProdded = dotProduct(penultimateLayer, weights[-1][inc:inc + len(penultimateLayer)])
        finVal = penultimateLayer[i] * weights[-1][i]
        inc +=len(penultimateLayer)
        #finalLayer.append(dotProdded)
        finalLayer.append(finVal)
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
    for i in range(len(errorWRTy[-1])):

        errorWRTy[-1][i] = realOutput[i]-nodeVals[-1][i] #can change this for all nodes
        negativeGradient[-1][i]  = nodeVals[-2][i] *  (realOutput[i]-nodeVals[-1][i])

    # errorWRTy[-1][0] = realOutput[0]-nodeVals[-1][0]
    # negativeGradient[-1][0]  = nodeVals[-2][0] *  (realOutput[0]-nodeVals[-1][0])
    inc = 0

    for layer in range(len(errorWRTy)-2,0,-1):
 
        if inc == 0: # layer is the second to last layer
            for i in range(len(nodeVals[layer])):
                errorWRTy[layer][i] = errorWRTy[layer+1][i]*weights[layer][i] * transferDeriv(3,nodeVals[layer][i],True)



        else:
            for i in range(len(nodeVals[layer])):
                #wtsForDotProduct = [ind for ind ,v in enumerate(weights[layer]) if ind%len(errorWRTy[layer]) == i]

                dotProdded = dotProduct(errorWRTy[layer+1],weights[layer][i::len(nodeVals[layer])]) #otherwise maybe use slicing if wtsForDotProduct doesnt work
                #dotProdded = dotProduct(errorWRTy[layer+1],wtsForDotProduct)
                errorWRTy[layer][i] = dotProdded * transferDeriv(3,nodeVals[layer][i],True)
        inc +=1
    
    
   
    
    for ii, layer in enumerate(errorWRTy):
        if ii == 0 or ii == len(errorWRTy)-1:
            continue
        for i in range(len(negativeGradient[ii-1])):
            
            negativeGradient[ii-1][i] = errorWRTy[ii][i//len(nodeVals[ii-1])]* nodeVals[ii-1][i%len(nodeVals[ii-1])]
    #print(negativeGradient)

    return negativeGradient
   


def main():

    arg = args[0]
    sqrOfRadius = 0
    inequality = ""
    if "=" in arg:
        signIndex = arg.index("=")-1
        inequality = arg[signIndex] + "="
        sqrOfRadius = float(arg.split("=")[1])
    elif ">" in arg:
        inequality = ">"
        sqrOfRadius = float(arg.split(">")[1])
    elif "<" in arg:
        inequality = "<"
        sqrOfRadius = float(arg.split("<")[1])
    alpha = .1
    inps = []
    sampleCt = 5000

    realOutputs = []
    for n in range(sampleCt):
        x = (random.random()- 0.5) * 3
        y = (random.random()- 0.5) * 3
        inp = [x,y,1]
        realOutput = 0
        if inequality == ">=":
            if x**2+y**2 >= sqrOfRadius:
                realOutput = 1
            else:
                realOutput = 0
        if inequality == "<=":
            if x**2+y**2 <= sqrOfRadius:
                realOutput = 1
            else:
                realOutput = 0
        if inequality == ">":
            if x**2+y**2 > sqrOfRadius:
                realOutput = 1
            else:
                realOutput = 0
        if inequality == "<":
            if x**2+y**2 < sqrOfRadius:
                realOutput = 1
            else:
                realOutput = 0
        inps.append(inp)
        realOutputs.append([realOutput])


    numInputs = len(inps[0])


    nodeCts = [numInputs,5,4,1,1]

    initialWeights = []
    for i in range(len(nodeCts)-2):
        ct = nodeCts[i]
        numWts = ct * nodeCts[i+1]
        wts = []
        for n in range(numWts):
            wts.append(random.random())
        initialWeights.append(wts)


    outputLayerWeights = []
    for i in range(nodeCts[-2]):
        outputLayerWeights.append(random.random())
    initialWeights.append(outputLayerWeights)

    weights = initialWeights
    bestError = 100000
    allInputs = inps
    layerCtStr = "Layer counts: "
    for i,v  in enumerate(nodeCts):
        layerCtStr+=str(v) + " "
    
    
    print(layerCtStr)

    for epoch in range(1,1001):
        totalError = 0

        for ind, currInps in enumerate(inps):

            #do forward prop to get network
            #print(currInps)
            nodeVals = feedForward(currInps,weights,3)
            
            

            #the following chunk calculates error
            summDiffs = 0
            for p,i in enumerate(realOutputs[ind]):
                for q, u in enumerate(nodeVals[-1]):
                    if p == q:
                        # summDiffs+= (i-u) *(i-u) if ((i>.5 and u <.5) or  (i<.5 and u>.5)) else 0
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
        if (epoch+1)%10000==1 :
            if totalError>.099:
                initialWeights = []
                for i in range(len(nodeCts)-2):
                    ct = nodeCts[i]
                    numWts = ct * nodeCts[i+1]
                    wts = []
                    for n in range(numWts):
                        wts.append(random.random())
                    initialWeights.append(wts)


                outputLayerWeights = []
                for i in range(nodeCts[-2]):
                    outputLayerWeights.append(random.random())
                initialWeights.append(outputLayerWeights)
                weights = initialWeights




if __name__ == '__main__': main()

# Anmol Karan, pd 3, 2025            


