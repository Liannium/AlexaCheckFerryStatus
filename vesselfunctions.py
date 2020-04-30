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
        output = "The {} {} sailing from {} to {} has been cancelled. ".format(ferry["nextdep"], ferry["nextdepAMPM"],
                                                                               ferry["lastdock"], ferry["aterm"])
    if ferry["eta"] == "":
        output = "The estimated arrival of the ferry currently leaving {} cannot be found.".format(ferry["lastdock"])
    elif ferry["eta"] == "Calculating":
        output = "The estimated arrival of the {} {} ferry departing from {} is being calculated. ".format(
            ferry["nextdep"], ferry["nextdepAMPM"], ferry["lastdock"])
    else:
        output = "The {} {} sailing of the {} from {} to {} left the dock at {} {} and is expected to arrive at {} " \
                 "{}. ".format(ferry["nextdep"], ferry["nextdepAMPM"], ferry["name"], ferry["lastdock"], ferry["aterm"],
                               ferry["leftdock"], ferry["leftdockAMPM"], ferry["eta"], ferry["etaAMPM"])
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


def getseattleferries(ferries: list, terminals: list, route: str, terminalname: str) -> str:
    returnstring = ''
    otherTerminal = findterminal(terminals, terminalname)
    leavingOther = findvessel(ferries, terminalname, route)
    returnstring += getalloutput(leavingOther, otherTerminal, terminalname, "Seattle")

    SeattleTerminal = findterminal(terminals, "Seattle")
    leavingSeattle = findvessel(ferries, "Seattle", route)
    SeattleNext = []
    for i in range(0, len(SeattleTerminal)):
        if SeattleTerminal[i]["ArriveSailingSpaces"][0]["TerminalName"] == terminalname:
            SeattleNext.append(SeattleTerminal[i])
    returnstring += getalloutput(leavingSeattle, SeattleTerminal, "Seattle", terminalname)
    return returnstring


def checkferries(ferries: list, terminals: list, route: str, terminal1name: str, terminal2name: str) -> str:
    returnstring = ''
    terminal1 = findterminal(terminals, terminal1name)
    leavingterminal1 = findvessel(ferries, terminal1name, route)
    returnstring += getalloutput(leavingterminal1, terminal1, terminal1name, terminal2name)
    terminal2 = findterminal(terminals, terminal2name)
    leavingterminal2 = findvessel(ferries, terminal2name, route)
    returnstring += getalloutput(leavingterminal2, terminal2, terminal2name, terminal1name)
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


def checkFVSferries(ferries: list, terminals: list) -> str:
    leavingVashon = findvessel(ferries, "Vashon Island", "F-V-S")
    returnstring = getallFVSoutput(leavingVashon, "Vashon Island", "Fauntleroy")
    leavingFauntleroy = findvessel(ferries, "Fauntleroy", "F-V-S")
    returnstring += getallFVSoutput(leavingFauntleroy, "Fauntleroy", "Vashon Island")
    leavingSouthworth = findvessel(ferries, "Southworth", "F-V-S")
    returnstring += getallFVSoutput(leavingSouthworth, "Southworth", "Vashon Island")
    return returnstring


def getallFVSoutput(ferries: list, terminal1: str, terminal2: str) -> str:
    returnstring = ''
    if ferries:
        for i in range(0, len(ferries)):
            current = ferries[i]
            returnstring += getFVSoutput(current)
    else:
        returnstring = "There are no ferries going from " + terminal1 + " to " + terminal2 + " right now. "
    return returnstring


def getFVSoutput (ferry: dict):
    if ferry["eta"] == "":
        output = "The estimated arrival of the ferry currently leaving {} cannot be found. ".format(ferry["lastdock"])
    elif not ferry["nextdep"]:
        output = ""
    elif ferry["eta"] == "Calculating":
        output = "The estimated arrival of the {} {} ferry departing from {} is being calculated. ".format(
            ferry["nextdep"], ferry["nextdepAMPM"], ferry["lastdock"])
    else:
        output = "The {} {} sailing of the {} from {} to {} left the dock at {} {} and is expected to arrive at {} " \
                 "{}. ".format(ferry["nextdep"], ferry["nextdepAMPM"], ferry["name"], ferry["lastdock"], ferry["aterm"],
                              ferry["leftdock"], ferry["leftdockAMPM"], ferry["eta"], ferry["etaAMPM"])
    return output
