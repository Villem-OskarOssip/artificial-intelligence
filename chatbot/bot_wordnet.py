#!/usr/bin/env python
# coding: utf-8

import random
import urllib.request
import json
import re
	
# Roboti kirjeldus, kasutuspiirangud ===================================
"""
Robot tagastab Eesti Wordneti API põhjal otsitava mõiste definitsioone, 
näitelauseid ja sellele lähedasi sõnu. 
Ühtlasi kasutab robot lemmatiseerijat http://prog.keeleressursid.ee/ws_etmrf/lemma.php, et 
tunda lauses ära ka käändes sõnu ja osata nii ära tunda vajalikke võtmesõnu. 
Küsitava sõna ees peab olema kindlasti sõna "sõna" või "mõiste", nii leitakse üles 
küsitav mõiste. Kuna sõna võib leiduda mitmes tähenduses, antakse nii seletusi, 
näitelauseid kui ka lähedasi sõnu kõigist neist.
"""
# ======================================================================

BotWebservice = "http://estwn-test.keeleressursid.ee/docs/#!/api/"

# Positiivsed testlaused (laused, mille puhul peab dialoogsüsteem tagastama mõistliku vastuse just sellelt robotilt)
sentencesPos = [
	"Milline on mõiste koer sünonüüm?", 
	"Anna näitelause sõnaga lammas.", 
	"Mida tähendab sõna laud?", 
	"Mis on lähedane sõnale klass?", 
	"Defineeri sõna uks."
]

def getResponse(text, initiative):
	confidenceValue = 0
	response = "Wordneti juturoboti vastus"
	initiative = False
	text = text.lower()
	text = re.sub("[^A-ZÕÄÖÜŠŽa-zõäöüšž ]", "", text)
	keywords = ["näitelause", "näidislause", "definitsioon", "defineeri", "tähendus", "tähenda", "sünonüüm", "samatähenduslik", "läheda"]
	keywords1 = ["sõna", "mõiste"]
	if any(w in text for w in keywords) and any(w in text for w in keywords1):
		confidenceValue = 0.9
		textsplit = text.split()
		lemmas = []
		word = -1
		for word in textsplit:
			file = urllib.request.urlopen('http://prog.keeleressursid.ee/ws_etmrf/lemma.php?s=' + urllib.parse.quote(word))
			analyys = json.loads(file.read().decode())
			lemma = analyys['root']
			lemmas.append(lemma)
		for i in range(len(lemmas)):
			if lemmas[i] == "sõna" or lemmas[i] == "mõiste":
				word = lemmas[i+1]
				break
		url = 'http://estwn-test.keeleressursid.ee/api/v1/synset/?format=json&word=' + urllib.parse.quote(word);
		file = urllib.request.urlopen(url)
		data = json.loads(file.read().decode())
		definitions = []
		examples = []
		synonyms = []
		for r in data["results"]:
			for s in r["senses"]:
				if s["primary_definition"] != "" and s["primary_definition"] not in definitions:
					definitions.append(s["primary_definition"])
				if s["primary_example"] != "" and s["primary_example"] not in examples:
					examples.append(s["primary_example"])
				if s["lexical_entry"]["lemma"] != "" and s["lexical_entry"]["lemma"] not in synonyms and s["lexical_entry"]["lemma"] != word:
					synonyms.append(s["lexical_entry"]["lemma"])
		# Lähedased sõnad
		if ("sünonüüm" in text or "samatähenduslik" in text or "läheda" in text):
			response = 'Sõnale "' + word + '" lähedane sõna'
			if len(synonyms) > 0:
				response += ' on "' + random.choice(synonyms) + '". Kokku leiti '+ str(len(synonyms)) + ' sünonüüm'
				if len(synonyms) > 1: 
					response += 'i.'
				else:
					response += '.'
			else:
				response += ' Wordnetis puudub.'
		# Definitsioonid
		elif ("definitsioon" in text or "defineeri" in text or "tähendus" in text or "tähenda" in text):
			response = 'Mõiste "' + word + '" definitsioon Wordnetis'
			if len(examples) > 0:
				response += ' on "' + random.choice(definitions) + '".'
			else:
				response += ' puudub.'
		# Näidislaused
		elif ("näitelause" in text or "näidislause" in text):
			response = 'Näitelause mõiste "' + word + '" jaoks Wordnetis'
			if len(examples) > 0:
				response += ' on "' + random.choice(examples) + '". Kokku leiti '+ str(len(examples)) + ' lause'
				if len(examples) > 1: 
					response += 't.'
				else:
					response += '.'
			else:
				response += ' puuduvad.'
	return confidenceValue, response, initiative
