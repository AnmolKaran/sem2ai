def placewords(placesf, fill, width, height):
    global words, worddict, placed, boardarray, NEWBOARD, counter, posdict, constraints, \
        partial, partialboard, complete
    if fill == len(placesf):
        complete = True
        # Check if all horizontal words are placed
        horizontal_placed = all('H' in place[1] for place in placesf)
        if horizontal_placed:
            print("All horizontal words placed:")
            twoDPrint(NEWBOARD, height, width, 0)
        return True
    wordlen = 0
    pattern = "^"
    places = placesf[fill]
    pos = places[0]
    wordlen = places[2]
    posdisp = "" + str(places[0])+places[1]
    for i in posdict[posdisp]:
        cell = NEWBOARD[i]
        if cell == "#":
            break
        elif cell == "-":
            pattern = pattern + "."
        else:
            pattern = pattern + cell.upper()
    pattern = pattern + "$"
    visited = list()
#    wordlist = [word for word in words if re.match(pattern,word.upper()) and len(word) == wordlen]
    #print(places[0], places[1],places[2],len(wordlist))
    if pattern[1] == ".": wordkey = "-"+str(wordlen)
    elif pattern[1].lower()+str(wordlen) not in worddict.keys(): wordkey = "-"+str(wordlen)
    else: wordkey = pattern[1].lower()+str(wordlen)
    #print("posdisp, pattern, wordkey, worddict",posdisp,pattern,wordkey, worddict[wordkey])
    for word in worddict[wordkey]:
        if word.upper() in placed or not re.match(pattern,word.upper()): continue
        visited.append(word)
        #print("matching", places[0], places[1],places[2],word)
        NEWWBOARD = NEWBOARD
        if places[1] == "H":
            for i in range(len(word)):
                NEWBOARD = NEWBOARD[:pos+i]+word[i]+NEWBOARD[pos+i+1:]
        else:
            for i in range(len(word)):
                NEWBOARD = NEWBOARD[:pos+i*width]+word[i]+NEWBOARD[pos+i*width+1:]
        failedcon = False
        for con in constraints[posdisp]:
            patcon = "^"
            lencon = 0
            letter = False
            for poscon in posdict[con]:
                if NEWBOARD[poscon] == "-":
                    patcon = patcon + "."
                else:
                    patcon = patcon + NEWBOARD[poscon].upper()
                    letter = True
                lencon += 1
            if letter:
                patcon = patcon + "$"
                if patcon[1] == ".":
                    patkey = "-" + str(lencon)
                elif patcon[1].lower() + str(lencon) not in worddict.keys():
                    patkey = "-" + str(lencon)
                else:
                    patkey = patcon[1].lower() + str(lencon)
                #print("  word",word," posdisp",posdisp,"patcon",patcon,"patkey:",patkey,"newboard",NEWBOARD, )
                matchlist = [word for word in worddict[patkey] if re.match(patcon,word.upper())]
                if matchlist == []:
                    #print("matchng", patcon, patkey, worddict[patkey]);
                    failedcon = True
                    break
        #print("failedcon ",failedcon)
        if failedcon: NEWBOARD = NEWWBOARD; continue
        placed.append(word.upper())
        if "Recursion" in stats:
            stats["Recursion"] += 1
        else:
            stats["Recursion"] = 1
        if time.time() - s > counter: counter = counter + 30; print(stats); twoDPrint(NEWBOARD, height, width, 0)
        match = placewords(placesf,fill+1,width,height)
        if match:
            return match
        placed.remove(word.upper())
        NEWBOARD = NEWWBOARD
    if not partial:
        partialboard = NEWBOARD
    partial = True
    return False
