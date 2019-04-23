#!/usr/bin/env python
# coding: utf-8

import random

# Roboti kirjeldus, kasutuspiirangud ===================================
"""
[TODO]
"""
# ======================================================================

BotWebservice = "[AADRESS]"

# Positiivsed testlaused (laused, mille puhul peab dialoogsüsteem tagastama mõistliku vastuse just sellelt robotilt)
sentencesPos = [
	"[LAUSE 1]", 
	"[LAUSE 2]", 
	"[LAUSE 3]", 
	"[LAUSE 4]", 
	"[LAUSE 5]"
]

def getResponse(text, initiative):
    confidenceValue = 0
    response = "Esimese roboti vastus"
    confidenceValue = random.uniform(0, 1)
    #initiative = True
    return confidenceValue, response, initiative
