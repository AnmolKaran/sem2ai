import sys; args = sys.argv[1:]
import time


def parseArgs(argList):
    for i, arg in enumerate(argList):

        if ("x" in arg or "X" in arg) and not (arg[0].upper() in "VH") and  ".txt" not in arg:
            splitted = arg.lower().split("x")  
            global height
            global width 
            height = int(splitted[0])
            width = int(splitted[1])
        elif all([i in "0123456789" for i in arg]) and  ".txt" not in arg:
            global numBlocks
            numBlocks = int(arg)
        elif ("x" in arg or "X" in arg) and  ".txt" not in arg:
            global seedStrings
            seedStrings.append(arg)
        elif "txt" in arg:  
            global lengthToWords
            linesOfFile = open(args[0]).read().splitlines()
            for line in linesOfFile:
                lengthToWords[len(line)].append(line.lower())



def finDict():
    global bigDict

    linesOfFile = open(args[0]).read().splitlines()
    for line in linesOfFile:
        length = len(line)
        if length<3:continue
        for ind,char in enumerate(line):
            if not bigDict[(ind,char,length)]:
                bigDict[(ind,char,length)] == set()
            bigDict[(ind,char,length)].add(line)
    







def setGlobals():
    global height
    global width 
    global numBlocks
    global seedStrings
    global alphabetString
    global inputtedBlocks
    global words
    global lengthToWords
    global specsToPoss

    alphabetString = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    height = 0
    width = 0
    numBlocks = 0
    seedStrings = []
    inputtedBlocks = 0
    lengthToWords = {i+1:[] for i in range(50)}
    locationsToFill = []
    specsToPoss = {}


def elapsed_time():
    return time.time() - start_time
    

def display2d(pzl,wid):
   startIndeces = [q for q in range(0,len(pzl),wid) ]
   listed = []
   for q in startIndeces:
       listPuzzle = list(pzl)
       theThing  = listPuzzle[q: q+wid]
       listed.append(''.join(theThing))
  


   if len(listed) ==0:
       print("No solution found")
   else:
       for i in listed:
           print (i)


def placeWord(board, seedStr,wid):
    global inputtedBlocks
    dimStr = ""
    word = ""
    direction = seedStr[0]
    for ind, ch in enumerate(seedStr):
        if ind == 0:
            continue
        if ch not in "0123456789":
            if ind == len(seedStr)-1 or seedStr[ind+1] not in "0123456789":
                word = seedStr[ind:]
                break
        dimStr += ch
    splitted = dimStr.split("x")
    yCoord = int(splitted[0])
    xCoord = int(splitted[1])
    startingInd = yCoord * wid + xCoord
    direction = direction.upper()
    if direction == "H":
        wordIncrement = 0
        if not word:
            word = "#"
        for i in range(startingInd,startingInd+ len(word)):
            if not (board[i] == "#" and word[wordIncrement] in alphabetString )and not (i%width == width-1 and wordIncrement <  len(word)-1):
                if word[wordIncrement] == "#":
                    # if i == 97:
                    #     print(seedStr)
                    #     display2d(board,width)
                    prevNumBlocks = board.count("#")
                    board = placeBlock(board,i,width,height,False,True)
                    #display2d(board,wid)
                    #inputtedBlocks+= board.count("#") - prevNumBlocks
                    wordIncrement+=1
                    # if i == 97:
                    #     display2d(board,width)
                    #     exit()
                else:
                    board= board[:i] + word[wordIncrement] + board[i+1:]
                    wordIncrement+=1
            else:

                return 0
        return board
    if direction == "V":
        wordIncrement = 0
        if not word:
            word = "#"
        for i in range(startingInd,len(board),width):
            
            if not (board[i] == "#" and word[wordIncrement] in alphabetString ):
                if word[wordIncrement] == "#":
                #     if i == 97:
                        
                #         display2d(board,width)
                    prevNumBlocks = board.count("#")
                    board = placeBlock(board,i,width,height,False,True)
                    #display2d(board,wid)
                    #inputtedBlocks+= board.count("#") - prevNumBlocks
                    wordIncrement+=1
                    # if i == 97:
                    #     display2d(board,width)
                    #     exit()
                else:
                    board= board[:i] + word[wordIncrement] + board[i+1:]
                    wordIncrement+=1
                if wordIncrement >= len(word):
                    return board
            else:
                return 0
        if wordIncrement !=  len(word)-1 : #the word hasnt fully even been spelled out
            return -1

        return board




def CCWRotate(brd,wid):

    finString = ""
    for colStart in range(wid-1,-1,-1):
        rs = brd[colStart:len(brd):wid]
        finString+=rs

    return finString




def decushionize(brd, origWid,origHeight):
    #newBrd = brd[origWid+2:]
    newBrd = ""

    for i in range(origHeight):
        line = brd[(i+1)*(origWid+2) + 1 :(i+1)*(origWid+2) + 1 + origWid]
        newBrd = newBrd + line
    return newBrd



def placeBlock(brd,spot,wid,ht, reversed = False,inInitial = False,alreadyCushioned = False):   #checks if a block can be placed in the spot. reversed means like am i nw placing the blocks after the 180 rotation

    cushionedBoard = "#"* wid + "##"
    for i in range(ht):
        cushionedBoard+="#" 
        cushionedBoard += brd[i*wid:i*wid+wid]
        cushionedBoard+="#"
    cushionedBoard += "#"* wid + "##"

    if alreadyCushioned == False:
        yCoord = spot //wid
        xCoord = spot%wid 
        cushionedIndex =   wid+2 + (yCoord * (wid+2)) + 1 + xCoord
    else:
        cushionedIndex = spot


    newlyAddedBlocks = [cushionedIndex]
    blockInOneOfThem = False

    #display2d(cushionedBoard,wid+2)
    # print(corners)
    # exit()
    
    while newlyAddedBlocks:
        # display2d(cushionedBoard,wid+2)
        #print(newlyAddedBlocks)
        blk = newlyAddedBlocks.pop(0)
        
        #print(spot)
        #exit()
        yCoordOfBlk = blk //(wid+2) -1
        if cushionedBoard[blk] not in  "-#":

            return 0
        # if cushionedBoard[blk] == "#":
        #     #display2d(cushionedBoard,wid+2)
        #     #make sure to decushionize the board
        #     return cushionedBoard
        

        viewRight = cushionedBoard[blk:blk+4] #rightwards
        
        if "#" in viewRight[1:]:

          
            if cushionedBoard[blk] in alphabetString:
                return 0 
                
            
            #print("viewing right", blk)
            #print('this shouldnt happen')
            blockInOneOfThem = True
            otherBlkIndex = viewRight[1:].index("#") + 1
            if otherBlkIndex != 1:
                if any([True for letter in viewRight[0:otherBlkIndex] if letter in alphabetString]):
                    return 0
                newView = viewRight
                for l in range(0,otherBlkIndex):
                    newView= newView[:l] + "#" + newView[l+1:]
                    if l !=0:
                        newlyAddedBlocks.append(cushionedIndex + l)
                #print(newlyAddedBlocks)
                ctr = 0
                for i in range(blk,blk+4):
                    cushionedBoard = cushionedBoard[:blk + ctr] + newView[ctr] + cushionedBoard[blk +ctr+1:]
                    ctr+=1

        viewLeft = cushionedBoard[blk:blk-4:-1]
        if "#" in viewLeft[1:] :
            if cushionedBoard[blk] in alphabetString:
                return 0 
                
            # if cushionedBoard[blk-1] == "#":   
            #     cushionedBoard = cushionedBoard[:blk] + "#"+ cushionedBoard[blk+1:]  
            #     continue
            blockInOneOfThem = True
            otherBlkIndex = viewLeft[1:].index("#")+1
            #print(viewLeft)
            if otherBlkIndex != 1:

                if any([True for letter in viewLeft[0:otherBlkIndex] if letter in alphabetString]):
                    return 0
                newView = viewLeft
                for l in range(0,otherBlkIndex):
                    newView= newView[:l] + "#" + newView[l+1:]
                    if l !=0:
                        newlyAddedBlocks.append(cushionedIndex - l)

                ctr = 0 #fix this whoops
                for i in range(0,otherBlkIndex):
                    cushionedBoard = cushionedBoard[:blk+ ctr] + newView[i] + cushionedBoard[blk +ctr+1:]
                    ctr -=1
            


        viewDown = cushionedBoard[blk:blk+ 4 * (wid+2) :wid+2] #rightwards
   
        if "#" in viewDown[1:]:

            if cushionedBoard[blk] in alphabetString:
                return 0 
                
            # if cushionedBoard[blk+wid] == "#":   
            #     cushionedBoard = cushionedBoard[:blk] + "#"+ cushionedBoard[blk+1:]  
            #     continue
            #print('this shouldnt happen')
            blockInOneOfThem = True
            otherBlkIndex = viewDown[1:].index("#") + 1
            if otherBlkIndex != 1:
                if any([True for letter in viewDown[0:otherBlkIndex] if letter in alphabetString]):
                    return 0
                newView = viewDown
                for l in range(0,otherBlkIndex):
                    newView= newView[:l] + "#" + newView[l+1:]
                    if l !=0:
                        newlyAddedBlocks.append(cushionedIndex + l * (wid+2))
                #print(newlyAddedBlocks)
                ctr = 0
                for i in range(blk,blk+len(newView)*(wid+2),wid+2):
                    cushionedBoard = cushionedBoard[:i] + newView[ctr] + cushionedBoard[i+1:]
                    ctr+=1
            
        viewUp = cushionedBoard[blk:blk- (yCoordOfBlk+1 if yCoordOfBlk <=2 else 3) * (wid+2)-1 :-(wid+2)]

        if "#" in viewUp[1:] :

            if cushionedBoard[blk] in alphabetString:
                return 0 
                
                
            # if cushionedBoard[blk-wid] == "#":   
            #     cushionedBoard = cushionedBoard[:blk] + "#"+ cushionedBoard[blk+1:]  
            #     continue

            blockInOneOfThem = True
            otherBlkIndex = viewUp[1:].index("#") + 1
            if otherBlkIndex != 1:
                if any([True for letter in viewUp[0:otherBlkIndex] if letter in alphabetString]):
                    return 0
                newView = viewUp

                for l in range(0,otherBlkIndex):
                    newView= newView[:l] + "#" + newView[l+1:]
                    if l !=0:
                        newlyAddedBlocks.append(cushionedIndex - l * (wid+2))
                #print(newlyAddedBlocks)
                ctr = 0
                for i in range(blk,blk-len(newView)*(wid+2),-(wid+2)):
                    cushionedBoard = cushionedBoard[:i] + newView[ctr] + cushionedBoard[i+1:]
                    ctr+=1   #not sure if this should be - or +
            

        cushionedBoard =  cushionedBoard[: cushionedIndex] +  "#" +  cushionedBoard[cushionedIndex+1:] 
    if not blockInOneOfThem:

        cushionedBoard =  cushionedBoard[: cushionedIndex] +  "#" +  cushionedBoard[cushionedIndex+1:] 
    
  

    midBoard = decushionize(cushionedBoard,wid,ht)

    if not reversed:
        rotated = CCWRotate(CCWRotate(midBoard,ht),wid)
        if inInitial:
            if alreadyCushioned:
                finBoard = placeBlock(rotated,spot,wid,ht,reversed=True,inInitial=True,alreadyCushioned=True)
            else:
                finBoard = placeBlock(rotated,spot,wid,ht,reversed=True,inInitial=True,alreadyCushioned=False)
        else:
            if alreadyCushioned:
                finBoard = placeBlock(rotated,spot,wid,ht,reversed=True,inInitial=False,alreadyCushioned=True)
            else:
                finBoard = placeBlock(rotated,spot,wid,ht,reversed=True,inInitial=False,alreadyCushioned=False)

        if finBoard:
            #return finBoard
            if  inInitial:
                return finBoard
            if checkConnectivity(finBoard,width,height):
                return finBoard
            else:
                return 0
        else:
            return 0
    else:
        rotated = CCWRotate(CCWRotate(midBoard,ht),wid)
        if  inInitial:
            return rotated
        isConnected = checkConnectivity(rotated,width,height)
        if isConnected:
            return rotated
        else:
            return 0




def checkConnectivity(brd,wid,ht): #finish;
    # this is a dfs that checks if the graph is connected
    
    cushionedBoard = "#"* wid + "##"

    for i in range(ht):
        cushionedBoard+="#" 
        cushionedBoard += brd[i*wid:i*wid+wid]
        cushionedBoard+="#"
    cushionedBoard += "#"* wid + "##"
    adjList ={ ind:[] for ind, s in enumerate(cushionedBoard) if (s == "-" or s in alphabetString)}
    for ind, spot in enumerate(cushionedBoard):
        if not (spot == "-" or spot in alphabetString): continue
        neighbors  = [ind+1,ind-1,ind+wid+2,ind-(wid+2)]
        for nbr in neighbors:
            if cushionedBoard[nbr] != "#":
                adjList[ind].append(nbr)
    if not adjList:
        return True
    visited = {ind:False for ind in adjList}
 
    myStack = [] 
    myStack.append(list(adjList.keys())[0])
    
    while myStack:
        curr = myStack.pop()
        if visited[curr]:
            continue
        visited[curr] = True
        for nbr in adjList[curr]:
            myStack.append(nbr)
    if all(visited.values()):
        return True    
    else: return False   







def placeAllBlocks(brd, remainingBlocks): #Bruteforce algorithm, remaining blocks is Int
    #after calling placeBlock(), if there are more Added blocking squres than remaining blocks, then this sqare is not possible. 
    # if it is, subtract the number of added blocks from remaining blocks

    if remainingBlocks == 0:
        return brd

    for ind, obj in enumerate(brd):
        if obj == "-":
            blocksBeforePlacement = brd.count("#")
            placed = placeBlock(brd,ind,width,height, False)

            if not placed:
                continue
            addedBlocks = placed.count("#") - blocksBeforePlacement
            if addedBlocks > remainingBlocks:
                continue

            return placeAllBlocks(placed,remainingBlocks-addedBlocks)
    return brd


def otherClumpPlace(brd,wid,ht,remainingBlocks):
    if remainingBlocks == 0:
        return brd
    placed= brd
    while remainingBlocks !=0:
        blocksBeforePlacement = placed.count("#")
        bestBlock = findBestBlock(placed,wid,ht)
        
        placed = placeBlock(placed,bestBlock,wid,ht,False,False,True)
        if not placed: continue
        addedBlocks = placed.count("#") - blocksBeforePlacement
        remainingBlocks-= addedBlocks
        if addedBlocks > remainingBlocks:
            continue
    
    return placed

def antiClumpPlaceBlocks(brd,wid,ht,remainingBlocks,depth =0):
    if elapsed_time() > 20:
        print('cant do it')
        return placeAllBlocks(brd,remainingBlocks)
    if remainingBlocks == 0:
        return brd
    
    cb = "#"* wid + "##"

    for i in range(ht):
        cb+="#" 
        cb += brd[i*wid:i*wid+wid]
        cb+="#"
    cb += "#"* wid + "##"
    impossibles = []

    if remainingBlocks%2 != 1:

        impossibles.append(len(cb)//2)
        impossibles.append(len(cb)//2 + 1)
        impossibles.append(len(cb)//2 - 1)
        impossibles.append(len(cb)//2 - (wid+2))
        impossibles.append(len(cb)//2 + (wid+2))
    else:
        brd[len(brd)//2] == "#"
        remainingBlocks -=1



    bestToWorst = []
    inc = 3
    for i in range(inc):
        blk = findBestBlock(brd,wid,ht,impossibles)
        impossibles.append(blk)
        bestToWorst.append(blk)

    bestToWorst = bestToWorst[:inc]

    placed = brd
    for ind in bestToWorst:

            blocksBeforePlacement = brd.count("#")
            placed = placeBlock(brd,ind,width,height, False,False,True)
            if not placed:
                continue
            addedBlocks = placed.count("#") - blocksBeforePlacement
            if addedBlocks > remainingBlocks:
                continue
            print()
            display2d(placed,wid)
            res = antiClumpPlaceBlocks(placed,wid,ht,remainingBlocks-addedBlocks,depth+1)
            return res
    #return placeAllBlocks(placed,remainingBlocks)




def findBestBlock(brd,wid,ht,impsbls = []):
    cushionedBoard = "#"* wid + "##"
    for i in range(ht):
        cushionedBoard+="#" 
        cushionedBoard += brd[i*wid:i*wid+wid]
        cushionedBoard+="#"
    cushionedBoard += "#"* wid + "##"
    indToDist = {}
    w = wid + 2 #with the augment
    h = ht+2 #with the augment

    bestBlock = 0
    for i in range(len(cushionedBoard)):
        if i in impsbls:
            continue
        if cushionedBoard[i] != "-" or CCWRotate(CCWRotate(cushionedBoard,w),w)[i] != "-":
            continue
        rightDist = 0
        rightBoard = cushionedBoard[i+1:].split("#")
        rightDist = len(rightBoard[0])

        leftDist = 0
        leftBoard = cushionedBoard[i-1::-1].split("#")

        leftDist = len(leftBoard[0])

        upBoard = cushionedBoard[i-w:0:-w].split("#")
        upDist = len(upBoard[0])

        downBoard = cushionedBoard[i+w:len(cushionedBoard):w].split("#")
        downDist = len(downBoard[0])
        totalDist = min( upDist,downDist)+ min(rightDist,leftDist)


        if not placeBlock(decushionize(cushionedBoard,wid,ht),i,wid,ht,False,False,True) == 0:
            indToDist[i] = totalDist



    if not indToDist:
        return 0
    sorted_dict = dict(sorted(indToDist.items(), key=lambda item: item[1],reverse=True))
    first_key, first_value = next(iter(sorted_dict.items()))

    return first_key



      





def mdTile(pzl,goalpos,currpos):
    
   
    column = currpos//width
    row = currpos%height
    goalcolumn = goalpos//width
    goalrow = goalpos%height
    return (abs(goalcolumn-column) + abs(goalrow-row))

        


def placeHorizontally(brd,wid):
    brd = brd.lower()
    display2d(brd,wid)
    print()
    lines = []
    usedWords = set()
    for i in range (0,len(brd),wid):
        lines.append(brd[i:i+wid])
    for ind, line in enumerate(lines):

        availSpaces = []
        for indx, ch in enumerate(line):
            if ch == "#":
                availSpaces.append("#")
            else:
                if indx != 0 and line[indx-1] !="#":
                    continue
                nextBlock = line[indx:].find("#")
                if nextBlock == -1: 
                    availSpaces.append(line[indx:])
                    break
                availSpaces.append(line[indx:][0:nextBlock])

        for spaceInd, space in enumerate(availSpaces):
            if len(space) == 0:
                availSpaces[spaceInd] = "#"
                continue
            word = space
            charInds = {i:ch for i, ch in enumerate(word) if ch !="-"} #placed in the space where there are already characters 
            for w in lengthToWords[len(space)]:
                possibleWord = True
                for i in charInds:      
                    if w[i] != charInds[i]:
                        possibleWord = False
                if not possibleWord:continue
                if w not in usedWords:
                    
                    word = w
                    usedWords.add(word)
                    
                    break
            availSpaces[spaceInd] = word
        
        newLine = ''
        newLine = ''.join(availSpaces)
        # print(availSpaces)
        # if all([c=="#" for c in availSpaces]):
        #     newLine  = newLine + "#" * wid
        # else:
        #     for indx,chunk in enumerate(availSpaces):

        #         if indx == len(availSpaces)-1:
        #             newLine = newLine + chunk
        #             break
                
        #         if chunk !="#" and availSpaces[indx+1] != "#":
        #             newLine = newLine + chunk + "#"
        #         else:
        #             newLine = newLine + chunk

        lines[ind] = newLine
    finBoard = ''.join(lines)
    return finBoard
            
        
def getAllLocs(brd,wid):
    global specsToPoss
    locationsToFill = []
    for ind, char in enumerate(brd):
        if char != "#":
            if ind%wid == 0 or (brd[ind-1] == "#" and  ind%wid > 0 ):
                end = 0
                inc = ind
                indsInWord = []
                first = True
                for i in range(ind,len(brd)):
                    if i%wid == 0 and first == False:
                        break
                        
                    if brd[i] == "#":
                        end = i
                        break
                    else:
                        indsInWord.append(i)
                    
                    inc+=1
                    first = False
                if end == 0:
                    end = inc
                spec = brd[ind:end]
                if spec not in specsToPoss:
                
                    for word in lengthToWords[len(spec)]:
                        goodSoFar = True
                        for i, char in enumerate(spec):
                            if not (spec[i] == word[i] or spec[i] == "-"):
                                goodSoFar = False
                        if goodSoFar:
                            if spec in specsToPoss:
                                specsToPoss[spec].add(word)
                            else:
                                specsToPoss[spec] = {word}
                locationsToFill.append((ind,spec,indsInWord))
            
            if ind //wid == 0 or (brd[ind-wid] == "#" and ind//wid > 0):
                end = 0
                inc = ind
                indsInWord = []
                first = True
                for i in range(ind,len(brd),wid):

                    if brd[i] == "#":
                        end = i
                        break
                    else:
                        indsInWord.append(i)
                    
                    inc+=wid

                if end == 0:
                    end = inc
                spec = brd[ind:end:wid]
                if spec not in specsToPoss:
                    for word in lengthToWords[len(spec)]:
                        goodSoFar = True
                        for i, char in enumerate(spec):
                            if not (spec[i] == word[i] or spec[i] == "-"):
                                goodSoFar = False
                        if goodSoFar:
                            if spec in specsToPoss:
                                specsToPoss[spec].add(word)
                            else:
                                specsToPoss[spec] = {word}
                locationsToFill.append((ind,spec,indsInWord))


    return locationsToFill

def bF(brd,wid,usedWords = []):
    brd = brd.lower()
    print()
    display2d(brd,wid)

    wordLocations = getAllLocs(brd,wid)

    for ind , loc in enumerate(wordLocations):
        if loc[1].count("-") ==0:
            if not loc[1] in lengthToWords[len(loc[1])]:
               
                return 0
            wordLocations.remove(loc)
        if not loc[1] in specsToPoss or len(specsToPoss[loc[1]]) == 0:
            return 0

    if brd.count("-") == 0:
        return brd

    locToBeFilled = 0
    highestLength = 999999999999
    candidates = set()
    letterLocs = []
    for ind, loc in enumerate(wordLocations):
        if loc[1].count("-") == 0:
            continue
        if loc[1] not in specsToPoss or len(specsToPoss[loc[1]] )== 0:
            return 0
    
        tempCands = specsToPoss[loc[1]]

        lenPsbilities = len(tempCands)
        if lenPsbilities < highestLength:
            letterLocs = loc[2]
            locToBeFilled = ind
            highestLength = lenPsbilities
            candidates = tempCands
    for candidate in candidates:
        if candidate in usedWords:
            continue
        usedWords.append(candidate)
        newBrd = brd
        inc = 0
        for letter in letterLocs:
            newBrd = newBrd[:letter] + candidate[inc]+ newBrd[letter+1:]
            
            inc +=1

        bruted = bF(newBrd,wid,usedWords)
        if bruted: return bruted
        usedWords.remove(candidate)
    return 0

    
    

                


def main():
    setGlobals()
    global start_time 
    start_time= time.time()

    parseArgs(args)
    board = "-" * height * width
    if height * width == numBlocks:
        board = "#" * height * width
        #display2d(board,width)
        exit()
    for sS in seedStrings:
        preboard = board
        board = placeWord(board,sS,width)

        if board == 0:
            display2d(preboard,width)
            print(sS)
            exit()
        

    


    inputtedBlocks = board.count("#")
    totalBlocks = numBlocks-inputtedBlocks
    placed = antiClumpPlaceBlocks(board,width,height,totalBlocks)
    #placed = antiClumpPlaceBlocks(board,width,height,totalBlocks)
    display2d(placed,width)
    #placed= "SUcHLEgOAFrOCArP"
    placedWords = bF(placed.lower(),width)
    print()
    display2d(placedWords.lower(),width)  
    # print('elapsed time: ' + str(elapsed_time()))


if __name__ == '__main__': 
    

    main()

# Anmol Karan, pd 3, 2025