import sys;  args = sys.argv[1:]
import math




def grfParse(lstArgs):
    edgeProps = {}
    grfRwd = 0
    nonDefaultRwds = set()#vertices without default rewards but with same rwd value

    for arg in lstArgs:

       
        finArg = arg
        
        if arg[0].upper() == "G":
            rwd = 12
            graphStruct = {}

            numVertices = 0
            if arg[1].upper() not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                finArg = finArg[0] + "G" + finArg[1:]
            numVertices = finArg[2]
            if len(finArg)>3:
                if finArg[3] in "0123456789" and finArg[2] in "0123456789" :
                    numVertices +=finArg[3]
                if len(finArg)> 4:
                    if finArg[3] in "0123456789" and finArg[2] in "0123456789" and finArg[4] in  "0123456789":
                        numVertices+= finArg[4]
            numVertices = int(numVertices)
            wid = -1
            if "W" in finArg:
                
                if finArg[1] == "N":
                    wid = -1
                else:
                    wInd = finArg.index("W") + 1
                    wid = finArg[wInd]
                    if wInd< len(finArg)-1:
                        if finArg[wInd+1] in "0123456789":
                            wid +=finArg[wInd+1]
                    wid = int(wid)


            if "R" in finArg:
                followingText = finArg[finArg.find("R")+1:]
                if not followingText:
                    rwd = grfRwd
                    
                else:
                    rwd = int(followingText)
                grfRwd = rwd
            else:
                grfRwd = 12
                

            if wid == -1:
                if finArg[1] !="N":
                    ht= 1
                    for i in range(1,int(math.sqrt(numVertices))+1):
                        if i >ht and numVertices %i == 0:
                            ht = i
                    wid = numVertices//ht

                else:
                    wid = 0
            if finArg[1] == "G" and not(wid ==0):
                theRange =[i for i in range(numVertices)]
                for i , ch in enumerate(theRange):
          
                    nbrSet = set()

                    #if (m:= re.search(r"^G([NG])(\d+)(W\D+)?(R\D+)"),ARG)
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
                    graphStruct[i] = [nbrSet,wid,rwd]
            elif finArg[1] == "G" :
                theRange =[i for i in range(numVertices)]
                for i,ch in enumerate (theRange):
                    
                    graphStruct[int(i)] = [set(),0,rwd]
            else:
                theRange =[i for i in range(numVertices)]
                for i,ch in enumerate (theRange):
                    
                    graphStruct[int(i)] = [set(),-1,rwd]

        if arg[0].upper() == "V":
          
            setOfVertices = set()
            if "B" in arg:
                
                slc = ""

                width = graphStruct[0][1]
                for i in range(1, len(arg)):
                    if arg[i] in "0123456789-:,":
                        slc+=arg[i]
                    else:
                        break
                for splitted in slc.split(","):
                    sections = splitted.split(":")

    
                    if len(sections) ==1:
                        for i, v in enumerate(sections):
                            v = int(v)
                            if v <0:
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections[i] = v
                        ind = int(sections[0])
                        setOfVertices = setOfVertices.union({ind})

                    if len(sections) == 2:
                        if not sections[1]:
                            sections[1] = len(graphStruct)
                        
                        if not sections[0]:
                            sections[0] = 0
                        for i, v in enumerate(sections):
                            v = int(v)
                            if v <0:
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections[i] = v

                        setOfVertices = setOfVertices.union(set(range(sections[0],sections[1])))

                    if len(sections) == 3:
                        section1IsNone = False
                        if not sections[1]:
                            if sections[2] and int(sections[2]) <0:
                                sections[1] = -1
                                section1IsNone = True
                            else:
                                sections[1] = len(graphStruct)
                        if not sections[0]:
                            if sections[2] and int(sections[2]) <0:
                                sections[0] = len(graphStruct)-1
                            else:
                                sections[0] = 0

                        for i, v in enumerate(sections[:2]):
                            v = int(v)
                            if v <0  and not (i == 1 and section1IsNone):
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections[i] = v
                        if not sections[2]:
                            if int(sections[0]) > int(sections[1]):

                                sections[2] = -1
                            else:
                                sections[2] = 1
                        sections[2] = int(sections[2])
                        if sections[1] == None:
                            setOfVertices = setOfVertices.union(set(range(sections[0],-1,sections[2])))
                        setOfVertices = setOfVertices.union(set(range(sections[0],sections[1],sections[2])))

                st = setOfVertices
                #print("\n\n")
                for v in st:
                    vertex = graphStruct[v]
                    mustRemove = set()


                    nbrs = vertex[0].copy()
                    
                    #print(graphStruct[v][0])
                    for otherVertex in graphStruct:
                        # if otherVertex in st:
                            
                        #     continue
                        otherVertexOrigNeighbors = graphStruct[otherVertex][0].copy()
                 
                        #print(otherVertex,v)
                        if v not in otherVertexOrigNeighbors and (v+1) %width != 0 and otherVertex == v+1:

                            
                            graphStruct[otherVertex][0].add(v)
                            if otherVertex in graphStruct[v][0]:
                                graphStruct[v][0].remove(otherVertex)
                                if (v,otherVertex) in edgeProps:
                                    del edgeProps[(v,otherVertex)]
                            else:
                                graphStruct[v][0].add(otherVertex) 

                        if v not in otherVertexOrigNeighbors and v %width != 0 and otherVertex == v-1:
                            graphStruct[otherVertex][0].add(v)
                            
                            if otherVertex in graphStruct[v][0]:
                                if (v,otherVertex) in edgeProps:
                                    del edgeProps[(v,otherVertex)]
                                graphStruct[v][0].remove(otherVertex)
                            else:
                                graphStruct[v][0].add(otherVertex) 

                        if v not in otherVertexOrigNeighbors and not v+width >= len(graphStruct) and otherVertex == v+width:
                            graphStruct[otherVertex][0].add(v)
                            
                            if otherVertex in graphStruct[v][0]:
                                if (v,otherVertex) in edgeProps:
                                    del edgeProps[(v,otherVertex)]
                                graphStruct[v][0].remove(otherVertex)
                            else:
                                graphStruct[v][0].add(otherVertex) 
                        
                        if v not in otherVertexOrigNeighbors and not v-width < 0 and otherVertex == v-width :
                            graphStruct[otherVertex][0].add(v)
                            
                            if otherVertex in graphStruct[v][0]:
                                if (v,otherVertex) in edgeProps:
                                    del edgeProps[(v,otherVertex)]
                                graphStruct[v][0].remove(otherVertex)
                            else:
                                graphStruct[v][0].add(otherVertex)   
                            
                        
                        
                        if v in otherVertexOrigNeighbors:
                            
                            
                            graphStruct[otherVertex][0].remove(v)
                            if otherVertex not in graphStruct[v][0] and ((not v-width < 0 and otherVertex == v-width) or (not v+width >= len(graphStruct) and otherVertex == v+width )or ( v %width != 0 and otherVertex == v-1) or ((v+1) %width != 0 and otherVertex == v+1)):
                                graphStruct[v][0].add(otherVertex)
                            elif otherVertex in graphStruct[v][0]:
                                if (v,otherVertex) in edgeProps:
                                    del edgeProps[(v,otherVertex)]
                                graphStruct[v][0].remove(otherVertex)
                    #print(graphStruct[v][0],nbrs)
                    # for i in graphStruct[v][0]:
                    #     if i in nbrs:
                    #         mustRemove.add(i)

                    for i in nbrs:
                        if i in graphStruct[v][0]:
                           # mustRemove.add(i)
                            graphStruct[v][0].remove(i)
                            if (v,i) in edgeProps:
                                del edgeProps[(v,i)]
                            if v in graphStruct[i][0]:
                                if (i,v) in edgeProps:
                                    del edgeProps[(i,v)]
                                graphStruct[i][0].remove(v)
                    #graphStruct[v][0] -=mustRemove
                   
            allNonDefRwds = False
            if "R" in arg:
                reward = 0
                rInd = finArg.rfind("R") + 1
                if rInd >= len(arg) or finArg[rInd] not in "0123456789":
                    reward = grfRwd
                    
                    allNonDefRwds = True
                if allNonDefRwds == False:
                    r = finArg[rInd]
                    if rInd< len(finArg)-1:
                        if finArg[rInd+1] in "0123456789":
                            r +=finArg[rInd+1]
                            if rInd+1 < len(finArg)-1:
                                if finArg[rInd+2] in "0123456789":
                                    r +=finArg[rInd+2]
                    


                    reward = int(r)
                allNonDefRwds = True #toggle


                slc = ""

                width = graphStruct[0][1]
                for i in range(1, len(arg)):
                    if arg[i] in "0123456789-:,":


                        slc+=arg[i]
                    else:
                        break
                for splitted in slc.split(","):
                    sections = splitted.split(":")

    
                    if len(sections) ==1:
                        for i, v in enumerate(sections):
                            v = int(v)
                            if v <0:
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections[i] = v
                        ind = int(sections[0])
                        setOfVertices = setOfVertices.union({ind})

                    if len(sections) == 2:
                        if not sections[1]:
                            sections[1] = len(graphStruct)
                        
                        if not sections[0]:
                            sections[0] = 0
                        for i, v in enumerate(sections):
                            v = int(v)
                            if v <0:
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections[i] = v

                        setOfVertices = setOfVertices.union(set(range(sections[0],sections[1])))

                    if len(sections) == 3:
                        section1IsNone = False
                        if not sections[1]:
                            if sections[2] and int(sections[2]) <0:
                                sections[1] = -1
                                section1IsNone = True
                            else:
                                sections[1] = len(graphStruct)
                        if not sections[0]:
                            if sections[2] and int(sections[2]) <0:
                                sections[0] = len(graphStruct)-1
                            else:
                                sections[0] = 0

                        for i, v in enumerate(sections[:2]):
                            v = int(v)
                            if v <0  and not (i == 1 and section1IsNone):
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections[i] = v
                        if not sections[2]:
                            if int(sections[0]) > int(sections[1]):

                                sections[2] = -1
                            else:
                                sections[2] = 1
                        sections[2] = int(sections[2])
                        if sections[1] == None:
                            setOfVertices = setOfVertices.union(set(range(sections[0],-1,sections[2])))
                        setOfVertices = setOfVertices.union(set(range(sections[0],sections[1],sections[2])))

                st = setOfVertices
                for v in setOfVertices:
                    graphStruct[v][2] = reward
                    if allNonDefRwds:
                        nonDefaultRwds.add(v)


        if arg[0].upper() == "E":
            if arg[1] == "+" and arg[2] == "~":
                finArg = arg[0] + "%" + arg[3:]
            if arg[1] not in "+~":
                finArg = finArg[0] + "_" + finArg[1:]
            setOfVertices = []
            slc = ""

            width = graphStruct[0][1]
            endOfVslc1 = 0
            for i in range(2, len(finArg)):
                if finArg[i] in "0123456789-:,":
                    slc+=finArg[i]
                else:
                    endOfVslc1 = i
                    break
            for splitted in slc.split(","): #making set of vertices for vslc 1




                sections = splitted.split(":")

                if len(sections) ==1:
                    for i, v in enumerate(sections):
                        v = int(v)
                        if v <0:
                            v = v*-1
                            
                            v = len(graphStruct)-v
                        sections[i] = v
                    ind = int(sections[0])
                    setOfVertices = setOfVertices + [ind]

                if len(sections) == 2:
                    if not sections[1]:
                        sections[1] = len(graphStruct)
                    
                    if not sections[0]:
                        sections[0] = 0
                    for i, v in enumerate(sections):
                        v = int(v)
                        if v <0:
                            v = v*-1
                            
                            v = len(graphStruct)-v
                        sections[i] = v

                    setOfVertices = setOfVertices + list(range(sections[0],sections[1]))

                if len(sections) == 3:
                    section1IsNone = False
                    if not sections[1]:
                        if sections[2] and int(sections[2]) <0:
                            sections[1] = -1
                            section1IsNone = True
                        else:
                            sections[1] = len(graphStruct)
                    if not sections[0]:
                        if sections[2] and int(sections[2]) <0:
                            sections[0] = len(graphStruct)-1
                        else:
                            sections[0] = 0

                    for i, v in enumerate(sections[:2]):
                        v = int(v)
                        if v <0  and not (i == 1 and section1IsNone):
                            v = v*-1
                            
                            v = len(graphStruct)-v
                        sections[i] = v
                    if not sections[2]:
                        if int(sections[0]) > int(sections[1]):

                            sections[2] = -1
                        else:
                            sections[2] = 1
                    sections[2] = int(sections[2])
                    if sections[1] == None:
                        setOfVertices = setOfVertices + list((range(sections[0],-1,sections[2])))
                    setOfVertices = setOfVertices+ list(range(sections[0],sections[1],sections[2]))
                
            allEdges = []
            if finArg[endOfVslc1] in "~=": #form 1
                slc2 = ""
                for i in range(endOfVslc1+1, len(finArg)):
                    if finArg[i] in "0123456789-:,":
                        slc2+=finArg[i]
                    else:
                        break
                
                setOfVertices2 = []
                for splitted2 in slc2.split(","): #making set of vertices (setOfVertices2 )for vslc 2



                    sections2 = splitted2.split(":")


                    if len(sections2) ==1:
                        for i, v in enumerate(sections2):
                            v = int(v)
                            if v <0:
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections2[i] = v
                        ind = int(sections2[0])
                        setOfVertices2 = setOfVertices2 + [ind]

                    if len(sections2) == 2:
                        if not sections2[1]:
                            sections2[1] = len(graphStruct)
                        
                        if not sections2[0]:
                            sections2[0] = 0
                        for i, v in enumerate(sections2):
                            v = int(v)
                            if v <0:
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections2[i] = v

                        setOfVertices2 = setOfVertices2 + list(range(sections2[0],sections2[1]))

                    if len(sections2) == 3:
                        section1IsNone = False
                        if not sections2[1]:
                            if sections2[2] and int(sections2[2]) <0:
                                sections2[1] = -1
                                section1IsNone = True
                            else:
                                sections2[1] = len(graphStruct)
                        if not sections2[0]:
                            if sections2[2] and int(sections2[2]) <0:
                                sections2[0] = len(graphStruct)-1
                            else:
                                sections2[0] = 0

                        for i, v in enumerate(sections2[:2]):
                            v = int(v)
                            if v <0  and not (i == 1 and section1IsNone):
                                v = v*-1
                                
                                v = len(graphStruct)-v
                            sections2[i] = v
                        if not sections2[2]:
                            if int(sections2[0]) > int(sections2[1]):

                                sections2[2] = -1
                            else:
                                sections2[2] = 1
                        sections2[2] = int(sections2[2])
                        if sections2[1] == None:
                            setOfVertices2 = setOfVertices2 + list(range(sections2[0],-1,sections2[2]))
                        setOfVertices2 = setOfVertices2 + list((range(sections2[0],sections2[1],sections2[2])))
                
                allEdges = list(zip(setOfVertices,setOfVertices2))
            elif finArg[endOfVslc1] in "NSEW":
                allEdges = []
                allDirs = ""
                if "~" in finArg[endOfVslc1:]:
                    allDirs = finArg[endOfVslc1:][:finArg[endOfVslc1:].index("~")]
                if "=" in finArg[endOfVslc1:]:
                    allDirs = finArg[endOfVslc1:][:finArg[endOfVslc1:].index("=")]
                for ind, ver in enumerate(setOfVertices):
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
                    
                        if ver + inc >= 0 and ver + inc <len(graphStruct) and abs(ver% width - (ver+inc) % width)<=1 :
                            otherV = ver+inc
                            if "=" in finArg[endOfVslc1:]:
                                allEdges.append((ver,otherV))
                                allEdges.append((otherV,ver))
                            elif "~" in finArg[endOfVslc1:]:
                                allEdges.append((ver,otherV))


     
            res = []
            [res.append(x) for x in allEdges if x not in res]

            allEdges = res
            allNonDefRwds = False

            if "R" in finArg:
                allNonDefRwds = True        
                followingText = finArg[finArg.find("R")+1:]
                if not followingText:
                    allNonDefRwds = True
                    rwd = grfRwd
                else:
                    rwd = int(followingText)
            else:
                rwd = -1


            if finArg[1] == "+":
                
                oldGraph = graphStruct.copy()

                #do stuff
                if "=" in finArg[2:]:
                    
                    v = []
                    r = [sorted(u) for u in allEdges]
                    [v.append(x) for x in r if x not in v]
                    allEdges =v
                    for edge in allEdges:

                        first = edge[0]
                        second = edge[1]
                        if first == second:
                            if first not in graphStruct[first][0]:
                                graphStruct[first][0].add(first)
                           
                            continue
                  
                        if second not in graphStruct[first][0]:
                 
                            graphStruct[first][0].add(second)
             
                       
                        if first not in graphStruct[second][0]:
                            graphStruct[second][0].add(first)
                elif "~" in finArg[2:]:
                    for edge in allEdges:
                        first = edge[0]
                        second = edge[1]
                        # print(graphStruct[first],edge)
                        if second not in graphStruct[first][0]:
                            graphStruct[first][0].add(second)
                            # print(graphStruct[first],edge)
                        
                

                if "=" in finArg[2:]:
                    
                    v = []
                    r = [u for u in allEdges]
                    [v.append((x[1],x[0])) for x in r if x not in v]
                    allEdges += v

                for e in allEdges:
                    
                    if e[1] in oldGraph[e[0]][0]:
                        continue
                    if rwd !=-1:
                        edgeProps[tuple(e)] = {'rwd':rwd}
                    if allNonDefRwds:
                        nonDefaultRwds.add(tuple(e))


            if finArg[1] == "~":
                if "=" in finArg[2:]:
                    
                    v = []
                    r = [sorted(u) for u in allEdges]
                    [v.append(x) for x in r if x not in v]
                    allEdges =v
                    for edge in allEdges:
                        first = edge[0]
                        second = edge[1]
                        if (first,second) in edgeProps:
                            del edgeProps[(first,second)]
                            #edgeProps.remove((first,second))
                        if (first,second) in nonDefaultRwds:
                            nonDefaultRwds.remove((first,second))
                            
                        if first == second:
                            if first not in graphStruct[first][0]:
                                #graphStruct[first][0].add(first)
                                pass
                            else:
                                
                                graphStruct[first][0].remove(first)
                            continue
                  
                        if second not in graphStruct[first][0]:
                 
                            #graphStruct[first][0].add(second)
                            pass
             
                        else:
                            graphStruct[first][0].remove(second)
                        if first not in graphStruct[second][0]:
                            #graphStruct[second][0].add(first)
                            pass
                        else:
                            graphStruct[second][0].remove(first)
                elif "~" in finArg[2:]:
                    for edge in allEdges:
                        first = edge[0]
                        second = edge[1]
                        # print(graphStruct[first],edge)
                        if second not in graphStruct[first][0]:
                            #graphStruct[first][0].add(second)
                            pass
                            # print(graphStruct[first],edge)
                        else:
                            
                            graphStruct[first][0].remove(second)
                
            if finArg[1] == "%": #same as +~
                extantEdges = set()
                for i in graphStruct:
                    for ii in graphStruct[i][0]:
                        extantEdges.add((i,ii))
                if "=" in finArg[2:]:
                    
                    v = []
                    r = [u for u in allEdges]
                    [v.append((x[1],x[0])) for x in r if x not in v]
                    allEdges += v

                for e in allEdges:
                    if rwd !=-1 and tuple(e) in extantEdges:
                        edgeProps[tuple(e)] = {'rwd':rwd}
                        if allNonDefRwds:
                            nonDefaultRwds.add(tuple(e))   
            if finArg[1] == "_":  #toggle
                if "=" in finArg[2:]:
                    
                    v = []
                    r = [sorted(u) for u in allEdges]
                    [v.append(x) for x in r if x not in v]
                    allEdges =v
                    for edge in allEdges:
                        first = edge[0]
                        second = edge[1]
                        if first == second:
                            if first not in graphStruct[first][0]:
                                graphStruct[first][0].add(first)
                            else:
                                graphStruct[first][0].remove(first)
                            continue
                  
                        if second not in graphStruct[first][0]:
                 
                            graphStruct[first][0].add(second)
             
                        else:
                            graphStruct[first][0].remove(second)
                        if first not in graphStruct[second][0]:
                            graphStruct[second][0].add(first)
                        else:
                            graphStruct[second][0].remove(first)
                        
                elif "~" in finArg[2:]:
                    for edge in allEdges:
                        first = edge[0]
                        second = edge[1]
                        # print(graphStruct[first],edge)
                        if second not in graphStruct[first][0]:
                            graphStruct[first][0].add(second)
                            # print(graphStruct[first],edge)
                        else:
                            graphStruct[first][0].remove(second)
                
                if "=" in finArg[2:]:
                    
                    v = []
                    r = [u for u in allEdges]
                    [v.append((x[1],x[0])) for x in r if x not in v]
                    allEdges += v
                for e in allEdges:
                    if rwd !=-1:
                        edgeProps[tuple(e)] = {'rwd':rwd}
                    if allNonDefRwds:
                        nonDefaultRwds.add(tuple(e))
                            
    graphStruct['grfRwd'] = grfRwd
    graphStruct['edgeProps'] = edgeProps
    graphStruct['nonDefaultRwds'] = nonDefaultRwds
    print(graphStruct)
    return graphStruct
                


def grfStrEdges(graph):
    finStr = ""
    jumps = []
    finGraph = graph.copy()
    del finGraph['edgeProps']
    del finGraph['grfRwd']
    del finGraph['nonDefaultRwds']
    for i in finGraph:
        val = finGraph[i]
        
        
        wid = val[1]
        nbrs = val[0]
        currDirs = set()
        
        symbol = "."
        for nbr in nbrs:
            
            if nbr == i-wid and nbr%wid == i %wid:
                currDirs.add("up")
            elif nbr == i +wid and nbr%wid == i %wid:
                currDirs.add("down")
            elif nbr == i+1 and nbr //wid == i//wid:
                currDirs.add("right")
            elif nbr == i-1 and nbr //wid == i//wid:
                currDirs.add("left")
            else:
                jumps.append((i,nbr))

        if {"up"}.issubset(currDirs):
            symbol = "N"
        if {"left"}.issubset(currDirs):
            symbol = "W"
        if {"right"}.issubset(currDirs):
            symbol = "E"
        if {"down"}.issubset(currDirs):
            symbol = "S"

        if {"up","down"}.issubset(currDirs):
            symbol = "|"
        if {"left","right"}.issubset(currDirs):
            symbol = "-"
        if {"up","right"}.issubset(currDirs):
            symbol = "L"
        if {"up","left"}.issubset(currDirs):
            symbol = "J"
        if {"down","left"}.issubset(currDirs):
            symbol = "7"
        if {"down","right"}.issubset(currDirs):
            symbol = "r"

        if {"up","right","down"}.issubset(currDirs):
            symbol = ">"
        if {"up","left","down"}.issubset(currDirs):
            symbol = "<"
        if {"right","left","down"}.issubset(currDirs):
            symbol = "v"
        if {"right","left","up"}.issubset(currDirs):
            symbol = "^"
        if {"right","left","up","down"}.issubset(currDirs):
            symbol = "+"

        
        finStr +=symbol
    if finStr.count(".") == len(finStr):
        finStr = ""

    jumpStr= ""
    if jumps:

        sortedJumps = [sorted(i)  for i in jumps]
        jumpStr += "Jumps: "

        for index, i in enumerate(jumps):
            if sortedJumps.count(i) >1:
                if sortedJumps.index(i) !=index:
                    continue
                else:
                    
                    jumpStr =  jumpStr + str(i[0]) + "=" + str(i[1]) + ";"

            else:
                jumpStr =  jumpStr + str(i[0]) + "~" + str(i[1]) + ";"
        jumpStr =jumpStr[:-1]
    fin = finStr + "\n" +jumpStr
    return fin
    

        


    

def display2d(pzl,wid):
   startIndeces = [q for q in range(0,len(pzl),wid) ]
   listed = []
   for q in startIndeces:
       listPuzzle = list(pzl)
       theThing  = listPuzzle[q: q+wid]
       listed.append(''.join(theThing))
  


   for i in listed:
        print (i)





def grfStrProps(graph):
    rwd = graph['grfRwd']
    if graph[0][1] == -1:
        prop = {'rwd':rwd}
    else:
        prop = {'rwd':rwd,'width':graph[0][1]}
    
    fin = str(prop)[1:-1].replace("'","")

    for key in graph:
        if key == "grfRwd" or key == "edgeProps" or key == "nonDefaultRwds":
            continue
        
        if graph[key][2] != graph['grfRwd'] or key in graph['nonDefaultRwds']:
            fin = fin + "\n" + str(key)+ ":rwd:" + str(graph[key][2])
    width = graph[0][1]
    for key in graph:
        for otherKey in graph:
            if (key,otherKey) in graph['edgeProps'] and otherKey in graph[key][0] :#and abs(otherKey-key) != width and abs(otherKey-key)!=1:
                fin = fin + "\n" + str((key,otherKey)) + ":rwd:" + str(graph['edgeProps'][(key,otherKey)]['rwd'])
    return fin


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
        symbol = "N"
    if {"left"}.issubset(currDirs):
        symbol = "W"
    if {"right"}.issubset(currDirs):
        symbol = "E"
    if {"down"}.issubset(currDirs):
        symbol = "S"

    if {"up","down"}.issubset(currDirs):
        symbol = "|"
    if {"left","right"}.issubset(currDirs):
        symbol = "-"
    if {"up","right"}.issubset(currDirs):
        symbol = "L"
    if {"up","left"}.issubset(currDirs):
        symbol = "J"
    if {"down","left"}.issubset(currDirs):
        symbol = "7"
    if {"down","right"}.issubset(currDirs):
        symbol = "r"

    if {"up","right","down"}.issubset(currDirs):
        symbol = ">"
    if {"up","left","down"}.issubset(currDirs):
        symbol = "<"
    if {"right","left","down"}.issubset(currDirs):
        symbol = "v"
    if {"right","left","up"}.issubset(currDirs):
        symbol = "^"
    if {"right","left","up","down"}.issubset(currDirs):
        symbol = "+"
    return {'symbol': symbol,"jumps":allJumps}

def shortestPathToRwd(graph,width,loc,prevLoc = None,steps = 0):
    global allDists
    if steps > len(graph)-3:
        return -1
    if prevLoc == None:
        if loc in graph['nonDefaultRwds']:
            return "*"
    else:
        isRwd = checkIfRwd(graph,width,prevLoc,loc)

        if isRwd: 

            return steps

    if prevLoc and prevLoc in graph[loc][0] and loc in graph[prevLoc][0] and (prevLoc,loc) in graph['nonDefaultRwds']:

        
        nbrs = graph[loc][0] 
    else:
        nbrs = graph[loc][0] #- {prevLoc}
        
    stepsToNbr = []
    if not nbrs:
        return -1
    for nbr in nbrs:     
        if (nbr, loc,steps+1)  not in allDists:
            path = shortestPathToRwd(graph,width,nbr,loc,steps+1)
            allDists[(nbr,loc,steps+1)] = path
        else:
            path = allDists[(nbr,loc,steps+1)]
        #path = shortestPathToRwd(graph,width,nbr,loc,steps+1)
        if not path == -1:

            stepsToNbr.append((path,nbr))
    


    if not stepsToNbr:   #not a possible location
        return -1
    elif prevLoc == None:   #the original index that was called
        stepsToNbr = sorted(stepsToNbr, key=lambda x: x[0], reverse=False)
        greatest_first_element = stepsToNbr[0][0]
        stepsToNbr = [tup for tup in stepsToNbr if tup[0] == greatest_first_element]

        allDirs = []
        for i, v in enumerate(stepsToNbr):
            nbr = v[1]
            if nbr == loc-width:allDirs.append("up")
            elif nbr == loc+width: allDirs.append("down")
            elif nbr == loc+1 and loc%width != width-1: allDirs.append("right")
            elif nbr == loc -1 and loc%width != 0: allDirs.append("left")
            else:
                allDirs.append((loc,nbr))
        finThing = processDirs(allDirs)
        return finThing
    else:   #return the minimum steps from the current location
        stepsToNbr = sorted(stepsToNbr, key=lambda x: x[0], reverse=False)
        greatest_first_element = stepsToNbr[0][0]
        stepsToNbr = [tup for tup in stepsToNbr if tup[0] == greatest_first_element]
        return stepsToNbr[0][0]
    




    

        


    

    #only go back if there is a rwd edge to the prev loc

    

    #return [(distance,dir)]


def showAllRwds(graph,width):

    finGraph = graph.copy()
    del finGraph['edgeProps']
    del finGraph['grfRwd']
    del finGraph['nonDefaultRwds']
    finStr = ""

    jumps = set()

    for vertex in finGraph:
        dirs = shortestPathToRwd(graph,width,vertex)
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
    # if wid !=0:
    #     strEdg = grfStrEdges(graph)
    #     rest = ""
    #     if "Jumps" in strEdg:
    #         rest = strEdg[strEdg.rfind("J"):]
    #         strEdg = strEdg[:strEdg.rfind("J")]
            
    #     display2d(strEdg,wid)
    #     if rest:
    #      print(rest)


    #print(grfStrProps(graph))
    # print()
    #print("grfStrEdges: " ,grfStrEdges(graph))
    # print()

    #print("final graph: ",graph)

    #print()
    if wid !=0:
        strEdg,jumpStr = showAllRwds(graph,wid)
        rest = ""

        print("Policy: ")           
        display2d(strEdg,wid)
        print(jumpStr)

if __name__ == '__main__': main()
# Anmol Karan, pd 3, 2025