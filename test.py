import requests
import json
import vesselfunctions

#terminalurl = "https://www.wsdot.wa.gov/ferries/vesselwatch/Terminals.ashx"
vesselurl = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"

#TODO: Make sure it can handle multiple ferries going to Bainbridge/Seattle at once

vesselresp = requests.get(vesselurl)
#terminalresp = requests.get(terminalurl)

if vesselresp.status_code == 200:
    print("Successfully accessed pages!")
    vessel = json.loads(vesselresp.text)
    vessellist = vessel["vessellist"]
    leavingBainbridge = vesselfunctions.findvessel(vessellist, "Bainbridge Island", "SEA-BI")
    if leavingBainbridge:
        for i in range(0, len(leavingBainbridge)):
            current = leavingBainbridge[i]
            print(current["eta"])
            BIoutput = vesselfunctions.getoutput(current)
            print(BIoutput)
    else:
        print("The ferry leaving Bainbridge could not be found")

    leavingSeattle = vesselfunctions.findvessel(vessellist, "Seattle", "SEA-BI")
    if leavingSeattle is not None:
        for i in range(0, len(leavingSeattle)):
            current = leavingSeattle[i]
            print(current["eta"])
            SEAoutput = vesselfunctions.getoutput(current)
            print(SEAoutput)
    else:
        print("The ferry leaving Seattle could not be found")
else:
    print("The page could not be successfully accessed")
