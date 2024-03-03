import sys; args = sys.argv[1:]




def parseArgs(argList):
    for arg in argList:

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






def setGlobals():
    global height
    global width 
    global numBlocks
    global seedStrings
    global alphabetString

    alphabetString = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    height = 0
    width = 0
    numBlocks = 0
    seedStrings = []

    

def decushionize(brd, origWid,origHeight):
    #newBrd = brd[origWid+2:]
    newBrd = ""

    for i in range(origHeight):
        line = brd[(i+1)*(origWid+2) + 1 :(i+1)*(origWid+2) + 1 + origWid]
        newBrd = newBrd + line
    return newBrd


def display2d(pzl,wid):
   startIndeces = [q for q in range(0,len(pzl),wid) ]
   listed = []
   for q in startIndeces:
       listPuzzle = list(pzl)
       theThing  = listPuzzle[q: q+wid]
       listed.append(' '.join(theThing))
  


   if len(listed) ==0:
       print("No solution found")
   else:
       for i in listed:
           print (i)


def placeWord(board, seedStr,wid):
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
    if direction == "H":
        wordIncrement = 0
        for i in range(startingInd,startingInd+ len(word)):
            if board[i] != "#"  and not (i%width == width-1 and wordIncrement <  len(word)-1):
                board= board[:i] + word[wordIncrement] + board[i+1:]
                wordIncrement+=1
            else:
                return -1
        return board
    if direction == "V":
        wordIncrement = 0
        for i in range(startingInd,len(board),width):
            if board[i] != "#":
                board= board[:i] + word[wordIncrement] + board[i+1:]
                wordIncrement+=1
                if wordIncrement >= len(word):
                    return board
            else:
                return -1
        if wordIncrement !=  len(word)-1 : #the word hasnt fully even been spelled out
            return -1
        return board


def placeBlocks(brd, remainingBlocks): #Bruteforce algorithm
    #after calling placeBlock(), if there are more Added blocking squres than remaining blocks, then this sqare is not possible. 
    # if it is, subtract the number of added blocks from remaining blocks
    return


def decuchionize():
    return

def getOppositeIndex():

    return




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




def CCWRotate(brd,wid):

    finString = ""
    for colStart in range(wid-1,-1,-1):
        rs = brd[colStart:len(brd):wid]
        finString+=rs

    return finString


def main():
    setGlobals()
    parseArgs(args)
    width = 7
    height = 7
    board = "-" * height * width
    # if height * width == numBlocks:
    #     board = "#" * height * width
    #     display2d(board,width)
    #     exit()

    for sS in seedStrings:
        board = placeWord(board,sS,width)
    # display2d(board,width)
    # pB = placeBlock(board, 2,width,height)
    # if pB == -1:
    #     display2d(board,width)
    # else:
    #     display2d(pB,width+2)
    # b = '--------#--------------------------------------#------------#--------------------------------------#--------'
    # display2d(b,12)
    # p = b[144]
    # print(p)
    s = "SUcHLEgOAFrOCArP"
    display2d(s,width)
    placed = placeBlock(s,19,width,height,False,False,True)


if __name__ == '__main__': 
    

    main()


# Anmol Karan, pd 3, 2025
    