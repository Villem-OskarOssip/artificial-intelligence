# coding: utf-8
from tkinter import *
import copy
import random
import pickle
import os.path


def createSpace(rida, veerg):
    taustavarv = root.cget('bg')
    Vahe = Text(root, height=2, width=5, background=taustavarv, bd=0)
    Vahe.grid(row=rida, column=veerg, padx=0, pady=0)


def createBoard():
    leftBoardStartCol = 1
    rightBoardStartCol = boardWidth + 2
    createSpace(1, 0)
    # vasakpoolne mänguväli
    # sinna paigutad alguses oma laevad
    # praegune loogika: kõigepealt viiene laev, siis neljane, kolmene, kahene
    for i in range(boardWidth):
        for j in range(boardWidth):
            button = Button(root, font="Times 13", height=1, width=3, bg = boardButton)
            button.grid(row=j + 1, column=i + leftBoardStartCol, padx=0, pady=0)
            button.configure(command=lambda i=i, j=j: pressButtonLeft(j, i))
            buttonsLeft[(j, i)] = button

    createSpace(1, leftBoardStartCol + boardWidth)

    # parempoolne mänguväli, sealt hakkad vastase laevu otsima hiljem
    for i in range(boardWidth):
        for j in range(boardWidth):
            button = Button(root, font="Times 13", height=1, width=3, bg = boardButton)
            button.grid(row=j + 1, column=i + rightBoardStartCol, padx=0, pady=0)
            button.configure(command=lambda i=i, j=j: pressButtonRight(j, i), state='disabled')
            buttonsRight[(j, i)] = button

    createSpace(1, rightBoardStartCol + boardWidth)

    # print(buttonsLeft) # Debug
from random import randint

def randomise():
    global player6, player5, player4, player3, player2
    boats = 6
    while(boats >= 2):
        randomX = randint(0, 9)
        randomY = randint(0, 9)
        direction = randint(1, 4)
        zeroPoint = (randomX, randomY)
        #if not zeroPoint in playerAllBoatsCoordinates:
        #    if (direction == 1):
        #        print("")

def pressButtonLeft(row, col):
    global player6, player5, player4, player3, player2
    button = buttonsLeft[(row, col)]  # see nupp mida vajutati

    if button['text'] == "" and (row, col) not in forbiddenButtonsForBoats:  # kui nuppu veel ei ole ära märgistatud
        button.configure(text="O", bg="black")
        current.append((row, col))
    elif button['text'] == "O" and (row, col) not in playerAllBoatsCoordinates:
        # kui on märgistatud aga veel ei kuulu laevale -> siis lubame muuta (kui kuulub juba laevale, ei lase enam muuta) võib hiljem edasi arendada
        button.configure(text="", bg= boardButton)
        current.remove((row, col))

    if len(player6) == 0 and isBoat(6):
        # kõigepelt viiene laev (ja viiest laeva veel ei ole)
        mangijaTeade.configure(text='Position your ship of length 5. ')
        for b in current:
            buttonsLeft[b].configure(background = color2)  # märgistab nupud teise värviliseks
        player6 = copy.deepcopy(current)  # salvestab laeva punktid
        for e in player6:
            playerAllBoatsCoordinates.append(e)
        current.clear()

    if len(player6) != 0 and len(player5) == 0 and isBoat(5):
        # kõigepelt viiene laev (ja viiest laeva veel ei ole)
        mangijaTeade.configure(text='Position your ship of length 4. ')
        for b in current:
            buttonsLeft[b].configure(background = color2)  # märgistab nupud teise värviliseks
        player5 = copy.deepcopy(current)  # salvestab laeva punktid
        for e in player5:
            playerAllBoatsCoordinates.append(e)
        current.clear()
    elif len(player6) != 0 and len(player5) != 0 and len(player4) == 0 and isBoat(4):
        # siis neljane laev (eeldusel, et viiene on juba olemas)
        mangijaTeade.configure(text='Position your ship of length 3. ')
        for b in current:
            buttonsLeft[b].configure(background = color2)
        player4 = copy.deepcopy(current)
        for e in player4:
            playerAllBoatsCoordinates.append(e)
        current.clear()
    elif len(player6) != 0 and len(player5) != 0 and len(player4) != 0 and len(player3) == 0 and isBoat(3):
        mangijaTeade.configure(text='Position your ship of length 2. ')
        for b in current:
            buttonsLeft[b].configure(background = color2)
        player3 = copy.deepcopy(current)
        for e in player3:
            playerAllBoatsCoordinates.append(e)
        current.clear()
    elif len(player6) != 0 and len(player5) != 0 and len(player4) != 0 and len(player3) != 0 and len(player2) == 0 and isBoat(2):
        for b in current:
            buttonsLeft[b].configure(background = color2)
        player2 = copy.deepcopy(current)
        for e in player2:
            playerAllBoatsCoordinates.append(e)
        current.clear()

        allBoatsAreChosen_EnableBombingMode()
    updateForbiddenButtonsForPlayer()


def updateForbiddenButtonsForPlayer():
    global playerAllBoatsCoordinates, forbiddenButtonsForBoats
    for elem in playerAllBoatsCoordinates:
        surroundingButtons = []
        zeroPoint = (elem[0] - 1, elem[1] - 1)
        for y in range(3):
            for x in range(3):
                point = (zeroPoint[0] + y, zeroPoint[1] + x)
                surroundingButtons.append(point)
                if not point in forbiddenButtonsForBoats:
                    if point in buttonsLeft:
                        forbiddenButtonsForBoats.append(point)
                        buttonsLeft[point].configure(state='disabled')


def allBoatsAreChosen_EnableBombingMode():
    global playerBoats, playerAllBoatsCoordinates
    if len(player6) != 0 and len(player5) != 0 and len(player4) != 0 and len(player3) != 0 and len(player2) != 0:
        mangijaTeade.configure(text=' ')
        print("All set!")
        playerBoats = [player6, player5, player4, player3, player2]
    for b in buttonsLeft:
        buttonsLeft[b].configure(state='disabled')  # vasakpoolsele mänguväljale ei saa enam klikkida
        teade.configure(text='Bombs away!')
    for e in buttonsRight:
        buttonsRight[e].configure(state='normal')  # lubame klikkimise parempoolsel mänguväljal
    for e in playerBoats:
        playerSunkedBoats[str(e)] = False


def isBoat(length):
    global current
    x_id = set()
    y_id = set()
    for e in current:
        x_id.add(e[0])
        y_id.add(e[1])
    if len(x_id) == 1:  # kõikide x'ide koordinaadid on võrdsed
        min, max = getMaxMin(y_id)
        if max - min == (length - 1) and len(y_id) == length:  # nupud on järjest ja õige pikkusega
            return True
    elif len(y_id) == 1:  # kõikide y'ite koordinaadid on võrdsed
        min, max = getMaxMin(x_id)
        if max - min == (length - 1) and len(x_id) == length:  # nupud on järjest ja õige pikkusega
            return True


def getMaxMin(list):  # leiab listist maximumi ja minimumi
    min = 10
    max = -1
    for el in list:
        if int(el) < min:
            min = el
        if int(el) > max:
            max = el
    return min, max


def pressButtonRight(row, col):
    if (row, col) not in playerGuesses:  # ei ole sinna kasti veel klikitud
        playerGuesses.append((row, col))
        # Lisame mängija pakkumise kaalutud väärtustega pakkumiste sõnastikku
        global guessCounter, allGuesses
        if ((row, col) not in allGuesses):
            allGuesses[(row, col)] = 0
        allGuesses[(row, col)] += guessWeights[guessCounter]
        guessCounter += 1
        # print(allGuesses) # Debug

        if (row, col) in AIAllBoatsCoordinates:
            global playerHitGuesses
            playerHitGuesses.append((row, col))  # Koordinaadi lisamine mängija jooksvate pihta saamiste hulka
            # print('playerHitGuesses:', playerHitGuesses) # Debug
            buttonsRight[(row, col)].configure(text="X")
            buttonsRight[(row, col)].configure(background = color6)  # Pihta läinud ruut saab teise tooni
            aiTeade.configure(text="HIT!")  # Teavitus
            checkDidBoatSunk()
            checkIfGameOver()
            # Kuna mängija sai AI laevale pihta, siis saab mängija uuesti pakkuda
        else:
            buttonsRight[(row, col)].configure(text="O")
            buttonsRight[(row, col)].configure(background = color1)  # Mööda läinud ruut värvitakse valgeks
            aiTeade.configure(text="MISS!")  # Teavitus
            # AI saab pakkuda ainult siis kui mängija pakkus mööda
            # checkIfGameOver()
            doAIMove()
        # Enne järgmist käiku kontrollime, kas mäng on läbi
        # checkIfGameOver() # Põhjustab AI võidu puhul topeltlõpetamise (sh. duubelread result.txt failis)???


def checkDidBoatSunk():
    for paat in AIBoats:
        if all(x in playerHitGuesses for x in paat):
            # kogu paat põhjas -> värvime ära
            for b in paat:
                buttonsRight[b].configure(background = color3)
            AISunkedBoats[str(paat)] = True  # lisame uppunud laevade listi
            # Jooksvate pihtasaamiste kustutamine
            global playerHitGuesses
            playerHitGuesses.clear()
            aiTeade.configure(text="DOWN YOU GO!")


def doAIMove():
    global AIGuesses, AIHitGuesses
    if len(AIHitGuesses) == 0:
        move = AIMove(coordinateFreqDict)
    else:
        move = AIPickNext(AIHitGuesses[-1], coordinateFreqDict)
    # print('Move: ', move) # Debug
    # print('AIHits: ', AIHitGuesses) # Debug
    AIGuesses.add(move)
    if move in playerAllBoatsCoordinates:
        buttonsLeft[move].configure(text="X")  # AI sai paadile pihta
        buttonsLeft[move].configure(background = color5)
        # Lisame pihta saanud koordinaadi tabamuste hulka
        AIHitGuesses.append(move)
        boatIsSunk = checkDidAIManageToSinkABoat()
        # Kontrollime, kas mäng on läbi
        checkIfGameOver()
        # AI saab uuesti pakkuda ja vastase pakkumiskord jääb vahele
        # Kui paat on põhjas, siis tühjendame edukad pakkumised ja valime järgmise populaarseima asukoha mänguväljalt
        if (boatIsSunk):
            AIHitGuesses.clear()
        doAIMove()
    else:
        buttonsLeft[move].configure(text="-")  # AI pani mööda
        buttonsLeft[move].configure(background = color1)  # Mööda läinud ruut värvitakse valgeks


# Pakutava koordinaadi juhuslik valimine
def pickMoveRandom():
    voimalikud = []
    for e in buttonsLeft.keys():
        if e not in AIGuesses:
            voimalikud.append(e)
    return random.choice(voimalikud)


def checkDidAIManageToSinkABoat():
    for paat in playerBoats:
        if all(x in AIHitGuesses for x in paat):
            # kogu paat põhjas -> värvime ära
            for b in paat:
                buttonsLeft[b].configure(background = color4)
            playerSunkedBoats[str(paat)] = True  # lisame uppunud laevade listi
            # Lisame laeva ümbruses olevad nupud AI pakkumiste hulka, sest seal ei saa enam laevu olla
            global AIGuesses
            forbidden = getForbiddenButtonsForAI(paat)
            for coord in forbidden:
                AIGuesses.add(coord)
            return True
    return False


def checkIfGameOver():
    if playerWon():
        displayWin()
    elif playerLost():
        displayLoss()

def save(result):
    # statistika jaoks
    endOfGame(result)

def displayLoss():
    teade.configure(text="You lost...")
    for b in buttonsRight:
        buttonsRight[b].configure(state='disabled')
    save('AIwon')

def displayWin():
    teade.configure(text="Congratulations, you won!")
    for b in buttonsRight:
        buttonsRight[b].configure(state='disabled')
    save('AIlost')

def playerWon():
    all(x == True for x in AISunkedBoats.values())

def playerLost():
    return all(x == True for x in playerSunkedBoats.values())

def endOfGame(result):
    addPlayerBoats()
    saveCoordinateFreqDict()
    saveGuessesDict()


# AI laevad: ruudud, mida kõige "viimastena" on pakutud. Selle jaoks tuleb varem mängija pakkumised sõnastikku salvestada,
# kus hilisemad pakkumised saavad suuremad väärtused.
# Alguspunkt kõige vähem pakutule ja siis vaatab edasi, et missugune ruut vasakult, paremalt, ülevalt või alt on järgmisena vähimalt pakutud.
def defineAIBoats():
    global AI2, AI3, AI4, AI5, AI6, AIBoats, AISunkedBoats

    AI6 = generateBoat(6)
    AI5 = generateBoat(5)
    AI4 = generateBoat(4)
    AI3 = generateBoat(3)
    AI2 = generateBoat(2)
    AIBoats = [AI6, AI5, AI4, AI3, AI2]

    for e in AIBoats:
        AISunkedBoats[str(e)] = False
        print(e)  # Debug


def generateBoat(length):
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
            print('Cannot build a ship of , length', length, boat)  # Debug
            return generateBoat(length)  # Püüab uuesti laeva luua
        else:
            progress_counter_prev = copy.copy(progress_counter)
    for elem in boat:
        AIAllBoatsCoordinates.append(elem)
    return boat


def findSurroundingButtons(boat):
    surrounding = []
    for coordinate in boat:
        surroundingThatButton = surroundingButtonsGen(coordinate)
        for button in surroundingThatButton:
            if button not in surrounding and button not in boat:
                surrounding.append(button)
    return surrounding


def surroundingButtonsGen(elem):
    global buttonsRight
    list = [(elem[0] - 1, elem[1]), (elem[0] + 1, elem[1]),
            (elem[0], elem[1] - 1), (elem[0], elem[1] + 1)]
    result = []
    for e in list:
        if e in buttonsRight:
            result.append(e)
    return result


def getForbiddenButtonsForAI(lst):
    result = []
    for elem in lst:
        surroundingButtons = [(elem[0] - 1, elem[1]), (elem[0] + 1, elem[1]),
                              (elem[0], elem[1] - 1), (elem[0], elem[1] + 1),
                              (elem[0] - 1, elem[1] - 1), (elem[0] + 1, elem[1] + 1),
                              (elem[0] + 1, elem[1] - 1), (elem[0] - 1, elem[1] + 1)]
        for surrounding in surroundingButtons:
            if not surrounding in result:
                if surrounding in buttonsLeft:
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
        if (coord in buttonsLeft and coord not in AIGuesses):
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
    # print(coordinateFreqDict) #Debug


def saveCoordinateFreqDict():
    global coordinateFreqDict
    pickle.dump(coordinateFreqDict, open("playerBoatsCoordFrequencyDictFile.p", "wb"),
                protocol=pickle.HIGHEST_PROTOCOL)
    # print(coordinateFreqDict)


def saveGuessesDict():
    global allGuesses
    pickle.dump(allGuesses, open("playerGuessesFrequencyDictFile.p", "wb"),
                protocol=pickle.HIGHEST_PROTOCOL)
    # print(allGuesses)


def start(state):
    global playerAllBoatsCoordinates, player6, player5, player4, player3, player2, playerBoats, playerSunkedBoats, forbiddenButtonsForBoats
    forbiddenButtonsForBoats = []
    playerAllBoatsCoordinates = []
    player6 = {}
    player5 = {}
    player4 = {}
    player3 = {}
    player2 = {}
    playerBoats = []
    playerSunkedBoats = {}

    global AIAllBoatsCoordinates, AISunkedBoats, playerGuesses, playerHitGuesses, guessCounter, AIGuesses, AIHitGuesses

    AIAllBoatsCoordinates = []
    AISunkedBoats = {}
    playerGuesses = []
    playerHitGuesses = []
    guessCounter = 0
    AIGuesses = set()
    AIHitGuesses = []

    global allGuesses, coordinateFreqDict
    # AI jaoks andmete sisse lugemine
    allGuesses = readGuessesDict()
    coordinateFreqDict = readCoordinateFreqDict()

    createBoard()
    defineAIBoats()

    teade.configure(text="Place your ships on the board!")
    mangijaTeade.configure(text='Position a ship of length 6. ')
    aiTeade.configure(text=" ")

def createFiles():
    # Loome AI jaoks vajalikud failid
    if not os.path.isfile("playerBoatsCoordFrequencyDictFile.p"):  # fails don't exist yet -> inizialize
        d = {}
        for i in range(boardWidth):
            for j in range(boardWidth):
                d[(j, i)] = 0
        pickle.dump(d, open("playerBoatsCoordFrequencyDictFile.p", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(d, open("playerGuessesFrequencyDictFile.p", "wb"), protocol=pickle.HIGHEST_PROTOCOL)

def setColors():
    # Määrame värvid
    global color1, color2, color3, color4, color5, color6, boardButton
    color1 = 'White'
    color2 = 'gray28'
    color3 = 'RoyalBlue2'
    color4 = 'red3'
    color5 = 'PaleGreen3'
    color6 = 'gray'
    boardButton = 'cornflower blue'

# Kaalud mängija poolt pakutavate ruutude jaoks. Mida hiljem mängija ruudu mängulaualt valib, seda suurema väärtuse saab.
def createWeights():
    weights = []
    start = 0.1
    step = 0.1
    for i in range(100):
        weights.append(start)
        start += step
    return weights

def main():

    #listide loomine
    global boardWidth, buttonsLeft, buttonsRight, current
    boardWidth = 10
    buttonsLeft = {}
    buttonsRight = {}
    current = []  # viimased, mis mängija poolt valitud (saavad laeva punktideks, aga veel ei ole)

    # Väärtuste listi loomine hilisemaks mängija pakkumiste loendamiseks
    global guessWeights
    guessWeights = createWeights()

    # Akna loomine
    global root, teade, mangijaTeade, aiTeade
    root = Tk()
    root.wm_title("Battleships")
    root.resizable(0, 0)

    minuLaevad = Label(root, text="Your ships", font="Times 15 bold").grid(row=0, column=1, padx=10, pady=8,
                                                                               columnspan=10)
    vastaseLaevad = Label(root, text="Enemy ships", font="Times 15 bold").grid(row=0, column=12, padx=10, pady=8,
                                                                                   columnspan=10)
    teade = Label(root, text="Place your ships on the board.", font="Times 13 bold")
    teade.grid(row=12, column=1, padx=10, pady=8, columnspan=21)

    mangijaTeade = Label(root, text='Position a ship of length 5.', font="Times 13 bold")
    mangijaTeade.grid(row=11, column=1, padx=10, pady=8, columnspan=10)

    aiTeade = Label(root, text=" ", font="Times 13 bold")
    aiTeade.grid(row=11, column=12, padx=10, pady=8, columnspan=10)

    loppNupp = Button(root, text="Restart", command=lambda: start(False))
    loppNupp.grid(row=13, column=12, padx=10, pady=8, columnspan=3)

    loppNupp = Button(root, text="Randomise", command=lambda: start(True))
    loppNupp.grid(row=13, column=8, padx=10, pady=8, columnspan=3)

    start(False)
    root.mainloop()


createFiles()
setColors()
main()
