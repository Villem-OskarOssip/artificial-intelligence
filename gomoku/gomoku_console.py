#!/usr/bin/env python
# coding: utf-8

# LTAT.01.003 Tehisintellekt I (2018 sügis)
# Koduülesanne 4. Gomoku

# Käsureaga kasutajaliides
# Fail, mida koduse töö esitamisel EI SAADETA

import gomoku_ai
import numpy as np
import random

# Muutujate algväärtustamine ========================================================================================

# Mängulaua suurus
boardSize = 15
board = [np.zeros(boardSize,dtype=int) for i in range(boardSize)]
# board = [[0]*boardSize for i in range(boardSize)]

players = [".","X","O"] # Mängijad
player = 1 # Käiku tegev mängija (alustab 1 ehk must)

# Tehisintellekti vastu mängimine (True või False)
playAI = True
# Kas AI mängib mustade (1) või valgete (2) nuppudega (alati alustavad mustad)
AIPlayer = 1

# Funktsioonid ======================================================================================================

# Mängulaua joonistamine     
def drawBoard():
    print(" ",end = "  ")
    for i in range(boardSize):
        if i<10:
            print(i, end = "  ")
        else:
            print(i, end=" ")
    print()
    for r, row in enumerate(board):
        if r<10:
            print(r, end = "  ")
        else:
            print(r, end=" ")
        for value in row:
            print(players[value], end="  ")
        print("\n")


# Kontrollib, kas sinna võib käia
def legalMove(move):
    if any([m not in range(0,boardSize) for m in move]):
        print("See käik jääb laualt välja")
        return False
    if board[move[0]][move[1]]==0:
        return True
    return False

# Tagastab mängija nupu võimalike käikude listi 
# Kui võimalikud käigud puuduvad, tagastab tühja listi
def getPossMoves(bd):
    possMoves = []
    for rownr, row in enumerate(bd):
        for colnr, value in enumerate(row):
            if value==0:
            #if legalMove((row,col)):
                possMoves.append((rownr,colnr))
    return possMoves    

# Suvaline käik kuhugi vabasse ruutu
def getTurnRandom(bd):
    # list võimalike käikudega
    allmoves = getPossMoves(bd)
    return random.choice(allmoves)
    
# Algus
def initialize():
    global board
    board = [np.zeros(boardSize,dtype=int) for i in range(boardSize)]
    # 1. must nupp
    move = getTurnRandom(board)
    board[move[0]][move[1]] = 1
    # 1. valge nupp
    move = getTurnRandom(board)
    board[move[0]][move[1]] = 2
    # 2. must nupp
    move = getTurnRandom(board)
    board[move[0]][move[1]] = 1
    # Joonista mängulaud, lase pool valida
    drawBoard()
    choice = input("Kumba mängijana jätkad? 1 = must (X), 2 = valge (O): ")
    choice = int(choice)
    while choice not in [1,2]:
        choice = input("Sisesta täisarv (1 või 2).\nKumba mängijana jätkad? 1 = must (X), 2 = valge (O): ")
        choice = int(choice)
    if choice == 1:
        AIPlayer = 2
        # EDASPIDI
        #move = getTurn(board,AIPlayer)
        move = getTurnRandom(board)
        board[move[0]][move[1]] = 2
        # Järgmisena käib nüüd must
        player = 1
        drawBoard()

# Kontrolli, kas reas on täpselt viis sama värvi nuppu järjest
# gomoku - 5 nupu järjend
# row - rida, milles seda otsitakse
def checkRow(gomoku, row):
    n = len(gomoku)
    # Eeldame, et kõik õiged väärtused
    #value = player
    value = gomoku[0]
    matches = [i for i in range(len(row)-n+1) if np.array_equal(gomoku,row[i:i+n])]
    # Viisik on olemas
    if len(matches)>0:
        # Kontrolli, ega tegu pole kuuikuga
        rokumoku = gomoku + [value]
        for match in matches:
            if (not np.array_equal(row[match-1:match+n],rokumoku)) \
			and (not np.array_equal(row[match:match+n+1],rokumoku)):
                return True
    return False
    
# Kontroll, kas mäng on lõppenud
def isEnd():
    answer = False
    winner = 0
    # Raske uskuda, aga mängulaud on täis
    if len(getPossMoves(board)) ==0:
        return True
    # Kellelgi on täpselt viis järjest ehk gomoku
    # Kontrolli seda mõlema mängija kohta
    # Eeldame, et mõlemad korraga ei saa gomokuni jõuda
    for pl in [1,2]:
        gomoku = [pl for i in range(5)]
        x = boardSize-len(gomoku)+1 #milliseid diagonaale kontrolida
        #read
        #veerud
        #langevad diagonaalid
        #tõusvad diagonaalid
        if any([checkRow(gomoku,row) for row in board]) or \
        any([checkRow(gomoku,row) for row in np.transpose(board)]) or \
        any([checkRow(gomoku,row) for row in [np.diagonal(board,i) for i in range(-x,x)]]) or \
        any([checkRow(gomoku,row) for row in [np.diagonal(np.fliplr(board),i) for i in range(-x,x)]]):
            answer = True
            winner = pl
    return answer, winner


#---------------------------------------------------------------------------

# Kui SWAPis midagi ei valita, käib kolmanda käigu valge (inimene)
player = 2
# Algväärtustus, trükib ka mängulaua välja
# Kui SWAP, siis on järgmine käija must (inimene)
initialize()
while True:
    print("Käib", players[player])
    # Korratakse seni, kuni kasutaja sisestab oma käigu koordinaadid
    while True:
        if playAI and player == AIPlayer:
            # Arvuti käik
		    # EDASPIDI
            #move = gomoku_ai.getTurn(board, player)
            move = getTurnRandom(board)
            #print(move)
        else:
            # Inimese käik
            move = input("Järgmine käik <rida> <veerg>: ")
            move = list(map(int, move.split()))
        if len(move)!=2 or not legalMove(move):
            print("Sisesta kaks täisarvu tühikuga eraldatult. Laua suurus on",boardSize)
            continue
        print(move)
        break
    # Tee käik
    board[move[0]][move[1]] = player
    drawBoard()
    #Mängija vahetub
    player = 3-player
    #Kas mäng on läbi?
    end, winner = isEnd()
    if end:
        if winner == 0:
            print("Mäng lõppes viigiga.")
        else:
            print("Gomoku! Võitis " + players[winner] + ".")
        #Mängutsükkel läbi
        break