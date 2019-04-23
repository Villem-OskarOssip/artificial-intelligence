import re
import urllib.request
import json

"""
Robot annab ilmainfot kõikide eesti linnade, alevike ja asulate kohta, küll aga praegu on probleem sellega,
et täpitähtedega kohanimed annavad encodingu vea ning sellest ma jagu ei saanud.
StackOverFlows pakutud ISO kood ei lahendanud probleemi.
Roboti ilusaks toimimiseks on vaja anda talle kohanimi ning vastavalt märksõna. (ilm, sooja, temperatuur, külma, vihm jne)
Robot oskab anda infot nii üldise ilma kohta kui ka selle kohta, kas sademeid on.  
Sademete küsimused peavad olema kas-küsimused, sest APIl on piiratud võimalused sademete kohta info kuvamiseks.
Näiteks: Kas Tartus homme lund sajab? 
Enim infot ilma kohta saab siis, kui küsimus sisaldab märksõna ilm. 
Näiteks: Mis ilm homme Tartus on?
"""

info = {}
info["city"] = ""       # mis linna kohta infot otsitakse
info["dataAsked"] = ""  # mida soovitakse teada saada
info["time"] = ""       # vaikeväärtus täna

APIKEY = '6d8047b5f829e312a2f42223b55cce92'

cities = set()

sentencesPos = [
    "Mis ilm homme Tartus on?",
    "Mis ilm täna Tallinnas on?",
    "Mis ilm ülehomme Narvas on?",
    "Kas praegu Tartus lund sajab?",
    "Kas praegu Tallinnas vihma sajab?",
    "Mis ilm täna Sauel on?",
    "Kas Tapal praegu sajab?"
]

# See meetod võtab info failist, mis sisaldab absoluutselt igat eesti linna, alevikku ja asumit
def addCities(cities):
    file = open("linnad.txt", encoding="UTF8")
    for city in file.readlines():
        cities.add(city.strip("\n").strip(" "))

addCities(cities)


def getResponse(text, initiative):

    # Kui tekstis leidub selliseid sõnu, siis jätkame ilmarobotiga
    if re.search("ilm|temperatuur|külm|soe|tuul|sooja|vihm|lund|lumi|sajab", text.lower()):
        return sisu(text, initiative)
    else:
        return 0, "Ilmarobot sellisele küsimusele vastata ei oska", 0

def sisu(text, initiative):
    # algväärtusta freimid
    reset()
    initiative = 1
    response = "Vabandust, ma ei saanud midagi aru :("
    # Kas meile anti mingi kindel kuupäev
    checkForDateTime(text)
    # Mis infot meilt sooviti
    checkForKeywords(text)
    # Mis linna kohta infot soovitakse
    checkForCity(text)

    # Kontrollin, kas sain piisavalt sisendeid. Kui ei ole, siis küsin lisainfot
    if info["city"] != "" and info["dataAsked"] != "":
        response = getResponseFromWeatherAPI()
    elif info["city"] == "" and info["dataAsked"] != "":
        response = "Ei saanud aru, mis linna kohta sa infot soovisid."
    elif info["city"] != "" and info["dataAsked"] == "":
        response = "Sa soovisid midagi teada " + info["city"] + " kohta. Aga mida täpsemalt?"


    # Kui kogu info on olemas
    return 1, response, initiative

# Tõlgib vastava päeva eestikeelse vastuse jaoks
def translateTime():
    if info["time"] == "tomorrow":
        return "homme"
    elif info["time"] == "dayAfterTomorrow":
        return "ülehomme"
    else:
        return "täna"


# Võtab APIst saadud vastuse ja annab edasi parserile.
def parseApiResponse(apiResponse):
    response = ""
    if info["dataAsked"] == "temp":
        response = parseTemperatureRequest(apiResponse)
    if info["dataAsked"] == "general":
        response = parseGeneralInfoRequest(apiResponse)
    if info["dataAsked"] == "rain":
        response = parseRainInfoRequest(apiResponse)
    if info["dataAsked"] == "snow":
        response = parseSnowInfoRequest(apiResponse)
    return response



# Kui tegu oli lumeinfo sooviga, siis see annab vastuse.
def parseSnowInfoRequest(apiResponse):
    if info["time"] == "today":
        if "snow" in apiResponse["weather"][0]["description"]:
            return "Jah, sajab."
        else:
            return "Ei saja."
    # hetkeinfo ja prognoosi apiresponsed on veidi erinevad ning seetõttu see eristus
    else:
        if "snow" in apiResponse:
            return "Jah, sajab."
        else:
            return "Ei saja."

# Kui tegu oli vihmainfo sooviga, siis see annab vastuse.
def parseRainInfoRequest(apiResponse):
    if info["time"] == "today":
        if "rain" in apiResponse["weather"][0]["description"]:
            return "Jah, sajab."
        else:
            return "Ei saja"
    # hetkeinfo ja prognoosi apiresponsed on veidi erinevad ning seetõttu see eristus
    else:
        if "rain" in apiResponse:
            return "Jah, sajab."
        else:
            return "Ei saja."

# Kui sooviti üldist ilma teada, siis see annab vastuse.
def parseGeneralInfoRequest(apiResponse):
    temp = round(apiResponse["main"]["temp"])
    humidity = round(apiResponse["main"]["humidity"])
    airpressure = round(apiResponse["main"]["pressure"])
    windspeed = round(apiResponse["wind"]["speed"])
    time = translateTime().capitalize()

    response = info["city"] + ". " + time + " on temperatuur " + str(temp) + " kraadi, " \
                "õhuniiskus on " + str(humidity) + "%, " \
                "õhurõhk on " + str(airpressure) + " mmHg, " \
                "tuule kiirus on " + str(windspeed) + " m/s."

    return response

# Kui sooviti temperatuuri teada mingis kohas, siis see annab vastuse.
def parseTemperatureRequest(apiResponse):
    temp = round(apiResponse["main"][info["dataAsked"]])
    response = info["city"] + ". "
    time = translateTime()
    response += "Temperatuur on " + time + " " + str(temp) + " kraadi."
    return response

# Ühendab ennast ilma APIga ning saab sealt vastava response, mis antakse edasi parserile.
def getResponseFromWeatherAPI():
    if info["time"] == "tomorrow":
        apiResponse = getDictFromJson('http://api.openweathermap.org/data/2.5/forecast?q='
                                      + info["city"] + '&units=metric&APPID=' + APIKEY)["list"][8]
    elif info["time"] == "dayAfterTomorrow":
        apiResponse = getDictFromJson('http://api.openweathermap.org/data/2.5/forecast?q='
                                      + info["city"] + '&units=metric&APPID=' + APIKEY)["list"][16]
    else:
        # järelikult tänase päeva kohta soovitakse infot
        apiResponse = getDictFromJson('http://api.openweathermap.org/data/2.5/weather?q='
                                      + info["city"] + '&units=metric&APPID=' + APIKEY)
    return parseApiResponse(apiResponse)





# teeb kindlaks, mis päeva kohta infot küsitakse.
def checkForDateTime(text):
    if re.search("homme", text):
        info["time"] = "tomorrow"
    elif re.search("ülehom", text):
        info["time"] = "dayAfterTomorrow"
    else: # järelikult peab olema tänase kohta
        info["time"] = "today"

    # Kahjuks tasuta API ajaloolist infot ei võimalda otsida

# teeb kindlaks, mis sorti infot soovitakse
def checkForKeywords(text):
    if re.search("ilm", text):
        info["dataAsked"] = "general"
    if re.search("sooja|soe|külm|temperat", text):
        info["dataAsked"] = "temp"
    if re.search("vihm", text):
        info["dataAsked"] = "rain"
    if re.search("lumi|lund", text):
        info["dataAsked"] = "snow"

# otsib kohanimesid tekstist
def checkForCity(text):
    upperCaseWords = re.findall("[A-ZÜÖÄÕ][A-ZÜÖÄÕa-züöä|-]+", text)
    # Kas sidekriipsuga kohanimi?
    if len(upperCaseWords) > 1:
        if ("-" not in upperCaseWords[1]):
            info["city"] = cityLemma(upperCaseWords[1])
        else:
            info["city"] = upperCaseWords[1]
    # Tavaline kohanimi
    elif len(upperCaseWords) == 1:
        city = cityLemma(upperCaseWords[0])
        if (city in cities):
            info["city"] = city

# otsib linnade algvorme
def cityLemma(city):
    file = urllib.request.urlopen('http://prog.keeleressursid.ee/ws_etmrf/lemma.php?s=' + urllib.parse.quote(city))
    analyys = json.loads(file.read().decode())
    return analyys['root']


def getDictFromJson(url):
    file = urllib.request.urlopen(url)
    data = json.loads(file.read().decode('utf-8'))
    return data


def reset():
    info = {}
    info["dataAsked"] = ""
    info["time"] = ""
    info["city"] = ""


if __name__ == '__main__':
    for s in sentencesPos:
        print(getResponse(s, 1))
    #print(getResponse("Kas praegu Tartus lund sajab?",1))
