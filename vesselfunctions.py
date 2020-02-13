import json
import re
import requests

vesselurl = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"
terminalurl = "https://www.wsdot.wa.gov/ferries/vesselwatch/Terminals.ashx"

def findvessel(ferries: list, departingfrom: str, route: str) -> list:
    """finds the vessel currently sailing from the specified dock on the specified route"""
    returnvessels = []
    for i in range(0, len(ferries)):
        current = ferries[i]
        if current["lastdock"] == departingfrom and current["route"] == route:
            returnvessels.append(current)
    return returnvessels


def findterminal(terminals: list, name: str):
    """finds the specified terminal"""
    for i in range(0, len(terminals)):
        current = terminals[i]
        if current["Terminal"]["TerminalName"] == name:
            return terminals[i]["DepartSailingSpaces"]
    return None


def getoutput(ferry: dict, canceled: bool) -> str:
    """returns the output string"""
    output = ""
    if canceled:
        output = "The " + ferry["nextdep"] + " " + ferry["nextdepAMPM"] + " sailing from " + ferry["lastdock"] + " to "\
                 + ferry["aterm"] + " has been " + "cancelled. "
    if ferry["eta"] == "":
        output = "The estimated arrival of the ferry currently leaving " + ferry["lastdock"] + " cannot be found. "
    elif ferry["eta"] == "Calculating":
        output = "The estimated arrival of the " + ferry["nextdep"] + " " + ferry["nextdepAMPM"] + \
                 " ferry departing from " + ferry["lastdock"] + " is being calculated. "
    else:
        output = "The " + ferry["nextdep"] + " " + ferry["nextdepAMPM"] +  " sailing of the " + ferry["name"] + \
                 " from " + ferry["lastdock"] + " to " + ferry["aterm"] + " left the dock at " + ferry["leftdock"] + \
                 " " + ferry["leftdockAMPM"] + " and is expected to arrive at " + ferry["eta"] + " " + \
                 ferry["etaAMPM"] + ". "
    return output


def getalloutput(ferries: list, terminaldata, terminal1: str, terminal2: str) -> str:
    returnstring = ''
    if ferries and terminaldata:
        for i in range(0, len(ferries)):
            current = ferries[i]
            nextFerry = terminaldata[i]
            returnstring += getoutput(current, nextFerry["Cancelled"])
    else:
        returnstring = "There are no ferries going from " + terminal1 + " to " + terminal2 + " right now. "
    return returnstring


def getSeaBrferries (ferries: list, terminals: list) -> str:
    returnstring = ''
    BremertonTerminal = findterminal(terminals, "Bainbridge Island")
    leavingBremerton = findvessel(ferries, "Bainbridge Island", "SEA-BR")
    returnstring += getalloutput(leavingBremerton, BremertonTerminal, "Bremerton", "Seattle")

    SeattleTerminal = findterminal(terminals, "Seattle")
    leavingSeattle = findvessel(ferries, "Seattle", "SEA-BR")
    SeattleNext = []
    for i in range(0, len(SeattleTerminal)):
        if SeattleTerminal[i]["ArriveSailingSpaces"][0]["TerminalName"] == "Bremerton":
            SeattleNext.append(SeattleTerminal[i])
    returnstring += getalloutput(leavingSeattle, SeattleTerminal, "Seattle", "Bremerton")
    return returnstring


def getbiseattleferries(ferries: list, terminals: list) -> str:
    returnstring = ''
    BainbridgeTerminal = findterminal(terminals, "Bainbridge Island")
    leavingBainbridge = findvessel(ferries, "Bainbridge Island", "SEA-BI")
    returnstring += getalloutput(leavingBainbridge, BainbridgeTerminal, "Bainbridge Island", "Seattle")

    SeattleTerminal = findterminal(terminals, "Seattle")
    leavingSeattle = findvessel(ferries, "Seattle", "SEA-BI")
    SeattleNext = []
    for i in range(0, len(SeattleTerminal)):
        if SeattleTerminal[i]["ArriveSailingSpaces"][0]["TerminalName"] == "Bainbridge Island":
            SeattleNext.append(SeattleTerminal[i])
    returnstring += getalloutput(leavingSeattle, SeattleTerminal, "Seattle", "Bainbridge Island")

    return returnstring


def getEdKingferries(ferries: list, terminals: list) -> str:
    returnstring = ''
    EdmondsTerminal = findterminal(terminals, "Edmonds")
    leavingEdmonds = findvessel(ferries, "Edmonds", "ED-KING")
    returnstring += getalloutput(leavingEdmonds, EdmondsTerminal, "Edmonds", "Kingston")
    KingstonTerminal = findterminal(terminals, "Kingston")
    leavingKingston = findvessel(ferries, "Kingston", "ED-KING")
    returnstring += getalloutput(leavingKingston, KingstonTerminal, "Kingston", "Edmonds")
    return returnstring


def loadvessellist():
    vesselresp = requests.get(vesselurl)
    if vesselresp.status_code != 200:
        return None
    else:
        vessels = json.loads(vesselresp.text)
        return vessels["vessellist"]


def loadterminallist():
    terminalresp = requests.get(terminalurl)
    if terminalresp.status_code != 200:
        return None
    else:
        regex = r'new Date\(\d*\)'
        terminalstring = re.sub(regex, "null", terminalresp.text, flags=re.MULTILINE)
        terminals = json.loads(terminalstring)
        return terminals["FeedContentList"]
