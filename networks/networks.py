import sys;  args = sys.argv[1:]
import random


def setGlobals():
    global avgDeg
    global constructionType
    global nodeCt 
    global edgeCt
    avgDeg = float(args[0])
    constructionType = args[1].upper()
    nodeCt =int(args[2])
    edgeCt = avgDeg * nodeCt
def main():
    global avgDeg
    global constructionType
    global nodeCt 
    global edgeCt
    setGlobals()

    graphStruct = {n:[] for n in range(nodeCt)}
    if constructionType[0].lower() == "c":

        
        inc = 0
        while True:
            if inc >= edgeCt:
                break
            node1 = random.randint(0,nodeCt-1)
            node2 = random.randint(0,nodeCt-1)    
            if not node2 in graphStruct[node1]:
                inc = inc + 2
                graphStruct[node1].append(node2)
                graphStruct[node2].append(node1)
    #print(graphStruct)
    elif constructionType[0].lower() == "i":
        graphStruct = {}
        graphStruct[0] = []
        addedEdges = 0
        allNodeCounts = []
        for n in range(nodeCt -1):
            if n == 0:
                allNodeCounts.append(0)
            ind = n+1
            edgesRemaining = edgeCt - addedEdges
           

            avgNodes = (int(edgesRemaining/2)+1 if edgesRemaining%2 != 0 else int(edgesRemaining/2))/(nodeCt - len(graphStruct))


            if (int(edgesRemaining/2)+1 if edgesRemaining%2 != 0 else int(edgesRemaining/2))% (nodeCt - len(graphStruct)) != 0:
                #print(avgNodes)
                avgNodes= int(avgNodes)
                #print(avgNodes)
                avgNodes+=1
            

            if len(graphStruct) < avgNodes:
                avgNodes = len(graphStruct)
            avgNodes = int(avgNodes)
            #print(avgNodes)


            addingNodes = []
            graphStruct[ind]= []
            for i in range(avgNodes):
                # print(allNodeCounts)
                totalNodes = len(allNodeCounts)
                node = allNodeCounts[random.randint(0, totalNodes-1)]
                # if isinstance(node,list):
                #     print(allNodeCounts)
                #     print(node)
                #     exit()
                if node  in addingNodes:
                    while True:
                        # print("hi")
                        if not node in addingNodes:
                            addingNodes.append(node)
                            break
                        node = allNodeCounts[random.randint(0, totalNodes-1)]
                addingNodes.append(node)
            #print(addingNodes)
            for i in addingNodes:
                addedEdges+=2
                graphStruct[ind].append(i)
                graphStruct[i].append(ind)
                allNodeCounts.extend([ind,i])
                
                


            

        
    degreeToCt = {}
    for node in graphStruct:
        if len(graphStruct[node]) not in degreeToCt:
            degreeToCt[len(graphStruct[node])] = 1
        else:
            degreeToCt[len(graphStruct[node])] +=1
    
    finStr = ""
    for i in degreeToCt:
        finStr += str(i) + ':' + str(degreeToCt[i]) + " "

    print(finStr)

        




if __name__ == '__main__': main()

# Anmol Karan, pd 3, 2025            
