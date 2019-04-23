#!/usr/bin/env python
# coding: utf-8

# LTAT.01.003 Tehisintellekt I (2018 sügis)
# Koduülesanne 4. Gomoku

# Fail, mida võib muuta ja mis tuleb esitada koduse töö lahendusena
# Faili nime peaks jätma samaks
# Faili võib muuta suvaliselt, kuid see peab sisaldama funktsiooni getTurn(),
# millele antakse argumendina ette mängijat tähistav number (1 - must ehk X; 2 - valge ehk O) 
# ning mis tagastab selle mängija järgmise käigu koordinaatide tuple'ina (rida, veerg)
from copy import deepcopy

def getTurn(board, player):
    # Üks võimalikest käikudest
    # move = [7,7] #sobib ka, kusagil otseselt tuple'iks olekut ei kontrollita
    # Siia tuleb järgmise käigu genereerimise loogika, kasutada võib ka siia faili loodud funktsioone
    # Kui sügavale minimax vaatab
    #move = (7, 7)
    depth = 1
    helptext = False

    def getAllTurns(board):
        allTakenPlaces = []
        possibleMoves = []
        for i in range(15):
            for j in range(15):
                if board[i][j] == 1 or board[i][j] == 2:
                    allTakenPlaces.append((i, j))
        for i in range(len(allTakenPlaces)):
            takenPoint = allTakenPlaces[i]
            zeroPoint = (takenPoint[0]-1, takenPoint[1]-1)
            for y in range(3):
                for x in range(3):
                    point = (zeroPoint[0]+y,zeroPoint[1]+x)
                    if (point[0] >= 0) and (point[1] >= 0) and (point[0] < 15) and (point[1] < 15):
                        if (point not in allTakenPlaces) and (point not in possibleMoves):
                            possibleMoves.append(point)
        return possibleMoves

    def getTurnMinimax(depth):
        # Kui laua täitumiseni jäänud käikude arv = depth, lõpeta
        if len(getAllTurns(board)) < depth:
            depth = len(getAllTurns(board))
        turn, rate = minimax(board, depth, player)
        return turn

    def minimax(board, depth, givenPlayer):
        # player - momendil käigul olija, algoritmi väljakutsuja
        # move - variantide katsetamisel võimaliku käigu tegija
        depth -= 1
        bestturn = (-5, -5)
        bestrate = 0
        allPossibleTurns = getAllTurns(board)
        if depth >= 0 and len(allPossibleTurns) > depth:
            if player == givenPlayer:
                bestturn, bestrate = maximizer(board, allPossibleTurns, depth, givenPlayer)
            else:
                bestturn, bestrate = minimizer(board, allPossibleTurns, depth, givenPlayer)
        return bestturn, bestrate

    # Mängija käik, maksimeeri tulemust
    def maximizer(board, allturns, depth, givenPlayer):
        bestturn = (-1, -1)
        bestrate = 0
        type = ""
        # Kui pole veel soovitud sügavus saavutatud ning mängu lõpuni on veel piisavalt käike
        for turn in allturns:
            b = deepcopy(board)
            b[turn[0]][turn[1]] = givenPlayer
            if depth > 0:
                _turn, rate = minimax(b, depth, 3 - givenPlayer)
            else:
                rate, type = getRate(givenPlayer, b, turn)
            if rate > bestrate or (rate == bestrate and type == "e"):
                bestrate = rate
                bestturn = turn
        print("!===============!")
        print("Final turn: " + str(bestturn))
        print("Rate: " + str(bestrate))
        print("!===============!")

        return bestturn, bestrate

    # Vastasmängija käik, minimeeri meie kahjusid
    def minimizer(board, allturns, depth, givenPlayer):
        bestturn = (-1, -1)
        bestrate = 10
        type = ""
        for turn in allturns:
            b = deepcopy(board)
            b[turn[0]][turn[1]] = givenPlayer
            if depth > 0:
                _turn, rate = minimax(b, depth, 3 - givenPlayer)
            else:
                rate1, type = getRate(givenPlayer, b, turn)
                rate = 6 - rate1
            if helptext:
                print("Katse (min)", rate, depth)
            if rate < bestrate:
                bestrate = rate
                bestturn = turn
        return bestturn, bestrate

    def changeList(list,e):
        if len(list) < 5:
            list.append(e)
        else:
            for i in range(4):
                list[i] = list[i + 1]
            list[-1] = e
        return list

    def goOver(list, bestRate, e, player):
        result = 0
        if e == 3 - player:
            list = []
        elif len(list) == 5:
            for i in list:
                if i == player:
                    result += 1
            if result > bestRate:
                bestRate = result
        if e == player:
            list = changeList(list, e)
        else:
            list = changeList(list, e)
        return list, bestRate

    def goOverRows(player,board):
        list = []
        bestRate = 0
        for r in range(15):
            for c in range(15):
                position = board[r][c]
                list, bestRate = goOver(list, bestRate, position, player)
            list = []
        return bestRate

    def finalCheck(list, bestRate, player):
        result = 0
        if len(list) == 5:
            for i in list:
                if i == player:
                    result += 1
            if result > bestRate:
                bestRate = result
        return bestRate

    #pareamlt vasakule
    def goOverDiagonals(player,board):
        list = []
        bestRate = 0
        column1 = 4
        row = 1
        diagonal1 = 5
        diagonal2 = 14
        for f in range(11):
            for g in range(diagonal1):
                position = board[0 + g][column1 - g]
                list, bestRate = goOver(list, bestRate, position, player)
            bestRate = finalCheck(list, bestRate, player)
            column1 += 1
            diagonal1 += 1
            list = []
        for h in range(11):
            for j in range(diagonal2):
                position = board[row + j][0 - j]
                list, bestRate = goOver(list, bestRate, position, player)
            bestRate = finalCheck(list, bestRate, player)
            diagonal2 -= 1
            row += 1
            list = []
        return bestRate

    # vasakult paremale
    def goOverDiagonals2(player,board):
        list = []
        bestRate = 0
        column1 = 10
        row = 1
        diagonal1 = 5
        diagonal2 = 14
        for f in range(11):
            for g in range(diagonal1):
                position = board[0 + g][column1 + g]
                list, bestRate = goOver(list, bestRate, position, player)
            bestRate = finalCheck(list, bestRate, player)
            column1 -= 1
            diagonal1 += 1
            list = []
        for h in range(11):
            for j in range(diagonal2):
                position = board[row + j][0 + j]
                list, bestRate = goOver(list, bestRate, position, player)
            bestRate = finalCheck(list, bestRate, player)
            diagonal2 -= 1
            row += 1
            list = []
        return bestRate

    def goOverColumns(player,board):
        list = []
        bestRate = 0
        for c in range(15):
            for r in range(15):
                position = board[r][c]
                list, bestRate = goOver(list, bestRate, position, player)
            list = []
        return bestRate

    def getRate(player, board, turn):
        resultsFriendly = []
        resultsEnemy = []
        result = goOverRows(player, board)
        resultsFriendly.append(result)
        result2 = goOverColumns(player, board)
        resultsFriendly.append(result2)
        result3 = goOverDiagonals(player, board)
        resultsFriendly.append(result3)
        result4 = goOverDiagonals2(player, board)
        resultsFriendly.append(result4)

        board[turn[0]][turn[1]] = 3 - player
        resultEnemy1 = goOverRows(3 - player, board)
        resultsEnemy.append(resultEnemy1)
        resultEnemy2 = goOverColumns(3 - player, board)
        resultsEnemy.append(resultEnemy2)
        resultEnemy3 = goOverDiagonals(3 - player, board)
        resultsEnemy.append(resultEnemy3)
        resultEnemy4 = goOverDiagonals2(3 - player, board)
        resultsEnemy.append(resultEnemy4)

        print("Turn: " + str(turn))
        print("Friendly moves: ")
        print("Row: " + str(result))
        print("Column: " + str(result2))
        print("Diagonal (R->L): " + str(result3))
        print("Diagonal (L->R): " + str(result4))
        print("+++++++++++++++++++")
        print("Move result for enemy: ")
        print("Row: " + str(resultEnemy1))
        print("Column: " + str(resultEnemy2))
        print("Diagonal (R->L): " + str(resultEnemy3))
        print("Diagonal (L->R): " + str(resultEnemy4))

        enemyBest = max(resultsEnemy)
        friendlyBest = max(resultsFriendly)
        if friendlyBest > enemyBest:
            move = friendlyBest
            type = "f"
        else:
            move = enemyBest
            type = "e"
        print("--------------------")
        print("Best rate: " + str(move))
        print("---------------")

        return move, type

    def checkCombination(row, board):
        row = sorted(row)
        if row in [sorted(list(i)) for i in board] or \
                        row in [sorted(list(i)) for i in zip(*board)] or \
                        row == sorted([board[i][i] for i in range(15)]) or \
                        row == sorted([board[2 - i][i] for i in range(2, -1, -1)]):
            return True
        return False

    return getTurnMinimax(depth)
