import urllib.request
import json
import re
import math
from datetime import date, timedelta, datetime

# Roboti kirjeldus, kasutuspiirangud ===================================
"""
Robot annab info aktsiturgude ja krüptorahade kohta. Aksiaid või krüptorahasid saab küsida nende indeksite järgi (Näiteks: Apple on AAPL, Mastercard on MA, Bitcoin on BTC)
Indekseid soovitatav sisestada suurte tähtedega, sest siis on tulemus kindlam õige tulemus. Rootilt saab küsida aktsiate uudiseid, hinda, turumahtu ja hinna muutust.
Krüptorahade päring on piiratud ainult indeksi täisnime ja viimase hinna leidmisele.
Indeksi otsimiseks tuleb sisestada koos indeksiga kas 'aktsia' või 'krüpto' (Kui seda kohe ei tee, siis robot küsib üle).
Aktsia hinna otsimiseks kuupäeva järgi sisestada kuupäev järgnevalt: AAAA-KK-PP
Bot võib olla veidikene aeglane, sest kui otsib indeksit, siis käib üle 8000+ indeksi niimekirja.
"""
# ======================================================================

# Positiivsed testlaused (laused, mille puhul peab dialoogsüsteem tagastama mõistliku vastuse just sellelt robotilt)
sentencesPos = [
    "Tere, mina olen Villem",
    "Mis on aktsia AAPL hind?",
    "Mis on väärtpaberi v hind?",
    "Mis oli kupüüri MSFT hind eile?",
    "Aktsia AAPL hind üleeile?",
    "Aktsia TSLA hind 2018-11-20",
    "Mis on krüptoraha BTC hind?",
    "Kes on eilse päeva aktsia turu kaotajad?",
    "Kes on aktsiate top tõusjad?",
    "Ütle mulle aktsia MSFT uudised",
    "Aktsia MA hind, muutus, kauplemisemaht ja uudised",
    "Mis on aktsiate TSLA, MA ja GOOGL nimetused?"
]

info = {}
info["dataAsked"] = ""  # Andmed mida küsitakse (N. hind, hinnamuutus jne)
info["dateTime"] = ""  # default value on today
info["index"] = ""  # Mis indeksit küsitakse
info["text"] = "" #Sisestatud teksti hoiab mälus

dataAsked = []  # Andmed mida küsitakse (N. hind, hinnamuutus jne)
indexes = []  # Kõik indeksid, mida küsitakse


def getResponse(text, initiative):
    # Otsime nime
    upperCaseWords = re.findall("[A-ZÜÖÄÕ][A-ZÜÖÄÕa-züöä|-]+", text)
    # tervitus
    if re.search("mina|olen|minu|nimi", text.lower()):
        if (len(upperCaseWords) > 1):
            # kasutaja sisestas enda nime
            return 1, "Tere, " + upperCaseWords[1] + "!", 0
    elif re.search("ter|terv|tsau|hei|servus", text.lower()):
        return 1, "Tere-Tere!", 0

    # Kui tekstis leidub selliseid sõnu siis jätkame finants roboti tööga
    if re.search(
            "aktsia|stock|krüpto|raha|hind|kahaneja|võitja|kasvaja|kaotaja|kasv|langeja|firma|fond|väärtpaber|ettevõte",
            text.lower()):
        return sisu(text, initiative)
    else:
        return 0, "Finantsrobot ei oska siinkoha vastust anda", 0


def sisu(text, initiative):
    # Nullime kõik globaalsete muutujate anemd
    reset()
    confidenceValue = 0.9
    response = "Vabandust, ma ei saanud midagi aru :("

    # Otsime tegevuse sõnu tekstis (N: hind, hinnavahe, uudised jne)
    checkForWords(text)
    # Otsime kuupäeva tekstist
    checkForDateTime(text)

    # Kui puudub sõna aktsia või krüpto, siis küsime seda järgi
    if info["dataAsked"] == "":
        info["text"] = text #salvestame sisestatud teksti mällu
        return 1, "Kas sa otsid aktsia või krüptoraha kohta infot?", 0
    else:
        if info["text"] != "": #Kui varasemalt on mälus tekst
            text = info["text"] #võtame mälust vana teksti
            info["text"] = "" #
            checkForWords(text) #Kontrollime uuesti üle sõnad
            checkForDateTime(text) #Kontrollime uuesti üle kuupäevad
    # Kui kürpto päring
    if info["dataAsked"] == "krüpto":
        if "gainers" in dataAsked or "losers" in dataAsked:
            print("Kahjuks krüptorahade puhul hetkel ei toimi päeva võitjate ja kaotajate analüüs\n")
        searchCryptoIndexFromText(text)
        # Kui ei leitud ühtegi indeksit (andmebaas suht väikene)
        if not indexes:
            return 1, "Minu andmebaasis ei ole sellist münti. Võis ka jutuda, et sa sisestasid midagi valesti.", 0
        # Kui leiduvad indeksid ja on küsitud midagi konkreetset
        if indexes and dataAsked:
            return 1, getCryptoData(), 0

    # Kui aktsia päring
    elif info["dataAsked"] == "aktsia":
        searchStockIndexFromText(text)
        result = ""
        if "gainers" in dataAsked or "losers" in dataAsked:
            # Otsime välja päeva kaotajad või võitja
            result += getGainersOrLosers()
        # Kui olemas indeksid (MA, AAPL jne) ja andmed ida tahetakse (hind, maht jne)
        if indexes and dataAsked:
            result += getStockData()
        # Kui ei küsita midagi konkreetset, siis tagastame info
        else:
            result += indexInfo()
        return 1, result, 0

    return confidenceValue, response, 0


def getGainersOrLosers():
    result = ""
    for data in dataAsked:
        if "gainers" in dataAsked:
            # Küsime API käest kõik võitjad
            gainers = getDictFromJson("https://api.iextrading.com/1.0/stock/market/list/gainers")
            result += "\n TOP10 KASVAJAD:\n"
            # Läbime kogu listi
            for gainer in gainers:
                result += "Sümbol: " + gainer["symbol"] + " |Nimi: " + gainer["companyName"] + " |Vahetus: " + gainer[
                    "primaryExchange"] + " |Sektor: " + gainer["sector"] + " |Hind: " + \
                          str("{0:.1f}".format(gainer["close"])) + " |Muutus " + str(
                    "{0:.1f}".format(gainer["changePercent"])) + "%"
                # Kui antud objekt ei ole viimane listis, siis lisame reavahetuse
                if gainer != gainers[-1]:
                    result += "\n"
        if "losers" in dataAsked:
            # Küsime API käest kõik kaotajad
            losers = getDictFromJson("https://api.iextrading.com/1.0/stock/market/list/losers")
            result += "\nTOP10 KAHANEJAD:\n"
            # Läbime kogu listi
            for loser in losers:
                result += "Sümbol: " + loser["symbol"] + " |Nimi: " + loser["companyName"] + " |Vahetus: " + loser[
                    "primaryExchange"] + " |Sektor: " + loser["sector"] + " |Hind: " + \
                          str("{0:.1f}".format(loser["close"])) + " |Muutus " + str(
                    "{0:.1f}".format(loser["changePercent"])) + "%"
                # Kui antud objekt ei ole viimane listis, siis lisame reavahetuse
                if loser != losers[-1]:
                    result += "\n"
    return result


def getCompanyInfo(index):
    # Küsime API käest ette antud indeksi kohta infot
    return getDictFromJson('https://api.iextrading.com/1.0/stock/' + index + '/company')


def indexInfo():
    result = ""
    # Käime läbi indeksite listi
    for i in indexes:
        # Korjame andmed selle ettevõtte kohta
        company = getCompanyInfo(i)
        result += "Sümbol: " + company["symbol"] + " |Nimi: " + company["companyName"] + " |Vahetus: " + company[
            "exchange"] + " |Valdkond: " + company["industry"] + " |Sektor: " + company["sector"] + " |CEO: " + company[
                      "CEO"]
        if i != indexes[-1]:
            result += "\n"
    # Kui ei ole sisestaud ühtegi indeksit või on vigaselt sisestatud (Näiteks AAPL asemel APPL)
    if result == "":
        result += "Ei leidnud mitte ühtegi vastet. Kas sa sisestasid midagi valesti?"
    return result


def searchCryptoIndexFromText(text):
    # Otsime tekstis sõnu, mis on pikemad kui 2 tähte ja kõik on suured tähed
    mostPossibleIndexes = re.findall("[A-ZÜÖÄÕ][A-ZÜÖÄÕ]+", text)
    allIndexes = searchCryptoIndexes()
    for i in mostPossibleIndexes:
        for data in allIndexes:
            if data["symbol"] == str(i).upper() + "USDT":
                info["index"] = str(i).upper() + "USDT"
                indexes.append(data["symbol"])
    # Kui mostPossibleIndexes list on tühi, siis käime läbi kogu teksti
    if info["index"] == "":
        allText = text.split(" ")
        for i in allText:
            for data in allIndexes:
                if data["symbol"] == str(i).upper() + "USDT":
                    info["index"] = str(i).upper() + "USDT"
                    indexes.append(data["symbol"])


def searchStockIndexFromText(text):
    # Sorteerime teksitst välja kõik sõnad mis on ainult suurte tähtedega kirjutatud (vahel võib olla punkt või sidekriips)
    mostPossibleIndexes = re.findall("[A-ZÜÖÄÕ][A-ZÜÖÄÕ|\.\-]+", text)
    allIndexes = searchStockIndexes()

    for i in mostPossibleIndexes:
        for data in allIndexes:
            if data["symbol"] == str(i).upper():
                info["index"] = str(i).upper()
                indexes.append(data["symbol"])
    # Kui ei leitud parimat tulemust
    if info["index"] == "":
        allText = text.split(" ")
        # Käime üle kogu teksti
        for i in allText:
            for data in allIndexes:
                if data["symbol"] == str(i).upper():
                    info["index"] = str(i).upper()
                    indexes.append(data["symbol"])


def searchStockIndexes():
    # Küsime API'lt kõik aktsiate sümbolid
    return getDictFromJson('https://api.iextrading.com/1.0/ref-data/symbols')


def searchCryptoIndexes():
    # Küsime API käest kõik krüptorahade indeksid
    return getDictFromJson('https://api.iextrading.com/1.0/stock/market/crypto')


def checkForDateTime(text):
    # ajahetk
    if re.search("täna|praegu|hetk|hetkel", text):
        info["dateTime"] = date.today()
    if re.search("eile", text):
        info["dateTime"] = date.today() - timedelta(days=1)
    if re.search("üleeile", text):
        info["dateTime"] = date.today() - timedelta(days=2)
    allText = text.split(" ")
    for i in allText:
        try:
            x = datetime.strptime(i, '%Y-%m-%d')
            if isinstance(x, datetime):
                info["dateTime"] = datetime.strptime(i, '%Y-%m-%d')
        except:
            continue


def checkForWords(text):
    # aktsia või krüpto
    if re.search("aktsia|stock|väärtpaber|kupüür", text.lower()):
        info["dataAsked"] = "aktsia"
    if re.search("krüpto|krüptorahad", text):
        info["dataAsked"] = "krüpto"

    # tüüp
    if re.search("hind|väärtus|maksumus", text):
        dataAsked.append("price")
    if re.search("muutus|liikumine", text):
        dataAsked.append("change")  # Protsentuaalselt palju muutunud on
    if re.search("maht|kauplemisemaht", text):
        dataAsked.append("volume")

    # uudised
    if re.search("uudised|uudis", text):
        dataAsked.append("news")

    # Gainers and losers
    if re.search("kasvaja|tõusja|võitja", text):
        dataAsked.append("gainers")
    if re.search("kahaneja|kaotaja|langeja", text):
        dataAsked.append("losers")

    # üleüldine info
    if re.search("info|nimetus", text):
        dataAsked.append("info")


def getStockData():
    # Siin meetodis käime läbi kõik tegurid listis dataAsk (n: hind, muutus, maht jne) ja lisame need vastusesse
    result = ""
    stockInfo = getDictFromJson('https://api.iextrading.com/1.0/stock/' + info["index"] + '/time-series')
    if info["dateTime"] == "":
        for tegurid in dataAsked:
            if tegurid == "price":
                hind = getDictFromJson('https://api.iextrading.com/1.0/stock/' + info["index"] + '/price')
                result += "Indeksi " + info["index"] + " viimane hind: " + str(hind) + " USD"
            if tegurid == "change":
                result += "Kuupäeva: " + str(stockInfo[-1]["date"]) + " hinnamuutus oli: " + str(
                    "{0:.1f}".format(stockInfo[-1]["change"])) + "" \
                                                                 " USD ja protsentuaalselt: " + str(
                    "{0:.1f}".format(stockInfo[-1]["changePercent"])) + "%"
            if tegurid == "volume":
                result += "Kuupäeva: " + str(stockInfo[-1]["date"]) + " kauplemise maht: " + str(
                    stockInfo[-1]["volume"]) + " USD"
            if tegurid != dataAsked[-1]:
                result += "\n"
    else:
        for day in stockInfo:
            if day["date"] == info["dateTime"].strftime("%Y-%m-%d"):
                for tegurid in dataAsked:
                    koikAndmed = getDictFromJson(
                        'https://api.iextrading.com/1.0/stock/' + info["index"] + '/time-series')
                    if tegurid == "price":
                        if koikAndmed:
                            result += getPrice(koikAndmed)
                    if tegurid == "change":
                        result += "Hinnamuutus oli: " + str(day["change"]) + "ja protsentuaalselt: " + str(
                            "{0:.1f}".format(day["changePercent"]))
                    if tegurid == "volume":
                        result += "Kuupäeva: " + str(day["date"]) + " kauplemise maht: " + str(day["volume"]) + " USD"
        if result == "":
            result += "Antud kuupäevaga vasteid ei leidnud"

    # Vaatame kas küsiti uudiseid
    if "news" in dataAsked:
        uudised = getDictFromJson('https://api.iextrading.com/1.0/stock/' + info["index"] + '/batch?types=news')
        result += "\n======UUDISED======\n"
        for news in uudised["news"]:
            result += "PEALKIRI: \n" + news["headline"] + "\n"
            result += "SISU: \n" + news["summary"] + "\n"
            result += "ALLIKAS: " + news["source"] + "\n"
            result += "LINK: " + news["url"] + "\n"
            result += "========================\n"

    # Kas küsiti üldist infot
    if "info" in dataAsked:
        koik = searchStockIndexes()
        for index in koik:
            for i in indexes:
                if index["symbol"] == i:
                    result += "\nSümbol: " + index["symbol"] + " |Täispikk nimi: " + index["name"]
    return result


def getCryptoData():
    if info["index"] != "":
        data = getDictFromJson('https://api.iextrading.com/1.0/stock/market/crypto')
        for i in data:
            if info["index"] == i["symbol"]:
                return "Sümbol: " + i["symbol"] + " |Nimi: " + i["companyName"] + " |Hind: " + str(
                    "{0:.1f}".format(i["close"]))
    return "Sisestage ka indeks, mille kohta soovite infot"


def getPrice(data):
    # Otsime väja aktsia hinna küsitud puupäeva järgi
    askedDate = info["dateTime"].strftime("%Y-%m-%d")
    # Kui hinnad puuduvad
    if len(data) == 0:
        return "Antud indeksile ei leidnud hinda"
    # Kui küsitud kuupäeva hinnad on olemas
    for day in data:
        if day["date"] == askedDate:
            result = "Hind: " + str(day["close"]) + " USD kuupäeva seisuga: " + askedDate
            return result
    # Kui küsitud kuupäeva hinda pole, siis tagastab viimase hinna
    else:
        result = "Kuupäevaga " + askedDate + " kahjuks ei leidnud tulemust. Viimane turu hind: " + \
                 str(data[-1]["close"]) + " USD kuupäeva seisuga: " + data[-1]["date"]
        return result


def reset():
    # Nullime kõik andmed
    info["dataAsked"] = ""
    info["dateTime"] = ""
    info["index"] = ""

    dataAsked[:] = []
    indexes[:] = []


def getDictFromJson(url):
    file = urllib.request.urlopen(url)
    data = json.loads(file.read().decode())
    return data

if __name__ == '__main__':
    for s in sentencesPos:
        print(getResponse(s,1))