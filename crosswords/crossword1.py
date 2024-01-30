import sys; args = sys.argv[1:]




def parseArgs(argList):
    for arg in argList:
        if "x" in arg or "X" in arg:
            splitted = arg.lower().split("x")      
            global height
            global width 
            height = int(splitted[0])
            width = int(splitted[1])
        else:
            global numBlocks
            numBlocks = int(arg)





def setGlobals():
    global height
    global width 
    global numBlocks
    
    height = 0
    width = 0
    numBlocks = 0

def main():
    parseArgs(args)


if __name__ == '__main__': 
    

    main()


# Anmol Karan, pd 3, 2025