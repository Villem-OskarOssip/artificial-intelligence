#!/usr/bin/env python
# coding: utf-8

# LTAT.01.003 Tehisintellekt (2018 sügis)
# Kodutöö nr 5. Dialoogsüsteem

import random
# Vastuse genereerimine, kui lävendit ei ületa ükski vastus
import default


# Moodulite nimekiri (failinimed)
bots = ['bot_atitootajad', 'bot_wordnet', 'samplebot1', 'bot_ilm', 'bot_finance']

nrOfBots = len(bots)

modules = []
for b in bots:
    modules.append(__import__(b))

# Minimaalne kindlusmäära väärtus
threshold = 0.3
# Viimati valitud vastust pakkunud teenuse indeks
topic = -1
# Initsiatiivi haaranud teenuse indeks
initiative = -1

print("Arvuti: Tere, mina olen juturobot.")

while True:
    #Kasutajalt lausungi ootamine
    human = input("Kasutaja: ")
    # Programmi töö lõpetamine, kui kasutaja kirjutab "bye"
    if human == "bye":
        print("Arvuti: Dialoog on lõppenud.")
        break
    # Arvuti vastus lausele
    responses = []
    # Kui on haaratud initsiatiiv (initiative != -1),
    # siis esitada päring vaid initsiatiivi omavale teenusele
    if initiative > -1:
        response = modules[initiative].getResponse(human, True)
        responses.append((response[0], response[1], response[2], initiative))
    # Kui initsiatiivi pole haaratud või initsiatiivi haaranud teenus annab vastuse usaldusväärsusega 0,
    # esitada päring kõigile teenustele, initsiatiivi haaramine tühistatakse
    if len(responses) == 0 or response[0] == 0:
        responses = []
        initiative = -1
        for i in range(nrOfBots):
            response = modules[i].getResponse(human, initiative == i)
            responses.append((response[0], response[1], response[2], i))
        random.shuffle(responses)
        responses = sorted(responses, key=lambda x: x[0], reverse=True)
    #print(responses)
    # Maksimaalse kindlusmääraga vastuse valik 
    if responses[0][0] >= threshold:
        response = responses[0][1]
        if responses[0][2]:
            initiative = responses[0][3]
        topic = bots[responses[0][3]]
	# Vastus juhul, kui ükski robot piisava kindlusmääraga vastust ei tagastanud
    else:
        response = default.getResponse(human)
    # Vastuse esitamine
    print("Arvuti:", response)
