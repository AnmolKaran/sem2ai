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
    display2d(board,width)


    


if __name__ == '__main__': 
    

    main()


# Anmol Karan, pd 3, 2025