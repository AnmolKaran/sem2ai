import sys;  args = sys.argv[1:]
import math

def parseArgs():

    transferFunction = 0
    allInputs =  []
    linesOfFile = []


    for arg in args:
        if ".txt" in arg:
            linesOfFile = open(args[0]).read().splitlines()
        elif "T" in arg:
            transferFunction = int(arg[1])
        else:
            allInputs.append(float(arg))
    return linesOfFile,transferFunction,allInputs


def performTransferFunc(transferFunction,val):
    if transferFunction == 1:
        return val

    if transferFunction == 2:
        return val * (val>0)
    if transferFunction == 3:
        return 1/(1+math.exp(-val))
    if transferFunction == 4:
        return (1/(1+math.exp(-val)))* 2 -1



def calcNodes(inps, wts,transferFunction):
    numResultingNodes = int(len(wts)/len(inps))
    wtsIter = 0
    finNodes = []
    for n in range(numResultingNodes):
        dotProdded = dotProduct(inps, wts[:len(inps)])
        wts = wts[len(inps):]
        
        finNodes.append(dotProdded)
        

    for i, v in enumerate(finNodes):
        transferred = performTransferFunc(transferFunction,v)
        finNodes[i] = transferred
        
    return finNodes




def dotProduct(v1,v2):
    allProds = []
    for i, n in enumerate(v1):
        allProds.append(n*v2[i])
    return sum(allProds)



def main():
    linesOfFile, transferFunction,initialInputs = parseArgs()
    newLinesOfFile = [i.split(" ") for i in linesOfFile]
    linesOfFile = [[float(i) for i in l] for l in newLinesOfFile]

    wtLayers = linesOfFile
    inps = initialInputs
    for wtLayer in wtLayers[:-1]:
       
        nodes = calcNodes(inps,wtLayer,transferFunction)
        inps = nodes
    
    inps = [v * wtLayers[-1][i] for i, v in enumerate(inps)]



    finString = ' '.join([str(i) for i in inps])   
    print(inps)
    #print(finString)
    print(wtLayers)

if __name__ == '__main__': main()






# Anmol Karan, pd 3, 2025            
