#!/usr/bin/env python
# coding: utf-8

# LTAT.01.003 Tehisintellekt I (2018 sügis)
# Koduülesanne 4. Gomoku

# Käsureaga kasutajaliides
# Fail, mida koduse töö esitamisel EI SAADETA

import gomoku_ai
import numpy as np
import random
import tkinter as tk
from tkinter import *

# Muutujate algväärtustamine ========================================================================================

# Mängulaua suurus
boardSize = 15
#board = [np.zeros(boardSize,dtype=int) for i in range(boardSize)]
board = [[0]*boardSize for i in range(boardSize)]

players = [".","X","O"] # Mängijad
playerColours = ["gray75","black","white"] # Värvid aknas
plNames = ["..","must","valge"] # Väljatrükiks
player = 1 # Käiku tegev mängija (alustab 1 ehk must)

# Tehisintellekti vastu mängimine (True või False)
#playAI = True
playAI = True
# Kas AI mängib mustade (1) või valgete (2) nuppudega (alati alustavad mustad)
AIPlayer = 1


# Funktsioonid ======================================================================================================

# Kontrollib, kas sinna võib käia
def legalMove(move):
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
        x = boardSize-len(gomoku)+1 #milliseid diagonaale kontrollida
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

# Väärtusta mänguruudustik	
def drawBoard():
	# Joonista algne mängulaud välja
	for row in range(boardSize):
		for col in range(boardSize):
			#bttext = tk.StringVar()
			#bttext.set("%s,%s" % (row, col))
			#text = "%s,%s" % (row, col)
			button = tk.Button(root, text="%s,%s" % (row, col), bg=playerColours[board[row][col]])
			button.configure(command=lambda row=row, col=col: click(row, col))
			button.grid(row=row, column=col, sticky="nsew")
			ruudud[(row,col)] = button

			
# GUI: Käidi kuhugi asjalikku kohta.
# Tee käik, värvi vastav ruut ära
# ja kui vaja, lase AIl vastukäik teha.
def click(row, col):
    global board, player, ruudud
    button = ruudud[(row,col)]
    # Abitekst
    message.configure(text="Käik (%s, %s). Järgmisena käib %s." % (row, col,plNames[3-player]))
    move = (row, col)
    if not legalMove(move):
        message.configure(text="See ruut on juba võetud")
        return
	# Tee käik
    board[row][col] = player
	# Muuda vastava ruudu peal olev tekst ja nupu värv
    button.configure(text=players[player], bg=playerColours[player])
    # Kontrolli, kas mäng on läbi
    end, winner = isEnd()
    if end:
        if winner == 0:
            message.configure(text="Mäng lõppes viigiga.")
        else:
            message.configure(text="Gomoku! Võitis " + plNames[winner] + ".")
        #Mängutsükkel läbi
		# Muuda nupud mitteklikitavaks
        for key in ruudud:
            ruudud[key].config(state=DISABLED)
    player = 3-player
    #Kui arvuti käib järgmisena
    if not end and playAI and player == AIPlayer:
        row, col = gomoku_ai.getTurn(board,AIPlayer)
	    # TESTIMISEKS
        #row, col = getTurnRandom(board)
        board[row][col] = player
        message.configure(text="%s käik (%s, %s). Järgmisena käib %s." % (plNames[player],row, col,plNames[3-player]))
        button = ruudud[(row,col)]
        button.configure(text=players[player], bg=playerColours[player])
		# Kontrolli, kas mäng on läbi
        end, winner = isEnd()
        if end:
            if winner == 0:
                message.configure(text="Mäng lõppes viigiga.")
            else:
                message.configure(text="Gomoku! Võitis " + plNames[winner] + ".")
            #Mängutsükkel läbi
		    # Muuda nupud mitteklikitavaks
            for key in ruudud:
                ruudud[key].config(state=DISABLED)
        player = 3-player

    
# GUI värvivalik
def valiv2rv():
    global init_choice
    #init_choice = IntVar()
    #init_choice.set(0)
    win = tk.Toplevel()
    win.wm_title("SWAP")

    l = tk.Label(win, text="Vali, mis värviga soovid jätkata")
    l.grid(row=0, column=0)

    #valge = ttk.Button(win, text="valge", command=lambda w=win: kasutajav2rv(2,w))
    valge = tk.Radiobutton(win, text="Valge", variable=init_choice, value=2, indicatoron=0, command = win.destroy)
    valge.grid(row=1, column=0)
    #must = ttk.Button(win, text="must", command=win.destroy)
    must = tk.Radiobutton(win, text="Must", variable=init_choice, value=1, indicatoron=0, command = win.destroy)
    must.grid(row=2, column=0)
	#Tõsta aknad nähtavale
    root.lift()
    win.lift()
	
# Algus
def initialize():
    global board, init_choice, AIPlayer, player
    board = [np.zeros(boardSize,dtype=int) for i in range(boardSize)]
    drawBoard()
    # 1. must nupp
    player = 1
    move = getTurnRandom(board)
    board[move[0]][move[1]] = 1
    click(move[0],move[1])
    # 1. valge nupp
    player = 2
    move = getTurnRandom(board)
    board[move[0]][move[1]] = 2
    click(move[0],move[1])
    # 2. must nupp
    player = 1
    move = getTurnRandom(board)
    board[move[0]][move[1]] = 1
    click(move[0],move[1])

    #board[0][4] = 2
    #board[0][5] = 2
    #board[0][6] = 2
    player = 2
    # Joonista mängulaud, lase pool valida
    drawBoard() #vaatab, mis juhtub
    root.lower()
    valiv2rv()
	#oota väärtustamist
    root.wait_variable(init_choice)
    ch = init_choice.get()
    if ch == 1 & playAI:
        AIPlayer = 2
        move = gomoku_ai.getTurn(board,AIPlayer)
        # TESTIMISEKS
        #move = getTurnRandom(board)
        board[move[0]][move[1]] = 2
        click(move[0],move[1])
        drawBoard() #vaatab, mis juhtub
        # Järgmisena käib nüüd must
		# aga see vahetus peaks iseenesest toimuma
        player = 1

#======================================================================================================
#  GUI osa ehk akende joonistamine
#      ja mängu käimapanek

#Et hiljem saaks mängulaua ruute muuta
ruudud = {}
# GUI ehk akna joonistamine
root = tk.Tk()
root.title("Gomoku")
root.grid_rowconfigure(boardSize, weight=1)
root.grid_columnconfigure(boardSize, weight=1)	

# Teadete jagamiseks
message = tk.Label(root, text="")
message.grid(row=boardSize, column=0, columnspan=15, sticky="new")

# Mis värv on inimmängijal
init_choice = tk.IntVar()
init_choice.set(0)
# Kui SWAPis midagi ei valita, käib kolmanda käigu valge (inimene)
player = 2
# Algväärtustus, trükib ka mängulaua välja
# Kui SWAP, siis on järgmine käija must (inimene)
initialize()

# Näita välja
root.mainloop()