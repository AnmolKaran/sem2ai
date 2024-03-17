import sys;  args = sys.argv[1:]
import math


def grfParse(lstArgs):
    
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
                rwd = int(followingText)

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

                for v in st:
                    vertex = graphStruct[v]

                    nbrs = vertex[0]
                    for otherVertex in graphStruct:
                        if otherVertex in st:
                            continue
                        otherVertexOrigNeighbors = graphStruct[otherVertex][0].copy()
                        if v not in otherVertexOrigNeighbors and (v+1) %width != 0 and otherVertex == v+1:
                            graphStruct[otherVertex][0].add(v)
                            graphStruct[v][0].add(otherVertex) 

                        if v not in otherVertexOrigNeighbors and v %width != 0 and otherVertex == v-1:
                            graphStruct[otherVertex][0].add(v)
                            
                            graphStruct[v][0].add(otherVertex) 

                        if v not in otherVertexOrigNeighbors and not v+width >= len(graphStruct) and otherVertex == v+width:
                            graphStruct[otherVertex][0].add(v)
                            graphStruct[v][0].add(otherVertex) 
                        
                        if v not in otherVertexOrigNeighbors and not v-width < 0 and otherVertex == v-width :
                            graphStruct[otherVertex][0].add(v)    
                            graphStruct[v][0].add(otherVertex)                
                            



                        if v in otherVertexOrigNeighbors:
                            
                            graphStruct[otherVertex][0].remove(v)
                            graphStruct[v][0].remove(otherVertex)

            if "R" in arg:
                reward = 0
                rInd = finArg.rfind("R") + 1
                if rInd >= len(arg) or finArg[rInd] not in "0123456789":
                    reward = 12
                    continue
                r = finArg[rInd]
                if rInd< len(finArg)-1:
                    if finArg[rInd+1] in "0123456789":
                        r +=finArg[rInd+1]
                        if rInd+1 < len(finArg)-1:
                            if finArg[rInd+2] in "0123456789":
                                r +=finArg[rInd+2]
                


                reward = int(r)




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



        if arg[0].upper() == "E":
            if arg[1] not in "!+*~@":
                finArg = finArg[0] + "~" + finArg[1:]
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
            

            res = []
            [res.append(x) for x in allEdges if x not in res]

            allEdges = res
            #if finArg[endOfVslc1] in "NSEW": # second form
            if finArg[1] == "~":
                if "=" in finArg[2:]:
                    for edge in allEdges:
                        first = edge[0]
                        second = edge[1]
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
                        if second not in graphStruct[first][0]:
                            graphStruct[first][0].add(second)
                        else:
                            graphStruct[first][0].remove(second)
                                        


    return graphStruct


def grfSize(graph):
    return len(graph)


def grfNbrs(graph,v):
    return graph[v][0]

def grfGProps(graph):
    if graph[0][1] == -1:
        prop = {'rwd':graph[0][2]}
    else:
        prop = {'rwd':graph[0][2],'width':graph[0][1]}


    return prop

def grfVProps(graph,v):
    return {}

def grfEProps(graph,v1,v2):
    return {}

def grfStrEdges(graph):
    finStr = ""
    for i in graph:
        val = graph[i]
        
        
        wid = val[1]
        nbrs = val[0]
        currDirs = set()
        symbol = "."
        for nbr in nbrs:
            if nbr == i-wid:
                currDirs.add("up")
            if nbr == i +wid:
                currDirs.add("down")
            if nbr == i+1:
                currDirs.add("right")
            if nbr == i-1:
                currDirs.add("left")
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
        return ""
    return finStr
    

        





def grfStrProps(graph):
    if graph[0][1] == -1:
        prop = {'rwd':graph[0][2]}
    else:
        prop = {'rwd':graph[0][2],'width':graph[0][1]}

    return str(prop)[1:-1].replace("'","")





def display2d(pzl,wid):
   startIndeces = [q for q in range(0,len(pzl),wid) ]
   listed = []
   for q in startIndeces:
       listPuzzle = list(pzl)
       theThing  = listPuzzle[q: q+wid]
       listed.append(''.join(theThing))
  


   for i in listed:
        print (i)



def main():
    graph = grfParse(args)
    wid = graph[0][1]
    if wid !=0:
        display2d(grfStrEdges(graph),wid)
    print(grfStrProps(graph))

if __name__ == '__main__': main()
# Anmol Karan, pd 3, 2025