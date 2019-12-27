import requests
import json
from bs4 import BeautifulSoup

url = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"

#TODO: Make sure it can handle multiple ferries going to Bainbridge/Seattle at once

vesselresp = requests.get(url)

if vesselresp.status_code == 200:
    print("Successfully accessed page!")
    vessel = json.loads(vesselresp.text)
    vessellist = vessel["vessellist"]
    leavingBainbridge = vessellist[0]
    for i in range(0, len(vessellist)):
        current = vessellist[i]
        if current["lastdock"] == "Bainbridge Island" and current["route"] == "SEA-BI":
            leavingBainbridge = vessellist[i]
    if leavingBainbridge["eta"] == "":
        print("The estimated arrival of the ferry currently leaving Bainbridge Island can not be found")
    elif leavingBainbridge["eta"] == "Calculating":
        print("The estimated arrival of the ferry currently leaving Bainbridge Island is being calculated")
    else:
        output = "The " + leavingBainbridge["name"] + " is estimated to arrive in Seattle at " + \
                 leavingBainbridge["eta"] + " " + leavingBainbridge["etaAMPM"]

    leavingSeattle = vessellist[0]
    for i in range(0, len(vessellist)):
        current = vessellist[i]
        if current["lastdock"] == "Seattle" and current["route"] == "SEA-BI":
            leavingSeattle = vessellist[i]
    print(leavingSeattle)
