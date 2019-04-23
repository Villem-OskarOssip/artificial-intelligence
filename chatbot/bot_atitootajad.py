#!/usr/bin/env python
# coding: utf-8

import urllib.request
import lxml.html
import re

# Roboti kirjeldus, kasutuspiirangud ===================================
"""
Robot annab infot TÜ ATI töötajate kohta (nimi, töökoht, haridus, telefon, aadress, e-posti aadress). 
Laused peavad algama suure tähega, nimed peavad olema nimetavas käändes ja suure algustähega, pöördumisel peab kasutama sõnu ati,
instituu või arvutiteadus. Probleemideks on korduvate nimedega inimesed, sel juhul valitakse esimene sobiv. 
"""
# ======================================================================

BotWebservice = "https://www.cs.ut.ee/et/kontakt/arvutiteaduse-instituut"

# Positiivsed testlaused (laused, mille puhul peab dialoogsüsteem tagastama mõistliku vastuse just sellelt robotilt)
sentencesPos = [
	"Mis on instituudi töötaja Varmo Vene aadress?", 
	"Millist tööd teeb atis töötav Jaak Vilo?", 
	"Milline on instituudis töötava Mark Fišeli haridus?", 
	"Millise e-posti aadressil saan saata kirja ATI õppejõule Eno Tõnisson?", 
	"Kas ATI töötajal Liivi Luik on telefon?"
]

def parseHtml():
	response = urllib.request.urlopen('https://www.cs.ut.ee/et/kontakt/arvutiteaduse-instituut')
	content = response.read().decode('utf-8')
	content = re.sub('<br>\(', ' (', content) # Sisetelefoni numbrid
	content = re.sub('<br>(\d)', ' \\1', content) # Mitu telefoninumbrit
	content = re.sub('<br>', '|', content)
	content = re.sub('<span class="spamspan"><span class="u">', '', content)
	content = re.sub('</span> \[ät\] <span class="d">', '@', content)
	content = re.sub('</span></span>', '', content)

	tree = lxml.etree.HTML(content)
	contentp = tree.xpath("//div[contains(@class, 'view-display-id-block_3')]/div/div/div/table/tbody/tr")

	employees = []

	for el in contentp:
		children = list(el)
		name = el[0].text.strip()
		temp = el[1].text.strip()
		tempsplit = temp.split(",")
		job = temp
		education= ""
		if len(tempsplit) > 1 and not(re.search("\d", tempsplit[-1])):
			education = tempsplit[-1].strip()
			job = ','.join(tempsplit[0:-1])
		temp = el[2].text.strip()
		tempsplit = temp.split("|")
		phone = ""
		address = ""
		email = ""
		if re.match("^[0-9 \(\)]+$", tempsplit[0]):
			phone = tempsplit[0].strip()
			del(tempsplit[0])
		if re.match(".*@.*", tempsplit[-1]):
			email = tempsplit[-1].strip()
			del(tempsplit[-1])
		address = ','.join(tempsplit).strip()
		employees.append({"name": name, "job": job, "education": education, "phone": phone, "address": address, "email": email})

	#for e in employees:
	#	for keys, values in e.items():
	#		print(keys, values)
	#	print()
	return employees

def getResponse(text, initiative):
	confidenceValue = 0
	response = "ATI töötajate juturoboti vastus"
	initiative = False
	if "arvutiteadus" in text.lower() or "instituu" in text.lower() or "ati" in text.lower():
		confidenceValue = 0.6
		wordsCap = re.findall("[A-ZÕÄÖÜŠŽ][\S]+", text)
		if len(wordsCap) > 1: # Kui rohkem kui üks sõna lauses on suure algustähega,...
			# ... siis ehk on selleks teiseks suure algustähega sõnaks nimi
			employees = parseHtml()
			employee = ""
			for n in wordsCap[1:]:
				nameTemp = n
				for e in employees:
					if nameTemp in e["name"]:
						employee = e
						break
				if employee != "":
					break
			if employee != "":
				name = e["name"]
				if re.search("telefon|telefoninumber", text):
					if employee['phone'] != "":
						confidenceValue = 0.9
						response = "Töötaja " + name + " telefoninumber on " + employee['phone'] + "."
				elif re.search("amet|töötab|tööd", text):
					if employee['job'] != "":
						confidenceValue = 0.9
						response = "Töötaja " + name + " amet on " + employee['job'] + "."
				elif re.search("haridus|on õppinud", text):
					if employee['education'] != "":
						confidenceValue = 0.9
						response = "Töötaja " + name + " haridus on " + employee['education'] + "."
				elif re.search("e-post|epost", text):
					if employee['email'] != "":
						confidenceValue = 0.8
						response = "Töötaja " + name + " e-posti aadress on " + employee['email'] + "."
				elif re.search("aadress", text):
					if employee['address'] != "":
						confidenceValue = 0.8
						response = "Töötaja " + name + " aadress on " + employee['address'] + "."
				else:
					response = "Töötaja nimega " + nameTemp + " sobivaid andmeid ei leitud."
			else:
				response = "Töötajat nimega " + nameTemp + " ei leitud."
	return confidenceValue, response, initiative
