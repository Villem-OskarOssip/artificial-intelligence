from tkinter import *
import copy
import random
import pickle
import os.path
from PIL import ImageTk, Image

def createBoard():
    #Loome mängulaua
    leftBoardStartCol = 1
    rightBoardStartCol = boardWidth + 2
    #Loome tühimiku mängu ääre ja mängija mängulaua vahele
    createSpaces(1, 0)
    #Loome mängija ruudustiku
    createPlayerGrid(leftBoardStartCol)
    #Loome tühimiku kahe mängulaua vahele
    createSpaces(1, leftBoardStartCol + boardWidth)

    #Loome AI ruudustiku
    createAIGrid(rightBoardStartCol)
    #Loome tühimiku AI laua ja mängu ääre vahele
    createSpaces(1, rightBoardStartCol + boardWidth)

def createSpaces(rida, veerg):
    #Siin loome tühimikud
    global root
    Vahe = Label(root, height=2, width=5, backgroun = color7)
    Vahe.grid(row=rida, column=veerg, padx=0, pady=0)

def createAIGrid(rightBoardStartCol):
    #Siin loome AI ruudustiku
    for i in range(boardWidth):
        for j in range(boardWidth):
            button = Button(root, font="Times 13", height=1, width=3, bg=boardButton)
            button.grid(row=j + 3, column=i + rightBoardStartCol, padx=0, pady=0)
            button.configure(command=lambda i=i, j=j: pressButtonRight(j, i), state='disabled')
            AIGrid[(j, i)] = button

def createPlayerGrid(leftBoardStartCol):
    #Siin loome mängija ruudustiku
    for i in range(boardWidth):
        for j in range(boardWidth):
            button = Button(root, font="Times 13", height=1, width=3, bg=boardButton)
            button.grid(row=j + 3, column=i + leftBoardStartCol, padx=0, pady=0)
            button.configure(command=lambda i=i, j=j: pressButtonLeft(j, i))
            playerGrid[(j, i)] = button

def saveBoatLength6():
    #Salvestame mängija paadi pikkusega 6
    global boat6
    playerNotification.configure(text='Position your ship of length 5. ')
    updateButtonsLeft()
    boat6 = copy.deepcopy(current)
    updatePlayerBoatsCoordinates(boat6)
    current.clear()

def saveBoatLength5():
    # Salvestame mängija paadi pikkusega 5
    global boat5
    playerNotification.configure(text='Position your ship of length 4. ')
    updateButtonsLeft()
    boat5 = copy.deepcopy(current)
    updatePlayerBoatsCoordinates(boat5)
    current.clear()

def saveBoatLength4():
    # Salvestame mängija paadi pikkusega 4
    global boat4
    playerNotification.configure(text='Position your ship of length 3. ')
    updateButtonsLeft()
    boat4 = copy.deepcopy(current)
    updatePlayerBoatsCoordinates(boat4)
    current.clear()

def saveBoatLength3():
    # Salvestame mängija paadi pikkusega 3
    global boat3
    playerNotification.configure(text='Position your ship of length 2. ')
    updateButtonsLeft()
    boat3 = copy.deepcopy(current)
    updatePlayerBoatsCoordinates(boat3)
    current.clear()

def saveBoatLength2():
    # Salvestame mängija paadi pikkusega 2
    global boat2
    updateButtonsLeft()
    boat2 = copy.deepcopy(current)
    updatePlayerBoatsCoordinates(boat2)
    current.clear()

def updateButtonsLeft():
    #Värskendame UI
    for b in current:
        playerGrid[b].configure(background=color2)

def updatePlayerBoatsCoordinates(boat):
    #Salvestame mängija paadi asukoha koordinaadid
    for c in boat:
        playerAllBoatsCoordinates.append(c)

def pressButtonLeft(row, col):
    #Reageerime iga mängija laual vajutatud nupu peale selle meetodiga
    global boat6, boat5, boat4, boat3, boat2
    button = playerGrid[(row, col)]  # see nupp mida vajutati

    #Kui pole hõivatud ja pole keelatud asukohtade listis
    if button['text'] == "" and (row, col) not in forbiddenButtonsForBoats:
        button.configure(text="O", bg="black")
        current.append((row, col))
    #Kui nupp on võetud ja ole mängija kõikide laevade lõplikus listis
    #Selle kontrolliga saame teha valitud nupu uuesti mitte aktiivseks
    elif button['text'] == "O" and (row, col) not in playerAllBoatsCoordinates:
        button.configure(text="", bg=boardButton)
        current.remove((row, col))

    #Kontrollime, kas laev pikkusega 6 on veel tühi ja kas mängulaual leidub koordinaatide põhjal mõni salvestamata kuuene laev
    if len(boat6) == 0 and isBoat(6):
        saveBoatLength6()

    #Kontrollime kas kuuene laev juba hõivatud, kas viieme laev veel tühi ja laual on üks  salvestamata viiene laev
    if len(boat6) != 0 and len(boat5) == 0 and isBoat(5):
        saveBoatLength5()

    #Kontrollime, kas kuuene ja viiene laev olemas, kas neljane veel tühi ja laual on üks salvestamata neljane laev
    elif len(boat6) != 0 and len(boat5) != 0 and len(boat4) == 0 and isBoat(4):
        saveBoatLength4()

    #Kontrollime, kas kuuene, viiene, neljane hõivatud, kas kolmene vaba ja kas laual on salvestamata kolmest
    elif len(boat6) != 0 and len(boat5) != 0 and len(boat4) != 0 and len(boat3) == 0 and isBoat(3):
        saveBoatLength3()

    #Kontrollime, kas kuuene, viiene, neljane ja kolmene hõivatud, kas kahene vaba ja kas laual on salvestamata kahest
    elif len(boat6) != 0 and len(boat5) != 0 and len(boat4) != 0 and len(boat3) != 0 and len(boat2) == 0 and isBoat(2):
        saveBoatLength2()
        #Kõik laevad on valitud ja võib alustada mänguga
        allBoatsAreChosen_EnableBombingMode()

    #Uuendame keelatud nuppe
    updateForbiddenButtonsForPlayer()

def updateForbiddenButtonsForPlayer():
    #Kui on salvestatud ära üks laev, siis uuendama keelatud koordinaatide listi.
    #Listi salvestame koordinaadid mis on igast ruudust igas ilmakaare ühe ruudu kaugusel.
    #Sellega väldime mängijal oma laevade asetamise otse üksteise kõrvale
    global playerAllBoatsCoordinates, forbiddenButtonsForBoats
    for elem in playerAllBoatsCoordinates:
        surroundingButtons = []
        zeroPoint = (elem[0] - 1, elem[1] - 1)
        for y in range(3):
            for x in range(3):
                point = (zeroPoint[0] + y, zeroPoint[1] + x)
                surroundingButtons.append(point)
                if not point in forbiddenButtonsForBoats:
                    if point in playerGrid:
                        forbiddenButtonsForBoats.append(point)
                        playerGrid[point].configure(state='disabled')

def allBoatsAreChosen_EnableBombingMode():
    global playerBoats, playerAllBoatsCoordinates
    #Kontrollime üle, kas kõik laevad olemas mängija poolt
    if len(boat6) != 0 and len(boat5) != 0 and len(boat4) != 0 and len(boat3) != 0 and len(boat2) != 0:
        playerNotification.configure(text=' ') #Tühjendame mägija teate laua
        playerBoats = [boat6, boat5, boat4, boat3, boat2]
    for b in playerGrid:
        playerGrid[b].configure(state='disabled')  # Lülitame välja vasakpoole mängulaua kõik nupud kuna mäng on alanud.
    for e in AIGrid:
        AIGrid[e].configure(state='normal')  # Lülitame sisse kõik AI poole mängulaua nupud, et saaks alustada pommitamisega
    for e in playerBoats:
        playerSunkedBoats[str(e)] = False #Mängija pommitatud laevade listi lisame kõik valitud laevad ja määrame nende staatuseks False
    teade.configure(text='Bombs away!')  # Uus teade

def isBoat(length):
    #Siin meetodis kontrollime, kas laual leidub ette antud pikkusega laev
    global current
    x_id = set() #Loome X telje listi
    y_id = set() #Loome Y telja listi
    for e in current:
        x_id.add(e[0]) #Jaotame mängija poolt valitud koordinaadid vastavalt kahte listi
        y_id.add(e[1])
    if len(x_id) == 1: #Kui tulbas on täpselt 1 element, siis järlikult potensiaalne laev
        min, max = getMaxMin(y_id)
        # Kontrollime kas nupud on järjest ja õiges pikkusega
        # Kui laual on rohkem või vähem nuppe siis False
        # Kui laual on piisavalt nuppe ühes tulbas, aga need ei ole koos, siis tagastame False
        if max - min == (length - 1) and len(y_id) == length:
            return True #agastame True, sest on leitud piisava pikkusega salvestamata laev
    elif len(y_id) == 1: #Kui reas on täpselt 1 element, siis järlikult potensiaalne laev
        minimum, maximum = getMaxMin(x_id)
        if maximum - minimum == (length - 1) and len(x_id) == length:  #Kontrollime kas nupud on järjest ja õiges pikkusega
            return True

def getMaxMin(list):
    # leiab listist maximumi ja minimumi
    maximum = -1
    minimum = 10
    for elem in list:
        if int(elem) > maximum: maximum = elem
        if int(elem) < minimum: minimum = elem
    return minimum, maximum

def pressButtonRight(row, col):
    #Kontrollime, kas on juba klikatud antud AI kasti
    if (row, col) not in playerGuesses:
        #Kui ei ole, siis lisame antud pakkumise mängija pakkumiste listi
        playerGuesses.append((row, col))
        # Lisame mängija pakkumise kaalutud väärtustega pakkumiste sõnastikku
        global guessCounter, allGuesses
        if ((row, col) not in allGuesses):
            allGuesses[(row, col)] = 0
        allGuesses[(row, col)] += guessWeights[guessCounter]
        guessCounter += 1
        #Kui vastase laevale pihta saanud
        if playerHitEnemyShip(row, col):
            #Uuendame pihta saanud paeva välja
            updateHitShip(row, col)
            #Kontrollime, kas pihsa läinud koordinaat oli viimane vastase laeva osast
            checkDidBoatSunk()
            checkIfGameOver()
        else:
            #Uendame mööda läinud listi
            updateMiss(row, col)
            #Kui ei saadud pihta, siis järgmisena käib AI
            doAIMove()
        # Enne järgmist käiku kontrollime, kas mäng on läbi
        # checkIfGameOver() # Põhjustab AI võidu puhul topeltlõpetamise (sh. duubelread result.txt failis)???

def updateMiss(row, col):
    AIGrid[(row, col)].configure(text="O")
    AIGrid[(row, col)].configure(background=color1)
    aiNotification.configure(text="MISS!")

def updateHitShip(row, col):
    #Siin uuendame pihta sanud laeva UI
    global playerHitGuesses
    playerHitGuesses.append((row, col))
    AIGrid[(row, col)].configure(text="X")
    AIGrid[(row, col)].configure(background=color6)
    aiNotification.configure(text="HIT!")

def playerHitEnemyShip(row, col):
    return (row, col) in AIAllBoatsCoordinates

def checkDidBoatSunk():
    #Kontrollime siin kas paat läks põhja
    for paat in AIBoats: #Vaatame läbi kogu tehisintellekti laevade listi
        if all(x in playerHitGuesses for x in paat):
            # Kui kogu paat on pihtas, siis muudame värvi laeval
            for b in paat:
                AIGrid[b].configure(background=color3)
            AISunkedBoats[str(paat)] = True  # lisame uppunud laevade listi
            # Jooksvate pihtasaamiste kustutamine
            global playerHitGuesses
            playerHitGuesses.clear()
            aiNotification.configure(text="DOWN YOU GO!")

def doAIMove():
    #Siin toimub AI käik
    global AIGuesses, AIHitGuesses
    if len(AIHitGuesses) == 0:
        move = AIMove(coordinateFreqDict)
    else:
        move = AIPickNext(AIHitGuesses[-1], coordinateFreqDict)

    AIGuesses.add(move)
    if move in playerAllBoatsCoordinates:
        AIHitPlayerBoat(move)
        boatIsSunk = checkDidAIManageToSinkABoat()
        checkIfGameOver()
        if (boatIsSunk):
            AIHitGuesses.clear()
        doAIMove()
    else:
        AIMiss(move)

def AIHitPlayerBoat(move):
    #uuendmae UI
    playerGrid[move].configure(text="X")
    playerGrid[move].configure(background=color5)
    AIHitGuesses.append(move)

def AIMiss(move):
    #Uuendame UI
    playerGrid[move].configure(text="-")
    playerGrid[move].configure(background=color1)

def pickMoveRandom():
    #Valime suvalise võimaliku käigu ja tagastame selle
    voimalikud = []
    for e in playerGrid.keys():
        if e not in AIGuesses:
            voimalikud.append(e)
    return random.choice(voimalikud)

def checkDidAIManageToSinkABoat():
    #Siin kontrollime, kas AI lasi mängija laeva põhja
    for paat in playerBoats:
        if all(x in AIHitGuesses for x in paat):
            # kogu paat põhjas -> värvime ära
            for b in paat:
                playerGrid[b].configure(background=color4)
            playerSunkedBoats[str(paat)] = True  # lisame uppunud laevade listi
            # Lisame laeva ümbruses olevad nupud AI pakkumiste hulka, sest seal ei saa enam laevu olla
            global AIGuesses
            forbidden = getForbiddenButtonsForAI(paat)
            for coord in forbidden:
                AIGuesses.add(coord)
            return True
    return False

def checkIfGameOver():
    #Siin kontrollime, kas mäng on läbi saanud
    if playerWon():
        displayWin()
    elif playerLost():
        displayLoss()

def displayLoss():
    teade.configure(text="You lost...")
    for b in AIGrid:
        AIGrid[b].configure(state='disabled')
    endOfGame()

def displayWin():
    teade.configure(text="Congratulations, you won!")
    for b in AIGrid:
        AIGrid[b].configure(state='disabled')
    endOfGame()

def playerWon():
    #Kontrollime, kas mängija võitis
    return all(x == True for x in AISunkedBoats.values())

def playerLost():
    #Kontrollime, kas AI võitis
    return all(x == True for x in playerSunkedBoats.values())

def endOfGame():
    #Mäng sai läbi
    addPlayerBoats()

    #Teeme vajalikud salvestused faili, et AI järgmine mäng paremini teaks arvata
    saveCoordinateFreqDict()
    saveGuessesDict()

def defineAIBoats():
    #Loome AI laevad
    global AIBoats, boat2, boat3, boat4, boat5, boat6
    AI6 = generateBoat(6)
    AI5 = generateBoat(5)
    AI4 = generateBoat(4)
    AI3 = generateBoat(3)
    AI2 = generateBoat(2)
    AIBoats = [AI6, AI5, AI4, AI3, AI2]

    for e in AIBoats:
        AISunkedBoats[str(e)] = False #Lisame kõik AI laevad põhja läinud laevade sõnastikku ja määrave väärtuseks False

def generateBoat(length):
    #Siin loome AI laevad ette antud pikkusega
    global allGuesses, AIAllBoatsCoordinates

    boat = []
    x_id = []
    y_id = []

    mostLessFrequent = lastChosen(allGuesses, boat)
    start = random.choice(mostLessFrequent)
    boat.append(start)
    startX = start[0]
    startY = start[1]
    x_id.append(startX)
    y_id.append(startY)

    forbidden = getForbiddenButtonsForAI(AIAllBoatsCoordinates)
    # Loendurid, mis jälgivad, et ei jääks tsüklisse kui ei leidu laeva jaoks vajalik arv vabu ruute
    progress_counter_prev = 0
    progress_counter = 0
    while (len(boat) != length):
        allSurroundingButtons = findSurroundingButtons(boat)

        for i in range(len(allSurroundingButtons)):
            e = random.choice(allSurroundingButtons)
            if e not in forbidden:
                x = e[0]
                y = e[1]
                x_id.append(x)
                y_id.append(y)  # lisame listi
                if len(set(x_id)) == 1 or len(set(y_id)) == 1:  # ja vaatame kas ikka on ühel joonel
                    boat.append(e)
                    progress_counter += 1
                    break
                else:
                    x_id.remove(x)
                    y_id.remove(y)
        if progress_counter == progress_counter_prev:  # Juhul kui jääb tsüklisse ja laeva jaoks ei leidu sobivat ruutu
            return generateBoat(length)  # Püüab uuesti laeva luua
        else:
            progress_counter_prev = copy.copy(progress_counter)
    for elem in boat:
        AIAllBoatsCoordinates.append(elem)
    return boat

def findSurroundingButtons(boat):
    #Ümbritsevate nuppude leidmine
    surrounding = []
    for coordinate in boat:
        surroundingThatButton = surroundingButtonsGen(coordinate)
        for button in surroundingThatButton:
            if button not in surrounding and button not in boat:
                surrounding.append(button)
    return surrounding

def surroundingButtonsGen(elem):
    #Ümbritsevate nuppude loomine
    global AIGrid
    list = [(elem[0] - 1, elem[1]), (elem[0] + 1, elem[1]),
            (elem[0], elem[1] - 1), (elem[0], elem[1] + 1)]
    result = []
    for e in list:
        if e in AIGrid:
            result.append(e)
    return result

def getForbiddenButtonsForAI(lst):
    #Tagastame koordinaadid, mis on AI jaoks keelatud
    result = []
    for elem in lst:
        surroundingButtons = [(elem[0] - 1, elem[1]), (elem[0] + 1, elem[1]),
                              (elem[0], elem[1] - 1), (elem[0], elem[1] + 1),
                              (elem[0] - 1, elem[1] - 1), (elem[0] + 1, elem[1] + 1),
                              (elem[0] + 1, elem[1] - 1), (elem[0] - 1, elem[1] + 1)]
        for surrounding in surroundingButtons:
            if not surrounding in result:
                if surrounding in playerGrid:
                    result.append(surrounding)
    return result

def lastChosen(dict, buttonsAlreadyInBoat):
    forbidden = getForbiddenButtonsForAI(AIAllBoatsCoordinates)
    # võtab kõige viimasena pakutud buttonid ja vaatab ega nad juba keelatud ei ole (laevade läheduses)
    max = 0
    keys = [(0, 0)]
    for k in dict.keys():
        if k not in forbidden and k not in AIAllBoatsCoordinates and k not in buttonsAlreadyInBoat:
            # Otsime suurima väärtusega ehk kõige hiljem valituid kohti mängulaual
            if dict[k] > max:
                max = dict[k]
                keys = [k]
            elif dict[k] == max:
                keys.append(k)
    return keys

def findMostPickedSpot(dict):
    #Siin valime välja koordinaadid, mille peale AI panustab
    max = 0
    keys = []
    for k in dict.keys():
        if k not in AIGuesses:
            # Otsime suurima väärtusega ehk kõige hiljem valituid kohti mängulaual
            if dict[k] > max:
                max = dict[k]
                keys = [k]
            elif dict[k] == min:
                keys.append(k)
    return keys

## AI pakub kõige sagedamini valitud asukohti. Kui kõige sagedasem on valitud, siis vaatab edasi,
# et missugune ruut vasakult, paremalt, ülevalt või alt on järgmisena kõige rohkem täidetud olnud.
# Kui laev on põhja lastud, siis vastavalt reeglitele - ümbritsevaid ruute enam ei pakuta.
def AIMove(dict):
    # Teeb esimese valiku nuppude seast, mida mängija on varem kõige rohkem laevade asukohaks valinud
    keys = findMostPickedSpot(dict)
    # Kontroll, kas mingi sobiv pakkumine on varasemate laevade asukohtade seast leitud
    if len(keys) == 0:
        # Juhul kui mängija laevad on kohtades, kus kunagi varem pole laevu olnud, tehakse juhuslik valik
        pickKey = pickMoveRandom()
    else:
        pickKey = random.choice(keys)
    return pickKey


def onTheSameRow(AIHits):
    return AIHits[0][0] == AIHits[1][0]

def findHitNeighbours(button):
    if len(AIHitGuesses) > 1:
        # Kontroll, kas asuvad samal real
        if onTheSameRow(AIHitGuesses):
            neighbours = [(button[0], button[1] - 1), (button[0], button[1] + 1)]
        else:
            # Asuvad samas veerus
            neighbours = [(button[0] - 1, button[1]), (button[0] + 1, button[1])]
    else:
        # Määratleme kõikvõimalikud naabrid läbi
        neighbours = [(button[0] - 1, button[1]), (button[0] + 1, button[1]),
                      (button[0], button[1] - 1), (button[0], button[1] + 1)]
    return neighbours

def findAnotherPopularOption(pot, dict):
    max_key = pot[0]
    max_value = 0
    for el in pot:
        if (el in dict and dict[el] > max_value):
            max_key = el
            max_value = dict[el]
    return max_key

def findPotentialPicks(neighbours):
    potentials = []
    for coord in neighbours:
        if (coord in playerGrid and coord not in AIGuesses):
            potentials.append(coord)
    return potentials

# Funktsioon kõrvalasuva asukoha pakkumiseks
def AIPickNext(button, dict):
    neighbours = findHitNeighbours(button)

    potentialPicks = findPotentialPicks(neighbours)

    if len(potentialPicks) == 0:
        return AIPickNext(AIHitGuesses[0], coordinateFreqDict)
    # Juhul kui on ainult üks võimalik koht
    elif len(potentialPicks) == 1:
        return potentialPicks[0]
    else:
        return findAnotherPopularOption(potentialPicks, dict)

def readCoordinateFreqDict():
    coordinateDict = pickle.load(open("playerBoatsCoordFrequencyDictFile.p", "rb"))
    dict = {}
    for elem in coordinateDict.keys():  # convering back to tuples
        x = int(elem[0])
        y = int(elem[1])
        value = coordinateDict[elem]
        dict[(x, y)] = value
    return dict

def readGuessesDict():
    guessesDict = pickle.load(open("playerGuessesFrequencyDictFile.p", "rb"))
    for elem in guessesDict.keys():  # convering back to tuples
        x = int(elem[0])
        y = int(elem[1])
        value = guessesDict.pop(elem)
        guessesDict[(x, y)] = value
    return guessesDict

# Pärast mängu lõppu tuleb mängija poolt valitud laevade asukohtade ruudud salvestada "populaarseimate" ruutude hulka,
# mida AI kasutab alates järgmisest mängust pommitamiseks.
def addPlayerBoats():
    global coordinateFreqDict
    for coordinate in playerAllBoatsCoordinates:
        if (coordinate not in coordinateFreqDict):
            coordinateFreqDict[coordinate] = 1
        else:
            coordinateFreqDict[coordinate] += 1

def saveCoordinateFreqDict():
    #Salvestame arvamiste sageduse AI jaoks faili
    global coordinateFreqDict
    pickle.dump(coordinateFreqDict, open("playerBoatsCoordFrequencyDictFile.p", "wb"),
                protocol=pickle.HIGHEST_PROTOCOL)

def saveGuessesDict():
    #Salvestame kõikide arvamiste koordinaadid faili AI joaks
    global allGuesses
    pickle.dump(allGuesses, open("playerGuessesFrequencyDictFile.p", "wb"),
                protocol=pickle.HIGHEST_PROTOCOL)

def initPlayerVars():
    #Siin loome kõik globaalsed muutujad
    global playerAllBoatsCoordinates, boat6, boat5, boat4, boat3, boat2, playerBoats, playerSunkedBoats, forbiddenButtonsForBoats
    forbiddenButtonsForBoats = []
    playerAllBoatsCoordinates = []
    boat6 = {}
    boat5 = {}
    boat4 = {}
    boat3 = {}
    boat2 = {}
    playerBoats = []
    playerSunkedBoats = {}

def initAIVars():
    #Siin loome AI kõik globaalsed muutujad
    global AIAllBoatsCoordinates, AISunkedBoats, playerGuesses, playerHitGuesses, guessCounter, AIGuesses, AIHitGuesses

    AIAllBoatsCoordinates = []
    AISunkedBoats = {}
    playerGuesses = []
    playerHitGuesses = []
    guessCounter = 0
    AIGuesses = set()
    AIHitGuesses = []

def gameStartNotifications():
    #Uuendmae UI
    teade.configure(text="Place your ships on the board!")
    playerNotification.configure(text='Position a ship of length 6. ')
    aiNotification.configure(text=" ")

def start():
    #Mängu alguse edasiloomine
    initPlayerVars()
    initAIVars()

    global allGuesses, coordinateFreqDict
    # AI jaoks andmete sisse lugemine
    allGuesses = readGuessesDict()
    coordinateFreqDict = readCoordinateFreqDict()

    #Loome mängulaua
    createBoard()
    #Defineerime AI laevad
    defineAIBoats()
    #Uuendmae UI teated
    gameStartNotifications()

def createFiles():
    # Siin loome vajalikud failid, mida AI hakkab kasutama
    if not os.path.isfile("playerBoatsCoordFrequencyDictFile.p"):  # fails don't exist yet -> inizialize
        d = {}
        for i in range(boardWidth):
            for j in range(boardWidth):
                d[(j, i)] = 0
        pickle.dump(d, open("playerBoatsCoordFrequencyDictFile.p", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(d, open("playerGuessesFrequencyDictFile.p", "wb"), protocol=pickle.HIGHEST_PROTOCOL)

def setColors():
    # Määrame värvid
    global color1, color2, color3, color4, color5, color6, color7, boardButton
    color1 = 'White'
    color2 = 'gray28'
    color3 = 'RoyalBlue2'
    color4 = 'red3'
    color5 = 'PaleGreen3'
    color6 = 'gray'
    color7 = 'red'
    boardButton = 'cornflower blue'

def createWeights():
    #Määrame raskused
    weights = []
    start = 0.1
    step = 0.1
    for i in range(100):
        weights.append(start)
        start += step
    return weights

def main():

    # Loome listid
    global boardWidth, playerGrid, AIGrid, current
    boardWidth = 10 #Mängulaua laius (standard on 10)
    playerGrid = {}
    AIGrid = {}
    current = []  #List kus hoitakse mängija poolt valitud enda mängulaua nupud, mis veel ei ole laevadeks määratud.

    # Väärtuste listi loomine hilisemaks mängija pakkumiste loendamiseks
    global guessWeights
    guessWeights = createWeights()

    # Siin looome UI
    global root, teade, playerNotification, aiNotification
    root = Tk()
    root.wm_title("Battleships")
    root.resizable(0, 0)

    img = ImageTk.PhotoImage(Image.open("ship.jpg"))

    background_label = Label(root, image=img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #Mängija teade
    Label(root, text="Your ships", font="Times 15 bold", backgroun = color7).grid(row=13, column=1, padx=10, pady=8,
                                                                           columnspan=10)
    #AI teade
    Label(root, text="Enemy ships", font="Times 15 bold", backgroun = color7).grid(row=13, column=12, padx=10, pady=8,
                                                                               columnspan=10)
    #Mängija üleüldised teated
    teade = Label(root, text="Place your ships on the board.", font="Times 13 bold", backgroun = color7)
    teade.grid(row=0, column=1, padx=10, pady=8, columnspan=21)

    #Mängija teated
    playerNotification = Label(root, text='Position a ship of length 6.', font="Times 13 bold", backgroun = color7)
    playerNotification.grid(row=1, column=1, padx=10, pady=8, columnspan=10)

    #AI teade
    aiNotification = Label(root, text=" ", font="Times 13 bold", backgroun = color7)
    aiNotification.grid(row=1, column=12, padx=10, pady=8, columnspan=10)

    #restart nupp
    loppNupp = Button(root, text="Restart", command=lambda: start(), font="Times 11 bold", backgroun = color7)
    loppNupp.grid(row=0, column=20, padx=10, pady=8, columnspan=3)

    #Alustame mängu loomisega
    start()
    #Mängu loop
    root.mainloop()

createFiles()
setColors()
main()
