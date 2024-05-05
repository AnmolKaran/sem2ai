import sys;  args = sys.argv[1:]
import math
#graph- {vertex: [nbrs, width,reward]}


def grfParse(lstArgs):
    grfRwd = 0
    nonDefaultRwds = set()#vertices without default rewards but with same rwd value

    impliedRwd = 12
    graphStruct = {}
    gType = "G1" #G0 or G1
    for ind,arg in enumerate(lstArgs):

        if ind == 0:
       
            numVertices = int(arg)

            wid = -1


        
            if len(args) > 1 and args[ind+1].isnumeric():
                wid = int(args[ind+1])
            else:
                ht= 1
                for i in range(1,int(math.sqrt(numVertices))+1):
                    if i >ht and numVertices %i == 0:
                        ht = i
                wid = numVertices//ht

            theRange= [i for i in range(numVertices)]

            for i , ch in enumerate(theRange):
          
                    nbrSet = set()
                    if not i% wid == wid-1:
                        rightNbr = theRange[i+1]
                        nbrSet.add(int(rightNbr))

                    if not i % wid == 0:
                        leftNbr = theRange[i-1]
                        nbrSet.add(int(leftNbr))
                    if not i //wid == 0:
                        upNbr = theRange[i-wid]
                        nbrSet.add(int(upNbr))
                    if not i +wid >= len(theRange):
                        downNbr = theRange[i+wid]
                        nbrSet.add(int(downNbr))
                    graphStruct[i] = [nbrSet,wid,0]
        

        
            
        

        if arg.isnumeric():
            continue
        

        if arg[0].upper() == "R":
            afterR = arg[1:]
            splitted = afterR.split(":")
            finSplitted = []
            for i in splitted:
                if i:
                    finSplitted.append(i)
            splitted = finSplitted
            if afterR.isnumeric():
                cell= int(afterR)
                graphStruct[cell][2] = impliedRwd
                nonDefaultRwds.add(cell)
            
            elif len(splitted) ==2:
                
                cell = int(splitted[0])
                cellRwd = int(splitted[1])
                graphStruct[cell][2] = cellRwd
                nonDefaultRwds.add(cell)
            elif len(splitted) == 1:
                newRwd = int(afterR[1:])
                
                impliedRwd = newRwd


        if arg[0] == "B":
            width = graphStruct[0][1]
            afterB = arg[1:]
            if afterB.isnumeric():
                v = int(afterB)
                vertex = graphStruct[v]
                nbrs = vertex[0].copy()

            
                for otherVertex in graphStruct:
                    if (otherVertex == v -1 and v% width >0) or (otherVertex == v +1 and v% width <width-1)  or (otherVertex == v + width and v+width <=len(graphStruct)-1) or (otherVertex == v -width  and v- width >=0)   :

                        otherVertexOrigNeighbors = graphStruct[otherVertex][0].copy()

                        if otherVertex in nbrs:
                            graphStruct[v][0].remove(otherVertex)
                        else:
                            graphStruct[v][0].add(otherVertex)
                        if v in otherVertexOrigNeighbors:
                            graphStruct[otherVertex][0].remove(v)
                        else:
                            graphStruct[otherVertex][0].add(v)
                
            else:
                numberInd = 0
                for ind,ch in enumerate(afterB):
                    if ch not in "0123456789":
                        numberInd = ind
                        break
                v = int(afterB[:numberInd])
                dirs = afterB[numberInd:]
                allDirs = {*dirs} #myabe they are supposed to be repeated? idk
                for direction in allDirs:
                    inc = 0
                    if direction == "N":
                        inc = -width
                    if direction == "S":
                        inc = width
                    if direction == "E":
                        inc = 1
                    if direction == "W":
                        inc = -1

                    if v + inc >= 0 and v + inc <len(graphStruct) and abs(v% width - (v+inc) % width)<=1 :
                        otherV = v+ inc
                        otherVNbrs = graphStruct[otherV][0]
                        nbrs = graphStruct[v][0]


                        if otherV in nbrs:
                            graphStruct[v][0].remove(otherV)
                        else:
                            graphStruct[v][0].add(otherV)
                        if v in otherVNbrs:
                            graphStruct[otherV][0].remove(v)
                        else:
                            graphStruct[otherV][0].add(v)
        if arg[0] == "G":
            if arg[1] == "0":
                gType = "G0"
            else:
                gType = "G1"


    graphStruct["gType"] = gType
    graphStruct["nonDefaultRwds"] = nonDefaultRwds
    return graphStruct





def display2d(pzl,wid):
   startIndeces = [q for q in range(0,len(pzl),wid) ]
   listed = []
   for q in startIndeces:
       listPuzzle = list(pzl)
       theThing  = listPuzzle[q: q+wid]
       listed.append(''.join(theThing))
  


   for i in listed:
        print (i)




def checkIfRwd(graph,width,loc1,loc2):  #checks if doing a move gets to a reward
    if (loc1,loc2) in graph['nonDefaultRwds']:
        return True
    if loc2 in graph['nonDefaultRwds']:
        return True
    return False


def processDirs(lst):
    allJumps = {i for i in lst if isinstance(i,tuple)}
    currDirs = {i for i in lst if isinstance(i,str)}
    symbol = "."

    if {"up"}.issubset(currDirs):
        symbol = "U"
    if {"left"}.issubset(currDirs):
        symbol = "L"
    if {"right"}.issubset(currDirs):
        symbol = "R"
    if {"down"}.issubset(currDirs):
        symbol = "D"

    if {"up","down"}.issubset(currDirs):
        symbol = "|"
    if {"left","right"}.issubset(currDirs):
        symbol = "-"
    if {"up","right"}.issubset(currDirs):
        symbol = "V"
    if {"up","left"}.issubset(currDirs):
        symbol = "M"
    if {"down","left"}.issubset(currDirs):
        symbol = "E"
    if {"down","right"}.issubset(currDirs):
        symbol = "S"

    if {"up","right","down"}.issubset(currDirs):
        symbol = "W"
    if {"up","left","down"}.issubset(currDirs):
        symbol = "F"
    if {"right","left","down"}.issubset(currDirs):
        symbol = "T"
    if {"right","left","up"}.issubset(currDirs):
        symbol = "N"
    if {"right","left","up","down"}.issubset(currDirs):
        symbol = "+"
    return {'symbol': symbol,"jumps":allJumps}




def shortestPathToRwd(graph,width,loc, gType, prevLoc = None,steps = 0):
    global allDists
    if steps > len(graph)-2:
        return -1,None
    if prevLoc == None:
        if loc in graph['nonDefaultRwds']:
            return "*",None
    else:
        isRwd = checkIfRwd(graph,width,prevLoc,loc)

        if isRwd: 

            return steps, loc

    if prevLoc and prevLoc in graph[loc][0] and loc in graph[prevLoc][0] and (prevLoc,loc) in graph['nonDefaultRwds']:

        
        nbrs = graph[loc][0] 
    else:
        nbrs = graph[loc][0] #- {prevLoc}
        
    stepsToNbrToRwdloc = []
    if not nbrs:
        return -1,None
    for nbr in nbrs:     
        if (nbr, loc,steps+1)  not in allDists:
            # print(shortestPathToRwd(graph,width,nbr,loc,steps+1))
            # print("hi")
            path,rwdLoc = shortestPathToRwd(graph,width,nbr,gType,loc,steps+1)
            allDists[(nbr,loc,steps+1)] = (path,rwdLoc)
        else:
            path = allDists[(nbr,loc,steps+1)][0]
            rwdLoc = allDists[(nbr,loc,steps+1)][1]
        #path = shortestPathToRwd(graph,width,nbr,loc,steps+1)
        if not path == -1:

            stepsToNbrToRwdloc.append((path,nbr,rwdLoc))
    


    if not stepsToNbrToRwdloc:   #not a possible location
        return -1,None
    elif prevLoc == None:   #the original index that was called
        

        if gType == "G0":
            teststepsToNbrToRwdloc = stepsToNbrToRwdloc.copy()
            greatestRwd = 0
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]>greatestRwd:
                    greatestRwd = graph[value[2]][2]
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]< greatestRwd:
                    stepsToNbrToRwdloc.remove(value)

            stepsToNbrToRwdloc = sorted(stepsToNbrToRwdloc, key=lambda x: x[0], reverse=False)

            greatest_first_element = stepsToNbrToRwdloc[0][0]
            stepsToNbrToRwdloc = [tup for tup in stepsToNbrToRwdloc if tup[0] == greatest_first_element]
        else:
            teststepsToNbrToRwdloc = stepsToNbrToRwdloc.copy()
            greatestRwd = 0
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]/value[0]>greatestRwd:
                    greatestRwd = graph[value[2]][2]/value[0]
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]/value[0]< greatestRwd:
                    stepsToNbrToRwdloc.remove(value)

            stepsToNbrToRwdloc = sorted(stepsToNbrToRwdloc, key=lambda x: graph[x[2]][2]/x[0], reverse=False)
            rwdByDist = 0
            
            for x in stepsToNbrToRwdloc:
                rwdByDist = graph[x[2]][2]/x[0]
                break
                    

            
            #greatest_first_element = stepsToNbrToRwdloc[0][0]
            stepsToNbrToRwdloc = [tup for tup in stepsToNbrToRwdloc if graph[tup[2]][2]/tup[0] == rwdByDist]

        allDirs = []
        for i, v in enumerate(stepsToNbrToRwdloc):
            nbr = v[1]
            if nbr == loc-width:allDirs.append("up")
            elif nbr == loc+width: allDirs.append("down")
            elif nbr == loc+1 and loc%width != width-1: allDirs.append("right")
            elif nbr == loc -1 and loc%width != 0: allDirs.append("left")
            else:
                allDirs.append((loc,nbr))
        finThing = processDirs(allDirs)
        return finThing, loc
    else:   #return the minimum steps from the current location'
        
        if gType == "G0":
            teststepsToNbrToRwdloc = stepsToNbrToRwdloc.copy()
            greatestRwd = 0
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]>greatestRwd:
                    greatestRwd = graph[value[2]][2]
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]< greatestRwd:
                    stepsToNbrToRwdloc.remove(value)



            stepsToNbrToRwdloc = sorted(stepsToNbrToRwdloc, key=lambda x: x[0], reverse=False)
            
            greatest_first_element = stepsToNbrToRwdloc[0][0]
            stepsToNbrToRwdloc = [tup for tup in stepsToNbrToRwdloc if tup[0] == greatest_first_element]
            return stepsToNbrToRwdloc[0][0], stepsToNbrToRwdloc[0][2]
        else: 
            teststepsToNbrToRwdloc = stepsToNbrToRwdloc.copy()
            greatestRwd = 0
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]/value[0]>greatestRwd:
                    greatestRwd = graph[value[2]][2]/value[0]
            for i, value in enumerate(teststepsToNbrToRwdloc):
                if graph[value[2]][2]/value[0]< greatestRwd:
                    stepsToNbrToRwdloc.remove(value)

            stepsToNbrToRwdloc = sorted(stepsToNbrToRwdloc, key=lambda x: graph[x[2]][2]/x[0], reverse=False)

            greatest_first_element = stepsToNbrToRwdloc[0][0]
            for x in stepsToNbrToRwdloc:
                rwdByDist = graph[x[2]][2]/x[0]
                break
                    

            
            #greatest_first_element = stepsToNbrToRwdloc[0][0]
            stepsToNbrToRwdloc = [tup for tup in stepsToNbrToRwdloc if graph[tup[2]][2]/tup[0] == rwdByDist]
            #stepsToNbrToRwdloc = [tup for tup in stepsToNbrToRwdloc if tup[0] == greatest_first_element]
            return stepsToNbrToRwdloc[0][0], stepsToNbrToRwdloc[0][2]
            


def showAllRwds(graph,width,gType):

    finGraph = graph.copy()
    del finGraph["gType"]
    del finGraph['nonDefaultRwds']
    finStr = ""

    jumps = set()

    for vertex in finGraph:
        dirs,nth = shortestPathToRwd(graph,width,vertex,gType)
        if dirs == -1:
            finStr +="."
        elif dirs == "*":
            finStr +=dirs
        else:
            finStr+= dirs['symbol']
            jumps  = jumps.union(dirs['jumps'])
    final = finStr + "\n"

    jumpStr = ""
    for jump in jumps:
        jumpStr+= str(jump[0]) + ">"  + str(jump[1]) + ";"
    
    if jumpStr:
        jumpStr = jumpStr[:-1]
    
    return final,jumpStr




def main():
    global allDists
    allDists = {}
    graph = grfParse(args)
    wid = graph[0][1]
    
   
    gType = graph['gType']
    greatestRwdInd = (0,0)

    if gType == "G0":
        
        for v in graph:
            if not isinstance(v,int):
                continue
          
            if graph[v][2] > graph[greatestRwdInd[0]][2]:
                greatestRwdInd = (v,graph[v][2])
    # newNonDefs = graph['nonDefaultRwds'].copy()
    # oldNonDefs = graph['nonDefaultRwds']
    # for v in graph["nonDefaultRwds"]:
    #     if graph[v][2]< greatestRwdInd[1]:
    #         newNonDefs.remove(v)
    # graph['nonDefaultRwds'] = newNonDefs
    print(graph)
    strEdg,jumpStr = showAllRwds(graph,wid,gType)
    rest = ""
    # for i, ch in enumerate (strEdg):
    #     if i in oldNonDefs:
    #         strEdg = strEdg[:i]+ "*" + strEdg[i+1:]
    print("Policy: ")           
    display2d(strEdg,wid)
    print(jumpStr)

if __name__ == '__main__': main()
# Anmol Karan, pd 3, 2025            
                    

