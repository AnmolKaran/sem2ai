#Anmol Karan, pd 3, 2025
import sys;  args = sys.argv[1:]
import math
import random
import csv
import time



def elapsed_time():
    return time.time() - start_time

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
            #print(dotProdded)
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








def testNN(inps,outs,weights):
    totalError = 0
    correct = 0
    incorrect = 0

    for index, input in enumerate(inps):
    
        nodeVals = feedForward(input,weights,3)
        # print('output layer: ',nodeVals[-1])
        # print('nodeVals: ',nodeVals)
        # print()

        maxVal = 0
        maxInd = 0
        for i,v in enumerate(nodeVals[-1]):
            if v> maxVal:
                maxInd = i
                maxVal = v
        
        if maxInd == outs[index].index(1):correct += 1
        else: incorrect += 1
    return  correct/len(inps)
    



def main():
    global start_time 
    start_time= time.time()
    train_x = []
    train_y = []
    test_x = []
    test_y = []

    with open('NN/mnist_data/mnist_train.csv','r') as train_csv:
        reader = csv.reader(train_csv)
        randNums = random.sample(range(0,60000), 60000)
        for ind, row in enumerate(reader):
            if ind not in randNums:
                
                continue
            if ind == 0:
                continue
            
            row =[row[0]] + [float(i)/255 for iind, i in enumerate(row[1:])]
            
            train_x.append(row[1:])
            ySignals= [0 for i in range(10)]
            ySignals[int(row[0])] = 1
            train_y.append(ySignals)

            
            # print(train_y,train_x)
            # print("\n")
            # exit()
        # print(train_x)
        #print(train_y)
            





    with open('NN/mnist_data/mnist_test.csv','r') as test_csv:
        reader = csv.reader(test_csv)
        randNums = random.sample(range(0,10000), 9999)
        for ind, row in enumerate(reader):
            if ind not in randNums:continue
            if ind == 0:
                continue
            
            row =[row[0]] + [float(i)/255 for iind, i in enumerate(row[1:])]
            
            test_x.append(row[1:])
            ySignals= [0 for i in range(10)]
            ySignals[int(row[0])] = 1
            test_y.append(ySignals)

        
    alpha = 0.1
    nodeCts = [785,40,25,10,10]
    initialWeights = []
    for i in range(len(nodeCts)-2):
        ct = nodeCts[i]
        numWts = ct * nodeCts[i+1]
        wts = []
        for n in range(numWts):
            wts.append(random.random()-0.5)
        initialWeights.append(wts)
    
    outputLayerWeights = []
    for i in range(nodeCts[-2]):
        outputLayerWeights.append(random.random()-0.5)
    initialWeights.append(outputLayerWeights)
    layerCtStr = "Layer counts: "
    for i in nodeCts:
        layerCtStr+=str(i) + " "

    print(layerCtStr)

    for i in range(len(train_x)):
        train_x[i].append(1)
    for i in range(len(test_x)):
        test_x[i].append(1)

    weights = initialWeights
    bestError = 100000

    accuracies_every_5k = []
    for epoch in range(1,11):

        
        totalError = 0



        for ind, currInps in enumerate(train_x):
            
            if ind %1000 ==0:
                print("epoch: ", epoch)
                #print("weights: ", weights)
                print("datapoint: ",ind)  
                print() 
                #tested = testNNN(test_x,test_y,weights,5000,output_lookup_table)  
                
                
                
            #do forward prop to get network

            nodeVals = feedForward(currInps,weights,3)
            
            #do backprop 
            
            negativeGradient = backProp(nodeVals,weights,3,train_y[ind])
            
            

            for i,layer in enumerate(negativeGradient):  #updating weights
                #print(layer)
                l = []
                for u,wt in enumerate(negativeGradient[i]):
                    #pass
                     l.append(weights[i][u]+ alpha * negativeGradient[i][u])
                weights[i] = l
            if ind %5000 == 0:
                acc = testNN(test_x,test_y,weights)  
                accuracies_every_5k.append(acc)

        
        tested = accuracies_every_5k[-1] 
        print( "correct: ", tested)
        f = open("NN/mnist_weights.txt","w")
        f.writelines('\n'.join([' '.join([str(w) for w in weight]) for weight in weights]))
        f.close()
        print('elapsed time: ' + str(elapsed_time()))   
    with open('NN/accuracies_every_5k.txt', 'w') as file:
        for value in accuracies_every_5k:
            file.write(f"{value}\n")
    

if __name__ == '__main__': main()    


# Anmol Karan, pd 3, 2025            


