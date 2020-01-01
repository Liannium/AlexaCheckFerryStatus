import requests
import json
import re

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


def getbiseattleferries(ferries: list, terminals: list) -> str:
    returnstring = ''
    BainbridgeTerminal = findterminal(terminals, "Bainbridge Island")
    leavingBainbridge = findvessel(ferries, "Bainbridge Island", "SEA-BI")

    if leavingBainbridge:
        for i in range(0, len(leavingBainbridge)):
            current = leavingBainbridge[i]
            nextFerry = BainbridgeTerminal[i]
            returnstring += getoutput(current, nextFerry["Cancelled"])
    else:
        returnstring += "No ferries are going from Bainbridge to Seattle right now. "

    SeattleTerminal = findterminal(terminals, "Seattle")
    leavingSeattle = findvessel(ferries, "Seattle", "SEA-BI")
    SeattleNext = []
    for i in range(0, len(SeattleTerminal)):
        if SeattleTerminal[i]["ArriveSailingSpaces"][0]["TerminalName"] == "Bainbridge Island":
            SeattleNext.append(SeattleTerminal[i])
    if leavingSeattle:
        for i in range(0, len(leavingSeattle)):
            current = leavingSeattle[i]
            nextFerry = SeattleNext[i]
            returnstring += getoutput(current, nextFerry["Cancelled"])
    else:
        returnstring += "No ferries are going from Seattle to Bainbridge right now."

    return returnstring
