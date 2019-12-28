def findvessel(ferries: list, departingfrom: str, route: str) -> list:
    returnvessels = []
    for i in range(0, len(ferries)):
        current = ferries[i]
        if current["lastdock"] == departingfrom and current["route"] == route:
            returnvessels.append(current)
    return returnvessels


def findterminal(terminals: list, name: str):
    for i in range(0, len(terminals)):
        current = terminals[i]
        if current["Terminal"]["TerminalName"] == name:
            return terminals[i]["DepartSailingSpaces"]
    return None


def getoutput(ferry: dict, departure: str, canceled: bool) -> str:
    output = ""
    if canceled:
        output = "The " + departure + " sailing from " + ferry["lastdock"] + " to " + ferry["aterm"] + " has been "\
            + "cancelled"
    if ferry["eta"] == "":
        output = "The estimated arrival of the ferry currently leaving " + ferry["lastdock"] + " can not be found"
    elif ferry["eta"] == "Calculating":
        output = "The estimated arrival of the " + departure + " ferry departing from " + ferry["lastdock"] + \
                 " is being calculated"
    else:
        output = "The " + departure + " sailing of the " + ferry["name"] + " from " + ferry["lastdock"] + " to " + \
            ferry["aterm"] + " left the dock at " + ferry["leftdock"] + " " + ferry["leftdockAMPM"] + \
            " and is expected to arrive at " + ferry["eta"] + " " + ferry["etaAMPM"]
    return output
