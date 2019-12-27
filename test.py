import requests
import json
import vesselfunctions

url = "https://www.wsdot.com/ferries/vesselwatch/Vessels.ashx"

#TODO: Make sure it can handle multiple ferries going to Bainbridge/Seattle at once

vesselresp = requests.get(url)

if vesselresp.status_code == 200:
    print("Successfully accessed page!")
    vessel = json.loads(vesselresp.text)
    vessellist = vessel["vessellist"]
    leavingBainbridge = vesselfunctions.findvessel(vessellist, "Bainbridge", "SEA-BI")
    if leavingBainbridge is not None:
        print(leavingBainbridge["eta"])
        BIoutput = vesselfunctions.getoutput(leavingBainbridge)
        print(BIoutput)
    else:
        print("The ferry leaving Bainbridge could not be found")

    leavingSeattle = vesselfunctions.findvessel(vessellist, "Seattle", "SEA-BI")
    if leavingSeattle is not None:
        print(leavingSeattle["eta"])
        SEAoutput = vesselfunctions.getoutput(leavingSeattle)
        print(SEAoutput)
    else:
        print("The ferry leaving Seattle could not be found")
else:
    print("The page could not be successfully accessed")
