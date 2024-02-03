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

def placeBlock(brd,spot,wid,ht):   #checks if a block can be placed in the spot
    cushionedBoard = "#"* wid + "##"
    for i in range(ht):
        cushionedBoard+="#" 
        cushionedBoard += brd[i*wid:i*wid+wid]
        cushionedBoard+="#"
    cushionedBoard += "#"* wid + "##"
    yCoord = spot //wid
    xCoord = spot%wid 
    cushionedIndex =   wid+2 + (yCoord * (wid+2)) + 1 + xCoord

    newlyAddedBlocks = [cushionedIndex]
    blockInOneOfThem = False

    while newlyAddedBlocks:
        # display2d(cushionedBoard,wid+2)
        #print(newlyAddedBlocks)
        blk = newlyAddedBlocks.pop(0)
        if cushionedBoard[blk] not in  "-#":

            return -1
        if cushionedBoard[blk] == "#":
            #display2d(cushionedBoard,wid+2)
            #make sure to decushionize the board
            return cushionedBoard
        

            
        viewRight = cushionedBoard[blk:blk+4] #rightwards
        if "#" in viewRight[1:]:
            #print('this shouldnt happen')
            blockInOneOfThem = True
            otherBlkIndex = viewRight[1:].index("#") + 1
            if any([True for letter in viewRight[0:otherBlkIndex] if letter in alphabetString]):
                return -1
            newView = viewRight
            for l in range(0,otherBlkIndex):
                newView= newView[:l] + "#" + newView[l+1:]
                if l !=0:
                    newlyAddedBlocks.append(cushionedIndex + l)
            #print(newlyAddedBlocks)
            ctr = 0
            for i in range(blk,blk+4):
                cushionedBoard = cushionedBoard[:cushionedIndex + ctr] + newView[ctr] + cushionedBoard[cushionedIndex +ctr+1:]
                ctr+=1

        viewLeft = cushionedBoard[blk:blk-4:-1]
        if "#" in viewLeft[1:]:
            blockInOneOfThem = True
            otherBlkIndex = viewLeft[1:].index("#")+1
            if any([True for letter in viewLeft[0:otherBlkIndex] if letter in alphabetString]):
                return -1
            newView = viewLeft
            for l in range(0,otherBlkIndex):
                newView= newView[:l] + "#" + newView[l+1:]
                if l !=0:
                    newlyAddedBlocks.append(cushionedIndex - l)

            ctr = 0 #fix this whoops
            for i in range(0,otherBlkIndex):
                cushionedBoard = cushionedBoard[:cushionedIndex+ ctr] + newView[i] + cushionedBoard[cushionedIndex +ctr+1:]
                ctr -=1

            

    if not blockInOneOfThem:

        cushionedBoard =  cushionedBoard[: cushionedIndex] +  "#" +  cushionedBoard[cushionedIndex+1:] 

    #decushionize
    #call placeBlock() on opposite index
    #return whatever that returns

    #display2d(cushionedBoard,wid+2)
    return cushionedBoard


def main():
    setGlobals()
    parseArgs(args)
    board = "-" * height * width
    if height * width == numBlocks:
        board = "#" * height * width
        display2d(board,width)
        exit()

    for sS in seedStrings:
        board = placeWord(board,sS,width)
    #display2d(board,width)
    pB = placeBlock(board, 2,width,height)
    if pB == -1:
        display2d(board,width)
    else:
        display2d(pB,width+2)


    


if __name__ == '__main__': 
    

    main()


# Anmol Karan, pd 3, 2025
    