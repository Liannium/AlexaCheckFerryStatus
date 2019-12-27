def findvessel(ferries: list, departingfrom: str, route: str) -> dict:
    returnvessel = ferries[0]
    found = False
    for i in range(0, len(ferries)):
        current = ferries[i]
        if current["lastdock"] == departingfrom and current["route"] == route:
            returnvessel = ferries[i]
            found = True
    if found:
        return returnvessel
    else:
        return None


def getoutput(ferry: dict) -> str:
    output = ""

    if ferry["eta"] == "":
        output = "The estimated arrival of the ferry currently leaving " + ferry["lastdock"] + " can not be found"
    elif ferry["eta"] == "Calculating":
        output = "The estimated arrival of the ferry currently leaving " + ferry["lastdock"] + " is being calculated"
    else:
        output = "The " + ferry["name"] + " is estimated to arrive in " + ferry["aterm"] + " at " + ferry["eta"] + " " \
                 + ferry["etaAMPM"]
    return output
