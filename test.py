import requests
import json
import re
import vesselfunctions

terminalurl = "https://www.wsdot.wa.gov/ferries/vesselwatch/Terminals.ashx"
vesselurl = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"

vesselresp = requests.get(vesselurl)
terminalresp = requests.get(terminalurl)

if vesselresp.status_code == 200 and terminalresp.status_code == 200:
    print("Successfully accessed pages!")
    vessels = json.loads(vesselresp.text)
    vessellist = vessels["vessellist"]

    regex = r'new Date\(\d*\)'
    terminalstring = re.sub(regex, "null", terminalresp.text, flags=re.MULTILINE)
    terminals = json.loads(terminalstring)
    terminallist = terminals["FeedContentList"]

    BainbridgeTerminal = vesselfunctions.findterminal(terminallist, "Bainbridge Island")
    leavingBainbridge = vesselfunctions.findvessel(vessellist, "Bainbridge Island", "SEA-BI")

    if leavingBainbridge:
        for i in range(0, len(leavingBainbridge)):
            current = leavingBainbridge[i]
            nextFerry = BainbridgeTerminal[i]
            output = vesselfunctions.getoutput(current, nextFerry["Cancelled"])
            print(output)
    else:
        print("No ferries are going from Bainbridge to Seattle right now")

    SeattleTerminal = vesselfunctions.findterminal(terminallist, "Seattle")
    leavingSeattle = vesselfunctions.findvessel(vessellist, "Seattle", "SEA-BI")
    SeattleNext = []
    for i in range(0, len(SeattleTerminal)):
        if SeattleTerminal[i]["ArriveSailingSpaces"][0]["TerminalName"] == "Bainbridge Island":
            SeattleNext.append(SeattleTerminal[i])
    if leavingSeattle:
        for i in range(0, len(leavingSeattle)):
            current = leavingSeattle[i]
            nextFerry = SeattleNext[i]
            SEAoutput = vesselfunctions.getoutput(current, nextFerry["Cancelled"])
            print(SEAoutput)
    else:
        print("No ferries are going from Seattle to Bainbridge right now")
else:
    print("The page could not be successfully accessed")
