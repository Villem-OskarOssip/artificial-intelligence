#!/usr/bin/env python
# coding: utf-8

import random

responses = ["Vabandust, ma ei saanud aru.", "Palun küsige kuidagi teisiti."]

def getResponse(text):
    return random.choice(responses)
